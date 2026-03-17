# PICVIDGENNS

Python-based launcher to build a **local Google Colab environment** for multiple Hugging Face Spaces apps (including NSFW/video face-swap workflows), then expose them through temporary Gradio public links (typically ~72 hours).

## What this provides

- Clones these Spaces locally into Colab:
  - `Heartsync/NSFW-Uncensored-video2`
  - `greg7025/swaping`
  - `r3gm/wan2-2-fp8da-aoti-preview`
  - `tonyassi/video-face-swap`
- Creates an isolated `env` virtual environment inside each project.
- Installs `requirements.txt` for each app.
- Runs selected app with `GRADIO_SHARE=True` so Gradio prints a public temporary link.

## Quick start (Google Colab)

Run this in a Colab notebook cell:

```bash
!git clone https://github.com/<your-user>/<your-repo>.git
%cd <your-repo>
!python colab_local_nsfw_editor.py --setup-all
```

Then launch one app:

```bash
!python colab_local_nsfw_editor.py --run heartsync_nsfw_video2
```

You can also list available app keys:

```bash
!python colab_local_nsfw_editor.py --list
```

## App keys

- `heartsync_nsfw_video2`
- `greg7025_swaping`
- `r3gm_wan2_preview`
- `tonyassi_video_face_swap`

## Notes

- Gradio share links are temporary by design (commonly around 72 hours).
- Some Spaces may require large model downloads and extended setup time.
- If a repo needs gated access, login/token setup may be required.
- Ensure all usage complies with local law and platform/content policies.
