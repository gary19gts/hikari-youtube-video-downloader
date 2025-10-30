#!/usr/bin/env python3
"""
Hikari Youtube Video Downloader
Modern YouTube video downloader with clean interface

Copyright (C) 2025 Gary19gts

This program is dual-licensed:

1. GNU Affero General Public License v3.0 (AGPL-3.0)
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published
   by the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program. If not, see <https://www.gnu.org/licenses/>.

2. Commercial License
   For commercial use without AGPL-3.0 obligations, contact Gary19gts
   for a commercial license.

Author: Gary19gts
Website: https://github.com/Gary19gts
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import re
import subprocess
import sys
from pathlib import Path
import requests
from PIL import Image, ImageTk
import io
import json

# CustomTkinter configuration
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class HikariYoutubeDownloader:
    def __init__(self):
        print("Starting Hikari Youtube Video Downloader...")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Hikari Youtube Video Downloader - by: Gary19gts")
        self.root.geometry("1100x850")
        self.root.resizable(True, True)
        self.root.minsize(900, 700)
        
        # Set window icon
        try:
            icon_path = Path(__file__).parent / "hikari_icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Configuration file
        self.config_file = Path.home() / ".hikari_config.json"
        
        # Load saved configuration
        self.load_config()
        
        # Variables
        self.output_folder = tk.StringVar(value=self.saved_output_folder)
        self.video_quality = tk.StringVar(value="1080p")
        self.video_format = tk.StringVar(value="mp4")
        self.download_library = tk.StringVar(value="yt-dlp")
        self.url_var = tk.StringVar()
        
        # Variables for available formats
        self.available_formats = {}
        self.video_info = None
        self.current_url = ""
        
        # Setup UI
        self.setup_ui()
        
        # Bind to automatically verify URL
        self.url_var.trace('w', self.on_url_change)
        
        # Bring window to front
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        print("Window created successfully")
    
    def load_config(self):
        """Load saved configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.saved_output_folder = config.get('output_folder', str(Path.home() / "Downloads"))
                    print(f"✅ Configuration loaded: {self.saved_output_folder}")
            else:
                self.saved_output_folder = str(Path.home() / "Downloads")
                print("📁 Using default folder")
        except Exception as e:
            print(f"⚠️ Error loading configuration: {e}")
            self.saved_output_folder = str(Path.home() / "Downloads")
    
    def save_config(self):
        """Save current configuration"""
        try:
            config = {
                'output_folder': self.output_folder.get()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"💾 Configuration saved: {self.output_folder.get()}")
        except Exception as e:
            print(f"⚠️ Error saving configuration: {e}")
    
    def setup_ui(self):
        # Header con título y autor
        header_frame = ctk.CTkFrame(self.root, fg_color="#f0f0f0", height=120)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Icono y título
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(expand=True)
        
        title = ctk.CTkLabel(title_container, text="🎬 Hikari Youtube Video Downloader", 
                           font=ctk.CTkFont(size=28, weight="bold"),
                           text_color="#2b2b2b")
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(title_container, text="Developed by Gary19gts", 
                              font=ctk.CTkFont(size=12),
                              text_color="#666666")
        subtitle.pack()
        
        # Contenedor principal con dos columnas
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columna izquierda (Settings)
        left_frame = ctk.CTkFrame(main_container, fg_color="#ffffff", corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Columna derecha (Preview)
        right_frame = ctk.CTkFrame(main_container, fg_color="#ffffff", corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # ===== COLUMNA IZQUIERDA =====
        # Video URL Section
        url_section = ctk.CTkFrame(left_frame, fg_color="transparent")
        url_section.pack(fill="x", padx=20, pady=(20, 15))
        
        url_header = ctk.CTkFrame(url_section, fg_color="transparent")
        url_header.pack(fill="x", pady=(0, 8))
        
        url_label = ctk.CTkLabel(url_header, text="Video URL", 
                               font=ctk.CTkFont(size=14, weight="bold"),
                               text_color="#2b2b2b")
        url_label.pack(side="left")
        
        info_btn = ctk.CTkLabel(url_header, text="ℹ️", 
                              font=ctk.CTkFont(size=12),
                              text_color="#0078d4",
                              cursor="hand2")
        info_btn.pack(side="right")
        info_btn.bind("<Button-1>", lambda e: self.show_info_dialog("Video URL", 
            "Paste a valid YouTube URL here.\n\n"
            "Supported formats:\n"
            "• https://www.youtube.com/watch?v=...\n"
            "• https://youtu.be/...\n\n"
            "Click 'Verify' to analyze the video and see available formats."))
        
        url_input_frame = ctk.CTkFrame(url_section, fg_color="transparent")
        url_input_frame.pack(fill="x")
        
        self.url_entry = ctk.CTkEntry(url_input_frame, 
                                    textvariable=self.url_var,
                                    placeholder_text="Paste YouTube URL here...",
                                    height=40,
                                    border_width=1,
                                    corner_radius=8,
                                    fg_color="#ffffff",
                                    border_color="#d0d0d0")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.verify_button = ctk.CTkButton(url_input_frame, 
                                         text="Verify",
                                         command=self.analyze_video, 
                                         width=100, 
                                         height=40,
                                         corner_radius=8,
                                         fg_color="#0078d4",
                                         hover_color="#005a9e",
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.verify_button.pack(side="right")
        
        # URL warning label (hidden by default)
        self.url_warning_label = ctk.CTkLabel(url_section, 
                                             text="",
                                             font=ctk.CTkFont(size=11),
                                             text_color="#dc3545",
                                             wraplength=500)
        # No pack initially - will be shown when needed
        
        # Settings Section
        settings_section = ctk.CTkFrame(left_frame, fg_color="transparent")
        settings_section.pack(fill="x", padx=20, pady=15)
        
        settings_label = ctk.CTkLabel(settings_section, text="Settings", 
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color="#2b2b2b")
        settings_label.pack(anchor="w", pady=(0, 15))
        
        # Video Quality
        quality_frame = self.create_setting_row(settings_section, "Video Quality", self.video_quality,
                               ["4K (2160p)", "2K (1440p)", "1080p", "720p", "480p", "360p", "Best available"],
                               self.on_quality_change)
        
        # Quality status label
        self.quality_status_label = ctk.CTkLabel(quality_frame, 
                                                text="",
                                                font=ctk.CTkFont(size=10),
                                                text_color="#dc3545")
        self.quality_status_label.pack(anchor="w", pady=(2, 0))
        
        # Video Format  
        format_frame = self.create_setting_row(settings_section, "Video Format", self.video_format,
                               ["mp4", "webm", "mkv"],
                               self.on_format_change)
        
        # Format status label
        self.format_status_label = ctk.CTkLabel(format_frame, 
                                               text="",
                                               font=ctk.CTkFont(size=10),
                                               text_color="#dc3545")
        self.format_status_label.pack(anchor="w", pady=(2, 0))
        
        # Processing Engine
        self.create_setting_row(settings_section, "Processing Engine", self.download_library,
                               ["yt-dlp", "pytube"],
                               self.on_library_change)
        
        # Output Folder Section
        folder_section = ctk.CTkFrame(left_frame, fg_color="transparent")
        folder_section.pack(fill="x", padx=20, pady=15)
        
        folder_header = ctk.CTkFrame(folder_section, fg_color="transparent")
        folder_header.pack(fill="x", pady=(0, 8))
        
        folder_label = ctk.CTkLabel(folder_header, text="Output Folder", 
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  text_color="#2b2b2b")
        folder_label.pack(side="left")
        
        folder_info = ctk.CTkLabel(folder_header, text="ℹ️", 
                                 font=ctk.CTkFont(size=12),
                                 text_color="#0078d4",
                                 cursor="hand2")
        folder_info.pack(side="right")
        folder_info.bind("<Button-1>", lambda e: self.show_info_dialog("Output Folder", 
            "Select where to save downloaded videos.\n\n"
            "You can:\n"
            "• Click 'Browse' to select any folder\n"
            "• Click '📁' to use the default 'downloads' folder\n\n"
            "Your selection will be saved for next time."))
        
        folder_input_frame = ctk.CTkFrame(folder_section, fg_color="transparent")
        folder_input_frame.pack(fill="x")
        
        self.folder_entry = ctk.CTkEntry(folder_input_frame, 
                                       textvariable=self.output_folder,
                                       height=40,
                                       border_width=1,
                                       corner_radius=8,
                                       fg_color="#ffffff",
                                       border_color="#d0d0d0")
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Default folder button
        default_folder_button = ctk.CTkButton(folder_input_frame, 
                                    text="📁",
                                    command=self.set_default_downloads_folder, 
                                    width=40,
                                    height=40,
                                    corner_radius=8,
                                    fg_color="#0078d4",
                                    hover_color="#005a9e",
                                    text_color="#ffffff",
                                    font=ctk.CTkFont(size=16))
        default_folder_button.pack(side="right", padx=(0, 5))
        
        folder_button = ctk.CTkButton(folder_input_frame, 
                                    text="Browse",
                                    command=self.select_folder, 
                                    width=100,
                                    height=40,
                                    corner_radius=8,
                                    fg_color="#e0e0e0",
                                    hover_color="#c0c0c0",
                                    text_color="#2b2b2b",
                                    font=ctk.CTkFont(size=13))
        folder_button.pack(side="right")
        

        # ===== COLUMNA DERECHA =====
        # Video Preview Section
        preview_section = ctk.CTkFrame(right_frame, fg_color="transparent")
        preview_section.pack(fill="both", expand=True, padx=20, pady=20)
        
        preview_label = ctk.CTkLabel(preview_section, text="Video Preview", 
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color="#2b2b2b")
        preview_label.pack(anchor="w", pady=(0, 15))
        
        # Preview placeholder (ajustado a 200px)
        self.preview_frame = ctk.CTkFrame(preview_section, 
                                        fg_color="#f5f5f5",
                                        corner_radius=10,
                                        height=200)
        self.preview_frame.pack(fill="x", pady=(0, 15))
        self.preview_frame.pack_propagate(False)
        
        # Thumbnail label (to display thumbnail)
        self.thumbnail_label = ctk.CTkLabel(self.preview_frame, text="")
        self.thumbnail_label.pack(expand=True)
        
        # Placeholder icon and text (hidden when thumbnail is shown)
        self.preview_icon = ctk.CTkLabel(self.preview_frame, 
                                  text="🎵",
                                  font=ctk.CTkFont(size=60),
                                  text_color="#c0c0c0")
        self.preview_icon.place(relx=0.5, rely=0.4, anchor="center")
        
        self.preview_text = ctk.CTkLabel(self.preview_frame, 
                                       text="Paste a media URL to see content preview",
                                       font=ctk.CTkFont(size=11),
                                       text_color="#999999")
        self.preview_text.place(relx=0.5, rely=0.65, anchor="center")
        
        # Video info labels (hidden initially)
        self.video_info_frame = ctk.CTkFrame(preview_section, fg_color="transparent")
        self.video_title_label = ctk.CTkLabel(self.video_info_frame, text="", 
                                            font=ctk.CTkFont(size=12, weight="bold"),
                                            wraplength=400,
                                            text_color="#2b2b2b")
        self.video_status_label = ctk.CTkLabel(self.video_info_frame, text="",
                                             font=ctk.CTkFont(size=10),
                                             text_color="#666666")
        
        # Formats Analysis Section (nueva sección)
        self.formats_frame = ctk.CTkFrame(preview_section, fg_color="transparent")
        
        formats_header = ctk.CTkLabel(self.formats_frame, 
                                     text="📊 Available Formats", 
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     text_color="#2b2b2b")
        formats_header.pack(anchor="w", pady=(0, 8))
        
        self.formats_text = ctk.CTkTextbox(self.formats_frame, 
                                          height=120,
                                          corner_radius=8,
                                          fg_color="#f5f5f5",
                                          border_width=1,
                                          border_color="#d0d0d0",
                                          font=ctk.CTkFont(size=10))
        self.formats_text.pack(fill="x")
        self.formats_text.insert("1.0", "Analyze a video to see available formats, resolutions, and file sizes.")
        self.formats_text.configure(state="disabled")
        
        # Status and Progress
        status_section = ctk.CTkFrame(preview_section, fg_color="transparent")
        status_section.pack(fill="x", pady=(0, 15))
        
        self.status_label = ctk.CTkLabel(status_section, 
                                       text="Ready to convert",
                                       font=ctk.CTkFont(size=12),
                                       text_color="#666666")
        self.status_label.pack(anchor="w", pady=(0, 8))
        
        self.progress_bar = ctk.CTkProgressBar(status_section, 
                                             height=8,
                                             corner_radius=4,
                                             progress_color="#0078d4")
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        # Download Button
        self.download_button = ctk.CTkButton(preview_section, 
                                           text="Download Video",
                                           command=self.start_download,
                                           height=50,
                                           corner_radius=8,
                                           fg_color="#0078d4",
                                           hover_color="#005a9e",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.download_button.pack(fill="x", pady=(0, 15))
        
        # Action Buttons Row
        action_buttons = ctk.CTkFrame(preview_section, fg_color="transparent")
        action_buttons.pack(fill="x", pady=(0, 15))
        
        self.open_folder_button = ctk.CTkButton(action_buttons, 
                                              text="Open Folder",
                                              command=self.open_folder,
                                              height=40,
                                              corner_radius=8,
                                              fg_color="#e0e0e0",
                                              hover_color="#c0c0c0",
                                              text_color="#2b2b2b",
                                              font=ctk.CTkFont(size=12))
        self.open_folder_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        diagnostics_button = ctk.CTkButton(action_buttons, 
                                         text="Diagnostics",
                                         command=self.show_diagnostics,
                                         height=40,
                                         corner_radius=8,
                                         fg_color="#e0e0e0",
                                         hover_color="#c0c0c0",
                                         text_color="#2b2b2b",
                                         font=ctk.CTkFont(size=12))
        diagnostics_button.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Support Development Section
        support_section_right = ctk.CTkFrame(preview_section, fg_color="transparent")
        support_section_right.pack(fill="x", pady=(10, 0))
        
        support_header_right = ctk.CTkLabel(support_section_right, 
                                    text="☕ Support Development", 
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color="#2b2b2b")
        support_header_right.pack(anchor="w", pady=(0, 8))
        
        support_text_right = ctk.CTkLabel(support_section_right, 
                                  text="If you find Hikari useful, consider supporting its development!", 
                                  font=ctk.CTkFont(size=12),
                                  text_color="#666666",
                                  wraplength=450)
        support_text_right.pack(anchor="w", pady=(0, 12))
        
        kofi_button_right = ctk.CTkButton(support_section_right, 
                                  text="☕ Buy me a coffee on Ko-fi",
                                  command=lambda: self.open_url("https://ko-fi.com/gary19gts"),
                                  height=50,
                                  corner_radius=8,
                                  fg_color="#FF5E5B",
                                  hover_color="#E04E4B",
                                  text_color="#ffffff",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        kofi_button_right.pack(fill="x", pady=(0, 8))
        
        thanks_label_right = ctk.CTkLabel(support_section_right, 
                                  text="Thank you for your support! ❤️", 
                                  font=ctk.CTkFont(size=11),
                                  text_color="#999999")
        thanks_label_right.pack(anchor="w", pady=(0, 12))
        
        # Update Libraries Button
        self.update_button = ctk.CTkButton(support_section_right, 
                                   text="📚 Update Libraries",
                                   command=self.update_libraries,
                                   height=40,
                                   corner_radius=8,
                                   fg_color="#28a745",
                                   hover_color="#218838",
                                   text_color="#ffffff",
                                   font=ctk.CTkFont(size=12, weight="bold"))
        self.update_button.pack(fill="x")
        
        # Footer
        footer = ctk.CTkLabel(self.root, 
                            text="© 2025 by Gary19gts - v1.3",
                            font=ctk.CTkFont(size=9),
                            text_color="#999999")
        footer.pack(side="bottom", pady=5)
        
        # Initialize states
        self.check_libraries()
    
    def create_setting_row(self, parent, label_text, variable, values, command):
        """Create a settings row with consistent style"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=8)
        
        # Header con label e info
        header = ctk.CTkFrame(row_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
        
        label = ctk.CTkLabel(header, text=label_text, 
                           font=ctk.CTkFont(size=12),
                           text_color="#2b2b2b")
        label.pack(side="left")
        
        info = ctk.CTkLabel(header, text="ℹ️", 
                          font=ctk.CTkFont(size=11),
                          text_color="#0078d4",
                          cursor="hand2")
        info.pack(side="right")
        
        # Bind click event based on label text
        if label_text == "Video Quality":
            info.bind("<Button-1>", lambda e: self.show_info_dialog("Video Quality", 
                "Select the desired video quality.\n\n"
                "Higher quality = larger file size\n"
                "Lower quality = smaller file size\n\n"
                "Recommended: 1080p for best balance\n\n"
                "Note: Not all qualities are available for every video."))
        elif label_text == "Video Format":
            info.bind("<Button-1>", lambda e: self.show_info_dialog("Video Format", 
                "Select the output video format.\n\n"
                "• MP4: Most compatible, works everywhere\n"
                "• WEBM: Good compression, web optimized\n"
                "• MKV: High quality, supports multiple tracks\n\n"
                "Recommended: MP4 for maximum compatibility"))
        elif label_text == "Processing Engine":
            info.bind("<Button-1>", lambda e: self.show_info_dialog("Processing Engine", 
                "Select the download library to use.\n\n"
                "• yt-dlp: More powerful, better format support\n"
                "• pytube: Simpler, lightweight\n\n"
                "Recommended: yt-dlp for best results"))
        
        # Dropdown
        dropdown = ctk.CTkOptionMenu(row_frame, 
                                    variable=variable,
                                    values=values,
                                    command=command,
                                    height=40,
                                    corner_radius=8,
                                    fg_color="#ffffff",
                                    button_color="#0078d4",
                                    button_hover_color="#005a9e",
                                    dropdown_fg_color="#ffffff",
                                    text_color="#2b2b2b",
                                    dropdown_text_color="#2b2b2b",
                                    font=ctk.CTkFont(size=12))
        dropdown.pack(fill="x")
        
        return row_frame
    
    def open_url(self, url):
        """Abre una URL en el navegador"""
        import webbrowser
        webbrowser.open(url)
    
    def show_diagnostics(self):
        """Muestra información de diagnóstico"""
        diag_window = ctk.CTkToplevel(self.root)
        diag_window.title("Diagnostics")
        diag_window.geometry("500x400")
        
        text = ctk.CTkTextbox(diag_window, width=480, height=350)
        text.pack(padx=10, pady=10)
        
        # Información del sistema
        info = "=== HIKARI DIAGNOSTICS ===\n\n"
        
        # Check libraries
        try:
            import yt_dlp
            info += "✅ yt-dlp: Installed\n"
        except ImportError:
            info += "❌ yt-dlp: Not installed\n"
        
        try:
            import pytube
            info += "✅ pytube: Installed\n"
        except ImportError:
            info += "❌ pytube: Not installed\n"
        
        try:
            import customtkinter
            info += f"✅ customtkinter: {customtkinter.__version__}\n"
        except:
            info += "❌ customtkinter: Error\n"
        
        info += f"\n📁 Output Folder: {self.output_folder.get()}\n"
        info += f"🎬 Selected Quality: {self.video_quality.get()}\n"
        info += f"📹 Selected Format: {self.video_format.get()}\n"
        info += f"⚙️ Processing Engine: {self.download_library.get()}\n"
        
        text.insert("1.0", info)
        text.configure(state="disabled")
    
    def update_libraries(self):
        """Automatically update all libraries"""
        response = messagebox.askyesno(
            "Update Libraries",
            "This will update all libraries to their latest versions:\n\n"
            "• yt-dlp\n"
            "• pytube\n"
            "• customtkinter\n"
            "• requests\n"
            "• Pillow\n\n"
            "This may take a few minutes. Continue?"
        )
        
        if not response:
            return
        
        # Deshabilitar botón durante actualización
        self.update_button.configure(state="disabled", text="⏳ Updating...")
        self.update_status("📥 Updating libraries, please wait...")
        
        # Ejecutar actualización en hilo separado
        thread = threading.Thread(target=self._update_libraries_thread)
        thread.daemon = True
        thread.start()
    
    def _update_libraries_thread(self):
        """Thread to update libraries without blocking UI"""
        import subprocess
        import sys
        
        libraries = [
            "yt-dlp",
            "pytube",
            "customtkinter",
            "requests",
            "Pillow"
        ]
        
        success_count = 0
        failed_libs = []
        
        for i, lib in enumerate(libraries, 1):
            try:
                self.root.after(0, lambda l=lib, idx=i, total=len(libraries): 
                    self.update_status(f"📥 Updating {l}... ({idx}/{total})"))
                
                # Ejecutar pip install --upgrade
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", lib],
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minutes timeout per library
                )
                
                if result.returncode == 0:
                    success_count += 1
                else:
                    failed_libs.append(lib)
                    
            except subprocess.TimeoutExpired:
                failed_libs.append(f"{lib} (timeout)")
            except Exception as e:
                failed_libs.append(f"{lib} ({str(e)})")
        
        # Actualizar UI en el hilo principal
        self.root.after(0, lambda: self._update_libraries_complete(success_count, failed_libs))
    
    def _update_libraries_complete(self, success_count, failed_libs):
        """Callback when update finishes"""
        # Re-enable button
        self.update_button.configure(state="normal", text="📚 Update Libraries")
        
        if not failed_libs:
            self.update_status("✅ All libraries updated successfully!")
            messagebox.showinfo(
                "Update Complete",
                f"✅ Successfully updated {success_count} libraries!\n\n"
                "All libraries are now up to date."
            )
        else:
            self.update_status("⚠️ Update completed with some errors")
            failed_list = "\n".join([f"• {lib}" for lib in failed_libs])
            messagebox.showwarning(
                "Update Completed",
                f"✅ Successfully updated: {success_count} libraries\n"
                f"❌ Failed to update:\n{failed_list}\n\n"
                "You may need to update these manually."
            )
    

    def check_libraries(self):
        """Check library status"""
        # Silent verification, no UI messages
        try:
            import yt_dlp
        except ImportError:
            pass
        
        try:
            import pytube
        except ImportError:
            pass
    
    def on_url_change(self, *args):
        """Executed when URL changes"""
        url = self.url_var.get().strip()
        
        # Hide warning if no URL
        if not url:
            self.url_warning_label.pack_forget()
            return
        
        # Detect URL type and show warning if needed
        url_type, message = self.detect_url_type(url)
        
        if url_type == 'normal_video':
            # Valid URL - hide warning
            self.url_warning_label.pack_forget()
            
            if url != self.current_url:
                # Clear previous information
                self.available_formats = {}
                self.video_info = None
                self.quality_status_label.configure(text="")
                self.format_status_label.configure(text="")
                
                # Automatically verify after delay
                self.root.after(3000, lambda: self.auto_analyze(url))
        
        elif url_type == 'video_in_playlist':
            # Soft warning - can try to download
            self.url_warning_label.configure(
                text="⚠️ Playlist URL detected. Only the individual video will be downloaded.",
                text_color="#ff9800"
            )
            self.url_warning_label.pack(fill="x", pady=(5, 0))
        
        else:
            # Unsupported URL - show warning
            warning_messages = {
                'playlist': "❌ Playlists not supported. Use individual video URL.",
                'shorts': "❌ YouTube Shorts not supported. Use normal video URL.",
                'live': "❌ Live streams not supported.",
                'channel': "❌ Channel URLs not supported. Use video URL.",
                'unknown': "❌ URL not recognized. Use format: youtube.com/watch?v=..."
            }
            
            warning_text = warning_messages.get(url_type, "❌ URL not supported")
            self.url_warning_label.configure(text=warning_text, text_color="#dc3545")
            self.url_warning_label.pack(fill="x", pady=(5, 0))
    
    def auto_analyze(self, url):
        """Automatic video analysis"""
        current_url = self.url_var.get().strip()
        if current_url == url:
            url_type, _ = self.detect_url_type(url)
            # Solo auto-analizar si es video normal o video en playlist
            if url_type in ['normal_video', 'video_in_playlist']:
                self.analyze_video()
    
    def on_quality_change(self, value):
        """Executed when selected quality changes"""
        self.check_quality_availability()
    
    def on_format_change(self, value):
        """Executed when selected format changes"""
        self.check_format_availability()
    
    def on_library_change(self, value):
        """Executed when selected library changes"""
        self.check_libraries()
    
    def check_quality_availability(self):
        """Check if selected quality is available"""
        if not self.available_formats:
            self.quality_status_label.configure(text="⚠️ Analyze video first")
            return
        
        selected_quality = self.video_quality.get()
        
        if selected_quality == "Best available":
            self.quality_status_label.configure(text="")
            return
        
        # Map selector qualities to analysis keys correctly
        quality_mapping = {
            "4K (2160p)": "2160p",
            "2K (1440p)": "1440p", 
            "1080p": "1080p",
            "720p": "720p",
            "480p": "480p",
            "360p": "360p",
            "240p": "240p",
            "144p": "144p"
        }
        
        quality_key = quality_mapping.get(selected_quality, selected_quality)
        
        # Debug: show what is being searched
        print(f"DEBUG: Searching quality '{selected_quality}' -> key '{quality_key}'")
        print(f"DEBUG: Available formats: {list(self.available_formats.keys())}")
        
        # Check if quality is available
        if quality_key in self.available_formats:
            self.quality_status_label.configure(text="✅ Available")
            self.quality_status_label.configure(text_color="#28a745")
        else:
            # Find closest available quality
            available_heights = [int(k.replace('p', '')) for k in self.available_formats.keys() if k.replace('p', '').isdigit()]
            target_height = int(quality_key.replace('p', ''))
            
            if available_heights:
                closest_height = min(available_heights, key=lambda x: abs(x - target_height))
                self.quality_status_label.configure(text=f"❌ Not available. Closest: {closest_height}p")
                self.quality_status_label.configure(text_color="#dc3545")
            else:
                self.quality_status_label.configure(text="❌ Not available")
                self.quality_status_label.configure(text_color="#dc3545")
    
    def check_format_availability(self):
        """Check if selected format is available"""
        if not self.available_formats:
            self.format_status_label.configure(text="⚠️ Analyze video first")
            return
        
        selected_format = self.video_format.get()
        format_available = False
        
        for quality, formats in self.available_formats.items():
            for fmt in formats:
                if fmt['ext'].lower() == selected_format.lower():
                    format_available = True
                    break
            if format_available:
                break
        
        # Update status label
        if format_available:
            self.format_status_label.configure(text="✅ Available")
            self.format_status_label.configure(text_color="#28a745")
        else:
            self.format_status_label.configure(text="❌ Not available")
            self.format_status_label.configure(text_color="#dc3545")
    
    def show_info_dialog(self, title, message):
        """Shows an information dialog"""
        messagebox.showinfo(title, message)
    
    def set_default_downloads_folder(self):
        """Sets the default downloads folder in the program location"""
        try:
            # Get program location
            program_dir = Path(__file__).parent
            downloads_folder = program_dir / "downloads"
            
            # Create folder if it doesn't exist
            downloads_folder.mkdir(exist_ok=True)
            
            # Set as output folder
            self.output_folder.set(str(downloads_folder))
            self.save_config()
            
            messagebox.showinfo("Default Folder", 
                              f"Downloads folder set to:\n{downloads_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not set default folder: {str(e)}")
    
    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder.get())
        if folder:
            self.output_folder.set(folder)
            self.save_config()  # Save the newly selected folder
    
    def detect_url_type(self, url):
        """Detects YouTube URL type and returns information about it"""
        # Patterns for different URL types
        patterns = {
            'normal_video': [
                r'^(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})$',
                r'^(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})$'
            ],
            'video_in_playlist': r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})&list=',
            'playlist': r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=',
            'shorts': r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
            'live': r'(?:https?://)?(?:www\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})',
            'channel': r'(?:https?://)?(?:www\.)?youtube\.com/(?:channel|c|user)/',
        }
        
        # Check normal video (without additional parameters)
        for pattern in patterns['normal_video']:
            if re.match(pattern, url):
                return 'normal_video', None
        
        # Check video in playlist
        if re.search(patterns['video_in_playlist'], url):
            return 'video_in_playlist', "⚠️ Video in playlist URL detected.\n\nThis program only downloads individual videos.\n\nPlease use the video URL without the '&list=' parameter:\n\nCorrect example:\nhttps://www.youtube.com/watch?v=VIDEO_ID"
        
        # Check playlist
        if re.search(patterns['playlist'], url):
            return 'playlist', "❌ Playlist URL detected.\n\nThis program does NOT support downloading complete playlists.\n\nPlease copy the URL of an individual video."
        
        # Check shorts
        if re.search(patterns['shorts'], url):
            return 'shorts', "❌ YouTube Shorts URL detected.\n\nThis program does NOT support YouTube Shorts.\n\nPlease use a normal video URL:\nhttps://www.youtube.com/watch?v=VIDEO_ID"
        
        # Check live
        if re.search(patterns['live'], url):
            return 'live', "❌ Live stream URL detected.\n\nThis program does NOT support live streams.\n\nPlease use a normal video URL."
        
        # Check channel
        if re.search(patterns['channel'], url):
            return 'channel', "❌ Channel URL detected.\n\nThis program does NOT support downloading channels.\n\nPlease copy the URL of an individual video."
        
        return 'unknown', "❌ URL not recognized.\n\nPlease use a valid YouTube video URL:\n\n• https://www.youtube.com/watch?v=VIDEO_ID\n• https://youtu.be/VIDEO_ID"
    
    def validate_url(self, url):
        """Validates if the URL is a normal YouTube video"""
        url_type, message = self.detect_url_type(url)
        
        if url_type == 'normal_video':
            return True
        elif url_type == 'video_in_playlist':
            # Show warning but allow to continue
            response = messagebox.askyesno(
                "Playlist URL Detected",
                message + "\n\nDo you want to try downloading only the video (without the playlist)?"
            )
            return response
        else:
            # For other types, show error and don't allow
            if message:
                messagebox.showerror("Unsupported URL", message)
            return False
    
    def analyze_video(self):
        """Analyze video and get available formats"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Detect URL type
        url_type, message = self.detect_url_type(url)
        
        # If video in playlist, clean the URL
        if url_type == 'video_in_playlist':
            # Extract only the video ID without the playlist parameter
            match = re.search(r'watch\?v=([a-zA-Z0-9_-]{11})', url)
            if match:
                video_id = match.group(1)
                url = f"https://www.youtube.com/watch?v={video_id}"
                self.url_var.set(url)  # Update URL in the field
                messagebox.showinfo("URL Cleaned", 
                    "The playlist parameter has been removed.\n\n"
                    "Only the individual video will be downloaded.")
        
        # Validate URL
        if not self.validate_url(url):
            return
        
        self.current_url = url
        
        # Execute analysis in separate thread
        thread = threading.Thread(target=self.fetch_video_formats, args=(url,))
        thread.daemon = True
        thread.start()
    
    def fetch_video_formats(self, url):
        """Get available video formats using yt-dlp"""
        try:
            self.root.after(0, lambda: self.update_status("🔍 Analyzing video and available formats..."))
            
            import yt_dlp
            
            # Configuration to get complete information
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'listformats': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract video information
                title = info.get('title', 'No title')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                
                # Process formats in more detail
                formats = info.get('formats', [])
                video_formats = {}
                audio_formats = []
                
                for f in formats:
                    format_id = f.get('format_id', '')
                    ext = f.get('ext', 'unknown')
                    filesize = f.get('filesize')
                    fps = f.get('fps')
                    vcodec = f.get('vcodec', 'none')
                    acodec = f.get('acodec', 'none')
                    height = f.get('height')
                    width = f.get('width')
                    
                    # Filter video formats (that have video codec and height)
                    if vcodec != 'none' and height and height > 0:
                        quality_key = f"{height}p"
                        
                        if quality_key not in video_formats:
                            video_formats[quality_key] = []
                        
                        size_mb = f"~{filesize // (1024*1024)} MB" if filesize else "Unknown size"
                        
                        video_formats[quality_key].append({
                            'format_id': format_id,
                            'ext': ext,
                            'fps': fps if fps else 'N/A',
                            'size': size_mb,
                            'vcodec': vcodec,
                            'acodec': acodec,
                            'width': width,
                            'height': height,
                            'has_audio': acodec != 'none'
                        })
                    
                    # Filter audio formats
                    elif acodec != 'none' and vcodec == 'none':
                        audio_formats.append({
                            'format_id': format_id,
                            'ext': ext,
                            'acodec': acodec,
                            'size': f"~{filesize // (1024*1024)} MB" if filesize else "Unknown size"
                        })
                
                self.available_formats = video_formats
                self.video_info = {
                    'title': title,
                    'duration': duration,
                    'uploader': uploader,
                    'audio_formats': audio_formats
                }
                
                # Update UI in main thread
                self.root.after(0, lambda: self.show_analysis_results())
                
        except ImportError:
            self.root.after(0, lambda: messagebox.showerror("Error", "yt-dlp is not installed.\nRun: pip install yt-dlp"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error analyzing video: {str(e)}"))
            self.root.after(0, lambda: self.update_status("❌ Error analyzing video"))
    
    def show_analysis_results(self):
        """Show analysis results"""
        if not self.video_info:
            return
        
        # Download and show thumbnail
        self.load_thumbnail()
        
        # Ocultar placeholder
        self.preview_icon.place_forget()
        self.preview_text.place_forget()
        
        # Show video information
        self.video_info_frame.pack(fill="x", pady=(0, 10))
        
        self.video_title_label.configure(text=f"📹 {self.video_info['title']}")
        self.video_title_label.pack(pady=(0, 5))
        
        duration_min = self.video_info['duration'] // 60
        duration_sec = self.video_info['duration'] % 60
        
        self.video_status_label.configure(
            text=f"👤 {self.video_info['uploader']} | ⏱️ {duration_min}:{duration_sec:02d}"
        )
        self.video_status_label.pack()
        
        # Show format analysis
        self.formats_frame.pack(fill="x", pady=(0, 15))
        self.update_formats_display()
        
        # Update quality and format states
        self.check_quality_availability()
        self.check_format_availability()
        
        self.update_status("✅ Video verified - Ready to download")
    
    def load_thumbnail(self):
        """Downloads and displays the video thumbnail"""
        if not self.video_info:
            return
        
        try:
            # Get thumbnail URL from yt-dlp
            import yt_dlp
            url = self.current_url
            
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                
                if thumbnail_url:
                    # Download image
                    response = requests.get(thumbnail_url, timeout=5)
                    if response.status_code == 200:
                        # Convert to PIL image
                        from PIL import Image
                        import io
                        
                        image_data = io.BytesIO(response.content)
                        pil_image = Image.open(image_data)
                        
                        # Resize to fit frame (max 400x180)
                        pil_image.thumbnail((400, 160), Image.Resampling.LANCZOS)
                        
                        # Convert to CTkImage
                        ctk_image = ctk.CTkImage(light_image=pil_image, 
                                                dark_image=pil_image,
                                                size=pil_image.size)
                        
                        # Show in label
                        self.thumbnail_label.configure(image=ctk_image, text="")
                        self.thumbnail_label.image = ctk_image  # Keep reference
        except Exception as e:
            print(f"Could not load thumbnail: {e}")
            # If it fails, keep the placeholder
    
    def update_formats_display(self):
        """Update available formats display"""
        if not self.available_formats:
            return
        
        # Generate analysis text
        analysis_text = ""
        
        # Ordenar por resolución
        sorted_qualities = sorted(self.available_formats.keys(), 
                                key=lambda x: int(x.replace('p', '')), reverse=True)
        
        # Show available resolutions
        analysis_text += "🎬 RESOLUTIONS:\n"
        for quality in sorted_qualities[:6]:  # Show maximum 6
            formats_list = self.available_formats[quality]
            height_num = int(quality.replace('p', ''))
            
            # Emoji by quality
            if height_num >= 2160:
                emoji = "🔥"
            elif height_num >= 1440:
                emoji = "⭐"
            elif height_num >= 1080:
                emoji = "✅"
            elif height_num >= 720:
                emoji = "📺"
            else:
                emoji = "📱"
            
            # Contar formatos
            formats_count = len(formats_list)
            analysis_text += f"  {emoji} {quality} ({formats_count} formats)\n"
        
        if len(sorted_qualities) > 6:
            analysis_text += f"  ... +{len(sorted_qualities)-6} more\n"
        
        # Información adicional
        analysis_text += f"\n📹 FORMATS: "
        all_formats = set()
        for formats_list in self.available_formats.values():
            for fmt in formats_list:
                all_formats.add(fmt['ext'].upper())
        analysis_text += ", ".join(sorted(all_formats))
        
        # Recomendación
        analysis_text += "\n\n💡 TIP: MP4 1080p recommended"
        
        # Actualizar textbox
        self.formats_text.configure(state="normal")
        self.formats_text.delete("1.0", "end")
        self.formats_text.insert("1.0", analysis_text)
        self.formats_text.configure(state="disabled")
    

    
    def update_status(self, message):
        self.status_label.configure(text=message)
        self.root.update()
    
    def update_progress(self, value):
        self.progress_bar.set(value)
        self.root.update()
    
    def start_download(self, is_test=False):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "Invalid YouTube URL")
            return
        
        if not self.available_formats:
            messagebox.showwarning("Warning", "First analyze the video to see available formats")
            return
        
        # Check quality and format availability
        selected_quality = self.video_quality.get()
        selected_format = self.video_format.get()
        
        if selected_quality != "Best available":
            # Use same mapping as in check_quality_availability
            quality_mapping = {
                "4K (2160p)": "2160p",
                "2K (1440p)": "1440p", 
                "1080p": "1080p",
                "720p": "720p",
                "480p": "480p",
                "360p": "360p",
                "240p": "240p",
                "144p": "144p"
            }
            
            quality_key = quality_mapping.get(selected_quality, selected_quality)
            
            if quality_key not in self.available_formats:
                response = messagebox.askyesno(
                    "Quality not available", 
                    f"Quality {selected_quality} is not available for this video.\n\n"
                    f"Do you want to download in the best available quality?"
                )
                if not response:
                    return
                self.video_quality.set("Best available")
        
        # Check format
        format_available = False
        for quality, formats in self.available_formats.items():
            for fmt in formats:
                if fmt['ext'].lower() == selected_format.lower():
                    format_available = True
                    break
            if format_available:
                break
        
        if not format_available:
            response = messagebox.askyesno(
                "Format not available", 
                f"Format {selected_format} is not available for this video.\n\n"
                f"Do you want to download in MP4 (more compatible)?"
            )
            if not response:
                return
            self.video_format.set("mp4")
        
        # Disable button
        self.download_button.configure(state="disabled")
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_video, args=(url, is_test))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url, is_test=False):
        try:
            prefix = "🧪 TEST: " if is_test else ""
            self.update_status(f"{prefix}🚀 Starting download...")
            self.update_progress(0.1)
            
            library = self.download_library.get()
            
            if library == "yt-dlp":
                success = self.download_with_ytdlp_ultimate(url, is_test)
            else:
                success = self.download_with_pytube_ultimate(url, is_test)
            
            if success:
                self.update_status(f"{prefix}✅ Download completed successfully!")
                self.update_progress(1.0)
                
                if is_test:
                    messagebox.showinfo("🧪 Test Successful", "Test download worked correctly!\n\nYou can now download in the quality you want.")
                else:
                    messagebox.showinfo("🎉 Success", "Video downloaded successfully!\n\nYou can find your file in the output folder.")
            else:
                self.update_status(f"{prefix}❌ Download error")
                
        except Exception as e:
            self.update_status(f"{prefix}❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        
        finally:
            self.download_button.configure(state="normal")
    
    def download_with_ytdlp_ultimate(self, url, is_test=False):
        try:
            import yt_dlp
            
            quality = self.video_quality.get()
            format_ext = self.video_format.get()
            
            # Configure SPECIFIC format selector
            if quality == "Best available":
                # Select best available quality in desired format
                format_selector = f"best[ext={format_ext}]/bestvideo[ext={format_ext}]+bestaudio/best"
            else:
                # Map specific qualities
                quality_map = {
                    "4K (2160p)": 2160,
                    "2K (1440p)": 1440,
                    "1080p": 1080,
                    "720p": 720,
                    "480p": 480,
                    "360p": 360
                }
                
                target_height = quality_map.get(quality, 1080)
                
                # VERY specific selector to ensure correct resolution
                format_selector = (
                    f"bestvideo[height={target_height}][ext={format_ext}]+bestaudio/"
                    f"best[height={target_height}][ext={format_ext}]/"
                    f"bestvideo[height={target_height}]+bestaudio/"
                    f"best[height={target_height}]/"
                    f"worst[height>={target_height}][ext={format_ext}]/"
                    f"worst[height>={target_height}]"
                )
            
            # Configure yt-dlp options
            output_template = '%(title)s.%(ext)s'
            if is_test:
                output_template = 'TEST_' + output_template
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(self.output_folder.get(), output_template),
                'noplaylist': True,
                'merge_output_format': format_ext,
                'writeinfojson': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
            }
            
            # Show download information
            self.update_status(f"📥 Downloading: {quality} in {format_ext.upper()} format with yt-dlp...")
            self.update_progress(0.3)
            
            # Crear hook para progreso
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        percent = d.get('_percent_str', '0%').replace('%', '')
                        progress = float(percent) / 100
                        self.root.after(0, lambda: self.update_progress(0.3 + (progress * 0.6)))
                    except:
                        pass
                elif d['status'] == 'finished':
                    self.root.after(0, lambda: self.update_progress(0.9))
            
            ydl_opts['progress_hooks'] = [progress_hook]
            
            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First get info to verify format to be downloaded
                info = ydl.extract_info(url, download=False)
                
                # Show which format was selected
                selected_format = ydl.process_info(info)
                
                # Now download
                ydl.download([url])
            
            self.update_progress(1.0)
            return True
            
        except ImportError:
            messagebox.showerror("Error", "yt-dlp is not installed.\nRun: pip install yt-dlp")
            return False
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Error yt-dlp", f"Error with yt-dlp:\n{error_msg}\n\nTry pytube or verify the URL.")
            return False
    
    def download_with_pytube_ultimate(self, url, is_test=False):
        try:
            from pytube import YouTube
            
            self.update_status("📥 Downloading with pytube...")
            self.update_progress(0.3)
            
            yt = YouTube(url)
            
            quality = self.video_quality.get()
            format_ext = self.video_format.get()
            
            # Map qualities
            quality_map = {
                "4K (2160p)": "2160p",
                "2K (1440p)": "1440p",
                "1080p": "1080p",
                "720p": "720p",
                "480p": "480p",
                "360p": "360p"
            }
            
            if quality == "Best available":
                # Search for best available quality in desired format
                stream = yt.streams.filter(file_extension=format_ext, progressive=True).order_by('resolution').desc().first()
                if not stream:
                    stream = yt.streams.filter(file_extension=format_ext, adaptive=True, only_video=True).order_by('resolution').desc().first()
                if not stream:
                    stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            else:
                resolution = quality_map.get(quality, "1080p")
                
                # Search for specific stream with exact resolution
                stream = yt.streams.filter(res=resolution, file_extension=format_ext, progressive=True).first()
                
                if not stream:
                    # Search for adaptive stream
                    stream = yt.streams.filter(res=resolution, file_extension=format_ext, adaptive=True, only_video=True).first()
                
                if not stream:
                    # Search for any stream with that resolution
                    stream = yt.streams.filter(res=resolution).first()
                
                if not stream:
                    # As last resort, search for closest quality
                    available_streams = yt.streams.filter(file_extension=format_ext).order_by('resolution').desc()
                    stream = available_streams.first()
            
            if not stream:
                messagebox.showerror("Error", f"No stream found for {quality} in {format_ext} format")
                return False
            
            self.update_progress(0.5)
            
            # Show selected stream information
            actual_resolution = getattr(stream, 'resolution', 'Unknown')
            actual_format = getattr(stream, 'mime_type', format_ext)
            
            self.update_status(f"📥 Downloading: {actual_resolution} {actual_format}")
            
            # Download with custom name if test
            output_path = self.output_folder.get()
            filename = None
            if is_test:
                filename = f"TEST_{yt.title}"
            
            stream.download(output_path=output_path, filename=filename)
            
            self.update_progress(0.9)
            return True
            
        except ImportError:
            messagebox.showerror("Error", "pytube is not installed.\nRun: pip install pytube")
            return False
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Error pytube", f"Error with pytube:\n{error_msg}\n\nTry yt-dlp or update pytube.")
            return False
    
    def open_folder(self):
        try:
            output_path = self.output_folder.get()
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")
    
    def run(self):
        print("Showing window...")
        self.root.mainloop()
        print("Application closed")

def main():
    try:
        print("=== Hikari Youtube Video Downloader ===")
        print("Developed by Gary19gts")
        app = HikariYoutubeDownloader()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            messagebox.showerror("Error", f"Error starting application:\n{str(e)}")
        except:
            print("Could not show error window")
        
        input("Press Enter to close...")

if __name__ == "__main__":
    main()