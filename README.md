# 🎬 Hikari Youtube Video Downloader

**Developed by Gary19gts**

A modern and elegant YouTube video downloader with a clean interface inspired by minimalist design principles.

![Version](https://img.shields.io/badge/version-1.2-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- **Modern UI**: Clean, minimalist interface with two-column layout
- **Multiple Qualities**: Download from 360p to 4K (2160p)
- **Format Support**: MP4, WEBM, MKV
- **Dual Engine**: Choose between yt-dlp or pytube
- **Video Preview**: See video information before downloading
- **Smart Analysis**: Automatic format detection and availability checking
- **Progress Tracking**: Real-time download progress
- **Easy to Use**: Simple and intuitive interface

## 🚀 Quick Start

### Windows
```bash
# Double-click to run
run_hikari.bat
```

### All Platforms
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python hikari-youtube-video-downloader.py
```

## 📦 Requirements

- Python 3.8 or higher
- Dependencies (auto-installed):
  - `yt-dlp>=2023.12.30` - Primary download engine
  - `pytube>=15.0.0` - Alternative download engine
  - `customtkinter>=5.2.0` - Modern UI framework
  - `requests>=2.31.0` - HTTP requests
  - `Pillow>=10.0.0` - Image processing

## 🎯 How to Use

1. **Paste URL**: Copy and paste a YouTube video URL
2. **Verify**: Click "Verify" to analyze the video
3. **Configure**: Select quality, format, and processing engine
4. **Download**: Click "Download Video" to start

### Settings

- **Video Quality**: Choose from 360p to 4K
- **Video Format**: MP4 (recommended), WEBM, or MKV
- **Processing Engine**: yt-dlp (recommended) or pytube
- **Output Folder**: Select where to save downloads

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'yt_dlp'"**
```bash
pip install yt-dlp
```

**"No module named 'pytube'"**
```bash
pip install pytube
```

**Video not available**
- Check if the URL is correct
- Video might be region-blocked
- Try switching processing engine

### Diagnostics

Click the "Diagnostics" button in the app to check:
- Installed libraries
- Current settings
- System information

## 📊 Supported Qualities

| Quality | Resolution | Typical Size (10 min) |
|---------|-----------|----------------------|
| 4K | 2160p | 2-5 GB |
| 2K | 1440p | 1-2 GB |
| Full HD | 1080p | 500 MB - 1 GB |
| HD | 720p | 200-500 MB |
| SD | 480p | 100-200 MB |
| Low | 360p | 50-100 MB |

## 🎨 Interface

The application features a modern two-column layout:

**Left Column (Settings)**
- Video URL input with verify button
- Quality, format, and engine selectors
- Output folder selection
- Support development section

**Right Column (Preview)**
- Video preview and information
- Download progress
- Action buttons (Download, Open Folder, Diagnostics)
- Quick links (Update Libraries, Credits)


## 💝 Support Development

### Thank you for using **Hikari Youtube Video Downloader**!

**Made with ❤️ by Gary19gts**

---

If Hikari has been helpful to you, please consider supporting its development:

### ☕ Buy me a coffee on Ko-fi

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Development-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/gary19gts)

**→ [https://ko-fi.com/gary19gts](https://ko-fi.com/gary19gts)**

---

✨ **Even the smallest donation can bring a big light during these tough times.**  
**Even $1 can help more than you think** 😀🙏

---

### Thank you so much for standing with me! ✨

## 📄 License

**Hikari Youtube Video Downloader** is dual-licensed:

### Option 1: AGPL-3.0 (Free & Open Source)
This software is licensed under the GNU Affero General Public License v3.0.
- ✅ Free to use, modify, and distribute
- ✅ Must share source code modifications
- ✅ Must use AGPL-3.0 for derivative works
- ✅ Network use triggers copyleft

### Option 2: Commercial License
For proprietary/commercial use without AGPL-3.0 obligations:
- ✅ Use in closed-source applications
- ✅ No obligation to share source code
- ✅ Remove attribution (if agreed)
- 💰 Contact Gary19gts for pricing

**Choose the license that fits your needs.**

See [LICENSE](LICENSE) file for full details.

---

## 📚 Third-Party Libraries

This software uses the following open-source libraries:

- **yt-dlp** - YouTube video downloader (Unlicense)
- **pytube** - Python YouTube library (MIT)
- **customtkinter** - Modern UI framework (MIT)
- **Pillow** - Image processing (HPND)
- **requests** - HTTP library (Apache 2.0)

All third-party licenses are compatible with both AGPL-3.0 and commercial use.

---

## 👨‍💻 Author

**Gary19gts** - 2025

- GitHub: [@Gary19gts](https://github.com/Gary19gts)
- For commercial licensing inquiries, contact through GitHub

## ⚠️ Legal Notice

This software is for **personal and educational use only**. Please:
- Respect YouTube's Terms of Service
- Respect copyright laws
- Only download content you have rights to
- Support content creators

## 🔄 Version History

### v1.3 (Current)
- Complete UI redesign with modern two-column layout
- Improved user experience
- Better visual feedback
- Added diagnostics and credits sections

### v1.1
- Added multiple quality support
- Improved format detection
- Better error handling

### v1.0
- Initial release

## 📞 Contact

For issues, suggestions, or contributions, please open an issue on the repository.

---

**© 2025 by Gary19gts - v1.2**

*Made with ❤️ for the YouTube community*

