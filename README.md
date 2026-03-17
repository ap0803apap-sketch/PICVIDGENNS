# PICVIDGENNS

Python-based launcher to build a **local Google Colab environment** for multiple Hugging Face Spaces apps, then expose them through temporary Gradio public links (typically ~72 hours).

## How to clone this repo in Google Colab

### Option A (recommended): clone from GitHub

Open a new Colab notebook and run:

```python
!git clone https://github.com/<your-user>/<your-repo>.git
%cd <your-repo>
```

Then verify files are present:

```python
!ls
```

You should see `colab_local_nsfw_editor.py` and `README.md`.

### Option B: private GitHub repo clone in Colab

If your repo is private, use a GitHub token:

```python
import os, getpass
os.environ["GH_TOKEN"] = getpass.getpass("GitHub token: ")
```

```python
!git clone https://$GH_TOKEN@github.com/<your-user>/<your-private-repo>.git
%cd <your-private-repo>
```

---

## Run setup in Colab

Install/prepare all configured apps:

```python
!python colab_local_nsfw_editor.py --setup-all
```

Or set up only one app:

```python
!python colab_local_nsfw_editor.py --setup heartsync_nsfw_video2
```

## Launch an app with temporary public link

```python
!python colab_local_nsfw_editor.py --run heartsync_nsfw_video2
```

When startup finishes, Gradio prints a share URL (temporary link, often around 72 hours).

## Available app keys

- `heartsync_nsfw_video2`
- `greg7025_swaping`
- `r3gm_wan2_preview`
- `tonyassi_video_face_swap`

You can print them anytime with:

```python
!python colab_local_nsfw_editor.py --list
```

## Notes

- Some Spaces require large model downloads and can take a while in Colab.
- If a Space is gated, login/token setup may be required.
- Use responsibly and follow all applicable laws and platform/content policies.
