<h1 align=center>
	<img src=Documents/Pictures/YTMVG.svg width=175>
	<br>
	YTMVG
</h1>

<p align=center>
	<a href="https://colab.research.google.com/github/kubinka0505/YTMVG/blob/master/Documents/YTMVG.ipynb"><img src="https://img.shields.io/badge/colab-open-F9AB00?&logoColor=F9AB00&style=for-the-badge&logo=google-colab"></a>　<a href="License.txt"><img src="https://img.shields.io/github/license/kubinka0505/YTMVG?logo=readthedocs&color=red&logoColor=white&style=for-the-badge"></a>
</p>

<p align=center>
	<img src="https://img.shields.io/github/languages/code-size/kubinka0505/YTMVG?style=for-the-badge">　<a href="https://codeclimate.com/github/kubinka0505/YTMVG"><img src="https://img.shields.io/codeclimate/maintainability/kubinka0505/YTMVG?logo=code-climate&style=for-the-badge"></a>　<a href="https://app.codacy.com/gh/kubinka0505/YTMVG"><img src="https://img.shields.io/codacy/grade/0b21f77d557f42bbaa447bca8d3b03f5?logo=codacy&style=for-the-badge"></a>
</p>

## Description 📝
Pack of scripts providing customizable **Y**ou**T**ube **M**usic **V**ideos **G**eneration.
~~But applicable to a *Shorts* too.~~

It generates:
- Video from image and audio file, that also can contain the embedded front cover art. 🎦
- Thumbnail with a centered image that background color is based on the subjectively selected image color clusters. 🖼️

[**[Example YouTube Playlist]**](https://www.youtube.com/playlist?list=PLmKxR1vlf4cyHwtOvWxd1nt3B0U9E2pH7)

## Requirements 📥
Programs:
- [`Python >= 3.8`](https://www.python.org/downloads) 🐍

Modules:
- [`sty >= 1.0.4`](../../../../feluxe/sty) - Colored terminal output 🎨
- [`colour >= 0.1.5`](../../../../vaab/colour) - Color handling 🎨
- [`distro >= 1.7`](../../../../python-distro/distro)<span>*</span> - Unix directory opening handler 📂
- [`mutagen >= 1.45.1`](../../../../quodlibet/mutagen) - Audio state checker & video length handler ⏳
- [`Pillow >= 9`](../../../../python-pillow/Pillow) - Image processor 🖼️
- [`CV2`](../../../../opencv/opencv-python) - Image processor 🖼️
- [`numpy`](../../../../numpy/numpy) - Colors histogram generation ⚙️
- [`scikit-learn`](../../../../scikit-learn/scikit-learn) - Colors histogram calculations ⚙️

Packages (bold links are **Windows** static executable binaries):
- [**`FFmpeg >= 4.2`**](https://videohelp.com/software/ffmpeg/old-versions) - Video processing 🎦
	- **64-bit reccomended!** ([*memory allocation* failures](https://forum.doom9.org/archive/index.php/t-162236.html#copyright))
- [**`JPEGOptim >= 1.4.7`**](../../../../tjko/jpegoptim) - Thumbnail optimization 📉
- [`Python3-PIP`](https://packages.debian.org/sid/python3-pip)<span>*</span>
- [`Python3-TK`](https://packages.debian.org/sid/python3-tk)<span>*</span>

<span>*</span> - Required on Linux

---
## Installation ⚙️
**When on Linux**, install required packages by using this one-liner:
```bash
sudo apt-get install git python3-apt python3-pip python3-tk ffmpeg jpegoptim
```
1. Clone the repository and move to its directory.
	```bash
	git clone https://github.com/kubinka0505/YTMVG
	cd YTMVG
	```
2. Install required modules by inputting `pip install -r requirements.txt`
3. Modify the parameters in the `Config.json` file. (or use command line arguments below)
4. Type **`YTMVG.py -h`** for more info. ℹ️

## Usage 📝
Process **audio** (`-a`) and **image** (`-i`)
```bash
YTMVG.py -a "~/Music/Song.mp3" -i "~/Pictures/Image.png"
```

As above, but set the **video resolution** (`-r`) to `720p` and **audio bitrate** (`-ab`) to **128 kb/s**
```bash
YTMVG.py -i "../Cover.jpg" -a "%UserProfile%\Downloads\Sound.ogg" -r 720p -ab 128k
```

Process audio **with embedded cover**, (no `-i`) and **encode lossless audio** (`-ab 0`)
```bash
YTMVG.py -a "~/Music/Discography/Artist/Album/Artist - Title.flac" -ab 0
```

As above, but **change color** (`-c`) to `Dry` and **process silently** (`-v -1`)
```bash
YTMVG.py -a "Artist ft. Guest - Title (Remix).mp3" -c 1 -ab 0 -v -1
```

### Presets 🗃️
Program comes in with bundled presets located as text files in the [`Data/Presets`](Data/Presets) directory. You may edit them or add your own.

> ℹ️ To launch the preset, use the `-p` flag, where argument is the preset file name without last extension.
>
> Example: `YTMVG.py -a ... -p MyPreset` (`Data/Presets/MyPreset.txt`)

### **Windows Explorer Context-Menu Extension** ⚙️
By running the [`!_GUI_Add.pyw`](Utility/Windows_Explorer_Context_Menu_Extension/!_GUI_Add.pyw) file, multiple values are injected into the `HKEY_CURRENT_USER` registry hive.
<br>
It enables quick, clear and **batch** usage directly from the `Explorer.exe` level, as shown below.

<p align=center>
	<br>
	<img src=Documents/Pictures/Examples/Shell_Extension.png>
	<br>
</p>

### **Batch processing** 🗃️
You can configure the [`!_GUI_Batch_Processing.py`](Utility/GUI_Batch_Processing.py) file for your needs.

---

## Meta Info ℹ️
All versions of this project have been tested on:
| OS | Distribution | OS Version | Python Version | System Architecture (`bits`) |
|:-:|:-:|:-:|:-:|:-:|
Windows | ― | 10 | 3.11.0 | 64
Linux | Ubuntu | LTS 22.04 | 3.10.6 | 64 |