<h1 align=center><img src=https://raw.githubusercontent.com/kubinka0505/YTMVG/master/Documents/Pictures/YTMVG.svg width=175><br>YTMVG</h1>

<p align=center><a href=https://colab.research.google.com/github/kubinka0505/YTMVG/blob/master/Documents/YTMVG.ipynb><img src=https://img.shields.io/badge/colab-open-F9AB00?&logo=google-colab&logoColor=F9AB00&style=for-the-badge></a>　<a href=https://youtube.com/watch?v=QQaUcnWe3ls><img src=https://shields.io/badge/showcase-watch-F00?logo=youtube&style=for-the-badge></a>　<a href=https://github.com/kubinka0505/YTMVG/blob/master/License.txt><img src=https://img.shields.io/github/license/kubinka0505/YTMVG?logo=readthedocs&color=red&logoColor=white&style=for-the-badge></a></p>

<p align=center><img src=https://img.shields.io/tokei/lines/github/kubinka0505/YTMVG?style=for-the-badge>　<img src=https://img.shields.io/github/languages/code-size/kubinka0505/YTMVG?style=for-the-badge>　<a href=https://codeclimate.com/github/kubinka0505/YTMVG><img src=https://img.shields.io/codeclimate/maintainability/kubinka0505/YTMVG?logo=code-climate&style=for-the-badge></a>　<a href=https://app.codacy.com/gh/kubinka0505/YTMVG><img src=https://img.shields.io/codacy/grade/0b21f77d557f42bbaa447bca8d3b03f5?logo=codacy&style=for-the-badge></a></p>

## Description 📝
Pack of scripts providing customizable **Y**ou**T**ube **M**usic **V**ideos **G**eneration.

It generates:
- Square video from image and audio file, which also can contain the embedded cover art. 🎦
- Thumbnail with a centered image that background color is based on image color clusters. 🖼️

[**[Example YouTube Playlist]**](https://www.youtube.com/playlist?list=PLmKxR1vlf4cyHwtOvWxd1nt3B0U9E2pH7)

## Requirements 📥
Programs:
- [`Python >= 3.7`](https://www.python.org/downloads) 🐍

Modules:
- [`sty >= 0.0.4`](https://github.com/feluxe/sty) - Colored terminal output 🎨
- [`ffpb > 0.4.1`](https://github.com/kubinka0505/ffpb-fix) - [FFmpeg](https://github.com/FFmpeg/FFmpeg) progress bar ⏳ *(optional)*
- [`Pillow >= 5.1`](https://github.com/python-pillow/Pillow) - Image processor 🖼️
- [`mutagen >= 1.45.1`](https://github.com/quodlibet/mutagen) - Audio state checker & video length handler ⏳
- [`distro >= 1.7`](https://github.com/python-distro/distro)<span>*</span> - Directory opening helper 📂

Packages (bold links are **Windows** static executable binaries):
- [**`FFmpeg >= 4.2`**](https://videohelp.com/software/ffmpeg/old-versions) - Video processing 🎦
	- **Check after 64-bit if possible!** ([*memory allocation* failures](https://forum.doom9.org/archive/index.php/t-162236.html#copyright))
- [**`JPEGOptim >= 1.4.7`**](https://github.com/tjko/jpegoptim) - Thumbnail optimization 📉
- [`Python3-PIP`](https://packages.debian.org/sid/python3-pip)<span>*</span>

<span>*</span> - Required on Linux

---
## Installation ⚙️
**When on Linux**, install required packages by using this one-liner:
```bash
sudo apt-get install git python3-apt python3-pip ffmpeg jpegoptim
```
1. Clone the repository and move to its directory.
	```bash
	git clone https://github.com/kubinka0505/YTMVG
	cd YTMVG
	```
2. Install required modules by inputting `pip install -r requirements.txt`
3. Modify the parameters in the `Config.json` file.
4. Type **`YTMVG.py -h`** for more info. ℹ️

## Usage 📝
Process **audio** (`-a`) and **image** (`-i`)
```bash
YTMVG.py -a "~/Music/Song.flac" -i "~/Pictures/Image.png"
```

As above, but set the **maximum video resolution** (`-r`) to `720p` and **audio bitrate** (`-ab`) to **128 kb/s**
```bash
YTMVG.py -i "../Cover.jpg" -a "%UserProfile%\Downloads\Sound.mp3" -r 720p -ab 128k
```

Process audio **with embedded cover**, (no `-i`) and **encode lossless audio** (`-flac`)
```bash
YTMVG.py -a "~/Music/Discography/Artist/Album/Artist - Title.flac" -ab 0
```

As above, but **change cluster** (`-c`) to `Dominant` and **process silently** (`-q`)
```bash
YTMVG.py -a "Artist ft. Guest - Title (Remix).wav" -c DOM -ab 0 -q
```

### **Batch processing** 🗃️
For batch processing file, please configure the [`Utility/Batch_Processing.py`](https://github.com/kubinka0505/YTMVG/blob/master/Utility/Batch_Processing.py).

---

## Meta Info ℹ️
All versions of this project have been tested on:
| OS | Distribution | OS Version | Python Version | System Architecture (`bits`) |
|:-:|:-:|:-:|:-:|:-:|
Windows | ― | 10 | 3.7.6 | 32, 64
Linux | Ubuntu | LTS 22.04 | 3.8.10 | 64 |