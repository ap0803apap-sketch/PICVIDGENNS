# PICVIDGENNS

Python launcher for a **single-cell Google Colab workflow** that clones and runs selected Hugging Face Spaces locally, then prints a temporary public Gradio link.

## Direct source links

- https://huggingface.co/spaces/Heartsync/NSFW-Uncensored-video2
- https://huggingface.co/spaces/greg7025/swaping
- https://huggingface.co/spaces/r3gm/wan2-2-fp8da-aoti-preview
- https://huggingface.co/spaces/tonyassi/video-face-swap

## One-cell Colab automation (recommended)

Run **one Colab cell** (replace only `YOUR_GITHUB_USERNAME` with your actual GitHub username):

```python
!git clone https://github.com/YOUR_GITHUB_USERNAME/PICVIDGENNS.git && \
cd PICVIDGENNS && \
python colab_local_nsfw_editor.py --auto heartsync_nsfw_video2
```

This does everything automatically:
1. Installs system packages (`git`, `git-lfs`)
2. Clones/updates the selected HF Space
3. Creates virtual environment
4. Installs requirements
5. Launches app with `GRADIO_SHARE=True`
6. Prints temporary public Gradio link in logs

## If you want a direct "Open in Colab" link

Use this format (replace placeholders):

```text
https://colab.research.google.com/github/YOUR_GITHUB_USERNAME/PICVIDGENNS/blob/main/<notebook>.ipynb
```

## App keys (for `--auto`, `--setup`, `--run`)

- `heartsync_nsfw_video2`
- `greg7025_swaping`
- `r3gm_wan2_preview`
- `tonyassi_video_face_swap`

## Other commands

List available app keys:

```python
!python colab_local_nsfw_editor.py --list
```

Setup only (do not run):

```python
!python colab_local_nsfw_editor.py --setup heartsync_nsfw_video2
```

Run only (after setup):

```python
!python colab_local_nsfw_editor.py --run heartsync_nsfw_video2
```

Setup all apps:

```python
!python colab_local_nsfw_editor.py --setup-all
```

## Notes

- Gradio share links are temporary (often around 72 hours).
- Large models may take significant download/setup time in Colab.
- If any Space is gated, authentication/token may be required.
- Follow all laws and platform/content policies.
