<div align="center">

# 🎬 Hikari Youtube Video Downloader

### Modern YouTube Video Downloader with Clean Interface

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Gary19gts/hikari-youtube-video-downloader)
[![Downloads](https://img.shields.io/badge/downloads-free-green.svg)](https://github.com/Gary19gts/hikari-youtube-video-downloader/releases)

<p align="center">
  <img src="hikari_icon.png" alt="Hikari Logo" width="120"/>
</p>

**A beautiful, fast, and easy-to-use YouTube video downloader built with Python**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Support](#-support)

---

</div>

## 📖 About

**Hikari Youtube Video Downloader** is a modern desktop application that makes downloading YouTube videos simple and elegant. With its clean two-column interface and powerful features, Hikari provides the best experience for saving your favorite videos offline.

### Why Hikari?

- 🎨 **Friendly Interface** - Modern, minimalist design that's easy on the eyes
- ⚡ **Fast Downloads** - Powered by yt-dlp and pytube engines
- 🎯 **Smart Quality Selection** - Automatic format detection with manual override
- 📊 **Real-time Progress** - See exactly what's happening during downloads
- 🔧 **Flexible Options** - Multiple qualities, formats, and engines to choose from
- 💾 **Persistent Settings** - Your preferences are saved automatically
- 🆓 **100% Free** - No ads, no subscriptions, no hidden costs

---

## ✨ Features

### Core Functionality

<table>
<tr>
<td width="50%">

#### 📥 Download Options
- **Multiple Qualities**: 360p, 480p, 720p, 1080p, 1440p, 4K (2160p)
- **Format Support**: MP4, WEBM, MKV
- **Dual Engines**: yt-dlp (recommended) or pytube
- **Best Available**: Automatic quality selection

</td>
<td width="50%">

#### 🎨 User Experience
- **Video Preview**: See thumbnail and info before downloading
- **Format Analysis**: View all available formats and sizes
- **Progress Tracking**: Real-time download progress bar
- **Smart Warnings**: Alerts for unavailable formats

</td>
</tr>
<tr>
<td width="50%">

#### ⚙️ Advanced Features
- **Custom Output Folder**: Save anywhere you want
- **Persistent Configuration**: Settings saved between sessions
- **Library Updates**: One-click update for all dependencies
- **Diagnostics Panel**: Check system status and libraries

</td>
<td width="50%">

#### 🌐 Compatibility
- **Cross-platform**: Windows, macOS, Linux
- **Python 3.8+**: Modern Python support
- **URL Detection**: Automatic YouTube URL validation
- **Error Handling**: Clear, helpful error messages

</td>
</tr>
</table>

---

## 🚀 Installation

### Quick Start (Windows)

1. **Download** the repository
2. **Double-click** `run_hikari.bat`
3. **Done!** The app will install dependencies and launch automatically

### Manual Installation (All Platforms)

```bash
# Clone the repository
git clone https://github.com/Gary19gts/hikari-youtube-video-downloader.git
cd hikari-youtube-video-downloader

# Install dependencies
pip install -r requirements.txt

# Run the application
python hikari-youtube-video-downloader.py
```

### Automatic Installer

```bash
# Run the installer script
python install.py
```

The installer will:
- ✅ Check Python version
- ✅ Install all dependencies
- ✅ Verify installation
- ✅ Create desktop shortcut (Windows)

---

## 📦 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **Internet Connection**: Required for downloads
- **Storage**: 100 MB for app + space for videos

### Dependencies

All dependencies are installed automatically:

```
yt-dlp>=2023.12.30      # Primary download engine
pytube>=15.0.0          # Alternative download engine  
customtkinter>=5.2.0    # Modern UI framework
requests>=2.31.0        # HTTP requests
Pillow>=10.0.0          # Image processing
```

---

## 🎯 Usage

### Basic Workflow

1. **Paste URL** → Copy a YouTube video URL and paste it into the input field
2. **Verify** → Click "Verify" to analyze the video and see available formats
3. **Configure** → Select your preferred quality, format, and processing engine
4. **Download** → Click "Download Video" and wait for completion
5. **Enjoy** → Open the output folder to access your video

### Interface Overview

<table>
<tr>
<td width="50%">

#### Left Column - Settings
- 🔗 **Video URL Input** with verify button
- 🎬 **Quality Selector** (360p to 4K)
- 📹 **Format Selector** (MP4, WEBM, MKV)
- ⚙️ **Engine Selector** (yt-dlp or pytube)
- 📁 **Output Folder** selection

</td>
<td width="50%">

#### Right Column - Preview
- 🖼️ **Video Thumbnail** and information
- 📊 **Available Formats** analysis
- 📈 **Progress Bar** with status
- 🔽 **Download Button**
- 🛠️ **Action Buttons** (Open Folder, Diagnostics)

</td>
</tr>
</table>

### Tips & Tricks

- 💡 Use **yt-dlp** engine for best compatibility
- 💡 Select **MP4** format for maximum device support
- 💡 Choose **1080p** for the best quality/size balance
- 💡 Click **ℹ️** icons for contextual help
- 💡 Use **Diagnostics** to troubleshoot issues

---

## 📊 Quality Comparison

| Quality | Resolution | Typical Size (10 min) | Best For |
|---------|-----------|----------------------|----------|
| **4K** | 2160p | 2-5 GB | Large screens, archiving |
| **2K** | 1440p | 1-2 GB | High-quality viewing |
| **Full HD** | 1080p | 500 MB - 1 GB | ⭐ Recommended |
| **HD** | 720p | 200-500 MB | Mobile devices |
| **SD** | 480p | 100-200 MB | Low storage |
| **Low** | 360p | 50-100 MB | Slow connections |

---

## 🛠️ Troubleshooting

### Common Issues

<details>
<summary><b>❌ "No module named 'yt_dlp'"</b></summary>

```bash
pip install yt-dlp
```
</details>

<details>
<summary><b>❌ "No module named 'pytube'"</b></summary>

```bash
pip install pytube
```
</details>

<details>
<summary><b>❌ "Video not available"</b></summary>

- Check if the URL is correct
- Video might be region-blocked or private
- Try switching to the other processing engine
- Update libraries using the in-app button
</details>

<details>
<summary><b>❌ "Selected quality not available"</b></summary>

- Click "Verify" to see available formats
- Choose a different quality from the dropdown
- Try "Best available" option
</details>

<details>
<summary><b>❌ Download is very slow</b></summary>

- Check your internet connection
- Try a lower quality
- Close other bandwidth-heavy applications
</details>

### Using Diagnostics

Click the **"Diagnostics"** button in the app to check:
- ✅ Installed libraries and versions
- ✅ Current settings and configuration
- ✅ System information
- ✅ Output folder status

---


## ⚠️ Legal Notice

**Important**: This software is for **personal and educational use only**.

### Please Remember

- ✅ Respect YouTube's Terms of Service
- ✅ Respect copyright laws and content creators' rights
- ✅ Only download content you have permission to download
- ✅ Support creators by watching ads or subscribing
- ❌ Do not use for commercial purposes without permission
- ❌ Do not redistribute downloaded content

**Hikari is a tool, not an endorsement of copyright infringement.**

---

## 📄 License

**Hikari Youtube Video Downloader** is dual-licensed:

### 🆓 Option 1: AGPL-3.0 (Free & Open Source)

This software is licensed under the GNU Affero General Public License v3.0.

- ✅ Free to use, modify, and distribute
- ✅ Must share source code modifications
- ✅ Must use AGPL-3.0 for derivative works
- ✅ Network use triggers copyleft

### 💼 Option 2: Commercial License

For proprietary/commercial use without AGPL-3.0 obligations:

- ✅ Use in closed-source applications
- ✅ No obligation to share source code
- ✅ Remove attribution requirements (if agreed)
- 💰 Contact Gary19gts for pricing

**Choose the license that fits your needs.**

See [LICENSE](LICENSE) file for full AGPL-3.0 text.

---

## 🙏 Third-Party Libraries

This software uses the following excellent open-source libraries:

| Library | Purpose | License |
|---------|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube video downloader | Unlicense |
| [pytube](https://github.com/pytube/pytube) | Python YouTube library | MIT |
| [customtkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern UI framework | MIT |
| [Pillow](https://python-pillow.org/) | Image processing | HPND |
| [requests](https://requests.readthedocs.io/) | HTTP library | Apache 2.0 |

All third-party licenses are compatible with both AGPL-3.0 and commercial use.

---

## 💝 Support

Thank you for using **Hikari Youtube Video Downloader**! Made with ❤️ by **Gary19gts**

If Hikari has been helpful to you, please consider supporting its development:

<div align="center">

### ☕ Buy me a coffee on Ko-fi

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Development-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/gary19gts)

**→ [https://ko-fi.com/gary19gts](https://ko-fi.com/gary19gts)**

✨ Even the smallest donation can bring a big light during these tough times.  
Even $1 can help more than you think 😀🙏

**Thank you so much for standing with me!** ✨

</div>

### Other Ways to Support

- ⭐ **Star this repository** on GitHub
- 🐛 **Report bugs** and suggest features
- 📢 **Share** Hikari with friends and communities
- 💬 **Provide feedback** to improve the app


---

## 📊 Project Stats

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/Gary19gts/hikari-youtube-video-downloader)
![GitHub code size](https://img.shields.io/github/languages/code-size/Gary19gts/hikari-youtube-video-downloader)
![Lines of code](https://img.shields.io/tokei/lines/github/Gary19gts/hikari-youtube-video-downloader)
![GitHub last commit](https://img.shields.io/github/last-commit/Gary19gts/hikari-youtube-video-downloader)

</div>

---

## 👨‍💻 Author

<div align="center">

**Gary19gts**

[![GitHub](https://img.shields.io/badge/GitHub-Gary19gts-181717?style=for-the-badge&logo=github)](https://github.com/Gary19gts)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-gary19gts-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/gary19gts)

*Passionate developer creating tools that make life easier*

</div>

---

## 📞 Contact

- 💬 **Issues**: [GitHub Issues](https://github.com/Gary19gts/hikari-youtube-video-downloader/issues)
- 📧 **Email**: Contact through GitHub
- 💼 **Commercial Licensing**: Contact through GitHub for inquiries

---

## 🌟 Acknowledgments

Special thanks to:

- The **yt-dlp** team for their amazing downloader
- The **pytube** developers for their Python library
- The **CustomTkinter** creator for the modern UI framework
- All **contributors** and **users** of Hikari
- The **open-source community** for inspiration and support


---

<div align="center">

## ⭐ Star History

If you find Hikari useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=Gary19gts/hikari-youtube-video-downloader&type=Date)](https://star-history.com/#Gary19gts/hikari-youtube-video-downloader&Date)

---

### Made with ❤️ by Gary19gts

**© 2025 Gary19gts - Hikari Youtube Video Downloader v1.3**

*Bringing light to your video downloads*

---

[⬆ Back to Top](#-hikari-youtube-video-downloader)

</div>
