<h1 align=center>
	<img src=Documents/Pictures/YTMVG.svg width=175>
	<br>
	YTMVG
</h1>

<p align=center>
	<!--a href="https://shields.io/github/kubinka0505/YTMVG/blob/master/Documents/YTMVG.ipynb"><img src="https://shields.io/badge/Colab-Open-F9AB00?&logoColor=F9AB00&style=for-the-badge&logo=Google-Colab"></a--><a href="License.txt"><img src="https://custom-icon-badges.demolab.com/github/license/kubinka0505/YTMVG?logo=law&color=red&style=for-the-badge"></a>
</p>

<p align=center>
	<img src="https://custom-icon-badges.demolab.com/github/languages/code-size/kubinka0505/YTMVG?logo=database&style=for-the-badge">　<a href="https://codeclimate.com/github/kubinka0505/YTMVG"><img src="https://shields.io/codeclimate/maintainability/kubinka0505/YTMVG?logo=Code-Climate&style=for-the-badge"></a>　<a href="https://app.codacy.com/gh/kubinka0505/YTMVG"><img src="https://shields.io/codacy/grade/0b21f77d557f42bbaa447bca8d3b03f5?logo=Codacy&style=for-the-badge"></a>
</p>

## Description 📝
<a href="https://www.youtube.com/playlist?list=PLmKxR1vlf4cyHwtOvWxd1nt3B0U9E2pH7">
	<img align=right src="https://shields.io/badge/YouTube-Example_Playlist-F00?logo=YouTube&logoColor=FFF&style=for-the-badge">
</a>

Pack of scripts providing customizable **Y**ou**T**ube **M**usic **V**ideos **G**eneration.
~~But applicable to *Shorts* too.~~

It generates:
- Video from image and audio file, that also can contain the embedded front cover art. 🎦
- Thumbnail with a centered image that background color is based on the subjectively selected image color clusters. 🖼️

---

## Requirements 📥
Programs:
- [`Python >= 3.8`](https://www.python.org/downloads) 🐍

Modules:
- [`sty >= 1.0.4`](https://github.com/feluxe/sty) - Colored terminal output 🎨
- [`colour >= 0.1.5`](https://github.com/vaab/colour) - Colors handling 🎨
- [`distro >= 1.7`](https://github.com/python-distro/distro)<span>*</span> - Unix directory opening handler 📂
- [`mutagen >= 1.45.1`](https://github.com/quodlibet/mutagen) - Audio state checker & video length handler ⏳
- [`Pillow >= 9`](https://github.com/python-pillow/Pillow) - Image processor 🖼️
- [`CV2`](https://github.com/opencv/opencv-python) - Image processor 🖼️
- [`numpy`](https://github.com/numpy/numpy) - Colors histogram generation ⚙️
- [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) - Colors histogram calculations ⚙️

Packages (bold links are **Windows** static executable binaries):
- [**`FFmpeg >= 4.2`**](https://videohelp.com/software/ffmpeg/old-versions) - Video processing 🎦
	- **64-bit reccomended!** ([*possible memory allocation* failures](https://forum.doom9.org/archive/index.php/t-162236.html#copyright))
- [**`JPEGOptim >= 1.4.7`**](https://github.com/tjko/jpegoptim) - Thumbnail optimization 📉
- [`Python3-PIP`](https://packages.debian.org/sid/python3-pip)<span>*</span>
- [`Python3-TK`](https://packages.debian.org/sid/python3-tk)<span>*</span>

<span>*</span> - Required on Linux

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

---

## Usage 📝
Process **audio** (`-a`) and **image** (`-i`)
```bash
YTMVG.py -a "~/Music/Song.mp3" -i "~/Pictures/Image.png"
```

As above, but set the **video resolution** (`-r`) to `720p` and **audio bitrate** (`-ab`) to **128 kb/s**
```bash
YTMVG.py -i "../Cover.jpg" -a "%UserProfile%\Downloads\Sound.ogg" -r 720p -ab 128k
```

Process **audio with embedded cover**, (no `-i`) **encode lossless audio** (`-ab 257`) and encode as WebM (`-webm`)
```bash
YTMVG.py -a "~/Music/Discography/Artist/Album/Artist - Title.flac" -ab 257 -webm
```

As above, but **process audio URL**, **change color** (`-c`) to `Dry` and **process silently** (`-v -1`)
```bash
YTMVG.py -a "https://website.com/Artist ft. Guest - Title (Remix).flac" -ab 257 -webm -c 1 -v -1
```

### Presets 🗃️
Program comes in with bundled presets located as text files in the [`Data/Presets`](Data/Presets) directory. You may edit them or add your own.

> [!Note]
> To launch the preset, use the `-p` flag, where argument is the preset file name without last extension.<br><br>
> Example: `YTMVG.py -a ... -p MyPresetFile` (`Data/Presets/MyPresetFile.txt`)

---

### **Windows Explorer Context Menu Extension** ⚙️
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

## Disclaimer ⚠️

> [!Important]
> This program is a free and open-source tool including implementation of the algorithm responsible for creating YouTube music videos and its thumbnails.<br><br>
> It uses other free open-source tools and resources available in the public domain to guarantee satisfactory results, albeit the author of this particular software is not affiliated with YouTube or its associates, nor can be responsible — as stated in the license file — for guaranteeing its correct behavior and the consequences resulting from its improper use.

---

## Meta Info ℹ️
All versions of this project have been tested on:
| OS | Distribution | OS Version | Python Version | System Architecture (`bits`) |
|:-:|:-:|:-:|:-:|:-:|
| Windows | ― | 10 | 3.11.0 | 64 |
| Linux | Ubuntu | LTS 22.04 | 3.10.6 | 64 |