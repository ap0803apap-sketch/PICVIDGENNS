#!/usr/bin/env python3
"""
Colab launcher for self-hosted Gradio apps cloned from Hugging Face Spaces.

This script helps reproduce a "Fooocus/Defooocus-like" workflow in Google Colab:
- clone selected repositories
- create per-project virtualenvs
- install dependencies
- launch chosen app with a public Gradio share link (typically expires in ~72h)

Usage (inside Colab):
    !python colab_local_nsfw_editor.py --setup-all
    !python colab_local_nsfw_editor.py --run heartsync_nsfw_video2
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


WORKSPACE_DEFAULT = Path("/content/nsfw_editor_workspace")


@dataclass(frozen=True)
class AppConfig:
    key: str
    repo_url: str
    folder: str
    run_cmd: str = "python app.py"
    requirements_file: str = "requirements.txt"


APPS: tuple[AppConfig, ...] = (
    AppConfig(
        key="heartsync_nsfw_video2",
        repo_url="https://huggingface.co/spaces/Heartsync/NSFW-Uncensored-video2",
        folder="NSFW-Uncensored-video2",
    ),
    AppConfig(
        key="greg7025_swaping",
        repo_url="https://huggingface.co/spaces/greg7025/swaping",
        folder="swaping",
    ),
    AppConfig(
        key="r3gm_wan2_preview",
        repo_url="https://huggingface.co/spaces/r3gm/wan2-2-fp8da-aoti-preview",
        folder="wan2-2-fp8da-aoti-preview",
    ),
    AppConfig(
        key="tonyassi_video_face_swap",
        repo_url="https://huggingface.co/spaces/tonyassi/video-face-swap",
        folder="video-face-swap",
    ),
)

APP_BY_KEY = {app.key: app for app in APPS}


def run(cmd: str | list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    if isinstance(cmd, list):
        printable = " ".join(shlex.quote(p) for p in cmd)
    else:
        printable = cmd
    prefix = f"[cwd={cwd}] " if cwd else ""
    print(f"\n>>> {prefix}{printable}")
    subprocess.run(cmd, cwd=cwd, env=env, check=True, shell=isinstance(cmd, str))


def ensure_system_packages() -> None:
    run("apt-get update")
    # git-lfs supports many HF repos; git may already be present in Colab images.
    run("apt-get install -y git git-lfs")
    run("git lfs install")


def clone_or_update(app: AppConfig, workspace: Path) -> Path:
    target = workspace / app.folder
    if target.exists():
        print(f"Repo already exists, pulling latest: {target}")
        run("git pull", cwd=target)
    else:
        run(["git", "clone", app.repo_url, app.folder], cwd=workspace)
    return target


def venv_python(venv_dir: Path) -> Path:
    if sys.platform.startswith("win"):
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def setup_app(app: AppConfig, workspace: Path) -> Path:
    project_dir = clone_or_update(app, workspace)
    venv_dir = project_dir / "env"
    if not venv_dir.exists():
        run([sys.executable, "-m", "venv", "env"], cwd=project_dir)

    py = str(venv_python(venv_dir))
    run([py, "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"], cwd=project_dir)

    req_file = project_dir / app.requirements_file
    if req_file.exists():
        run([py, "-m", "pip", "install", "-r", app.requirements_file], cwd=project_dir)
    else:
        print(f"WARNING: requirements file not found for {app.key}: {req_file}")

    return project_dir


def setup_apps(app_keys: Iterable[str], workspace: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    ensure_system_packages()
    for key in app_keys:
        app = APP_BY_KEY[key]
        print(f"\n=== Setting up {app.key} ===")
        setup_app(app, workspace)


def run_app(app_key: str, workspace: Path) -> None:
    app = APP_BY_KEY[app_key]
    project_dir = workspace / app.folder
    venv_dir = project_dir / "env"
    py = venv_python(venv_dir)

    if not project_dir.exists() or not py.exists():
        raise FileNotFoundError(
            f"App '{app_key}' is not set up yet. Run --setup {app_key} first."
        )

    env = os.environ.copy()
    # Gradio share links are generally temporary (~72h), matching the request.
    env["GRADIO_SHARE"] = "True"
    env["PYTHONUNBUFFERED"] = "1"

    cmd = f"{shlex.quote(str(py))} {app.run_cmd}"
    print("\nLaunching app with GRADIO_SHARE=True.")
    print("A public Gradio link will be printed in logs when the app starts.")
    run(cmd, cwd=project_dir, env=env)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Colab NSFW editor environment launcher")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=WORKSPACE_DEFAULT,
        help=f"Base folder for cloned apps (default: {WORKSPACE_DEFAULT})",
    )

    parser.add_argument("--list", action="store_true", help="List available app keys")
    parser.add_argument("--setup", choices=tuple(APP_BY_KEY), help="Setup one app")
    parser.add_argument("--setup-all", action="store_true", help="Setup all apps")
    parser.add_argument("--run", choices=tuple(APP_BY_KEY), help="Run one app")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list:
        print("Available apps:")
        for app in APPS:
            print(f"- {app.key}: {app.repo_url}")
        return

    if args.setup_all:
        setup_apps((app.key for app in APPS), args.workspace)

    if args.setup:
        setup_apps((args.setup,), args.workspace)

    if args.run:
        run_app(args.run, args.workspace)

    if not any((args.list, args.setup_all, args.setup, args.run)):
        print("No action requested. Try --help")


if __name__ == "__main__":
    main()
