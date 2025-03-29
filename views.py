import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.themes import user_themes
from typing import Callable


# Register the custom theme
theme_path = os.path.join(os.path.dirname(__file__), "themes", "superhero.json")
if os.path.exists(theme_path):
    user_themes.load_themes(theme_path)
    

class YouTubeView:
    """View: Handles UI elements and user interaction"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # Create style
        self.style = ttk.Style("darkly")
        
        # Variables
        self.url_var = tk.StringVar()
        self.dir_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="highest")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Create widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="YouTube Video Downloader", 
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # URL Entry Frame
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=X, pady=10)
        
        url_label = ttk.Label(url_frame, text="Video URL:", width=10)
        url_label.pack(side=LEFT, padx=(0, 10))
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        self.fetch_btn = ttk.Button(
            url_frame, 
            text="Fetch Video", 
            style="info.TButton"
        )
        self.fetch_btn.pack(side=LEFT)
        
        # Video info frame
        self.info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding=10)
        self.info_frame.pack(fill=X, pady=10)
        
        self.title_label = ttk.Label(self.info_frame, text="", wraplength=750)
        self.title_label.pack(fill=X, pady=5)
        
        self.author_label = ttk.Label(self.info_frame, text="")
        self.author_label.pack(fill=X, pady=5)
        
        self.length_label = ttk.Label(self.info_frame, text="")
        self.length_label.pack(fill=X, pady=5)
        
        # Download options frame
        self.download_frame = ttk.LabelFrame(main_frame, text="Download Options", padding=10)
        self.download_frame.pack(fill=X, pady=10)
        
        # Quality selection
        quality_frame = ttk.Frame(self.download_frame)
        quality_frame.pack(fill=X, pady=5)
        
        quality_label = ttk.Label(quality_frame, text="Quality:", width=10)
        quality_label.pack(side=LEFT, padx=(0, 10))
        
        quality_combo = ttk.Combobox(
            quality_frame, 
            textvariable=self.quality_var,
            values=["highest", "lowest", "audio_only"],
            state="readonly",
            width=15
        )
        quality_combo.pack(side=LEFT)
        
        # Output directory selection
        dir_frame = ttk.Frame(self.download_frame)
        dir_frame.pack(fill=X, pady=5)
        
        dir_label = ttk.Label(dir_frame, text="Save to:", width=10)
        dir_label.pack(side=LEFT, padx=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=50)
        self.dir_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        self.browse_btn = ttk.Button(
            dir_frame, 
            text="Browse", 
            style="secondary.TButton"
        )
        self.browse_btn.pack(side=LEFT)
        
        # Download button
        self.download_btn = ttk.Button(
            self.download_frame, 
            text="Download",
            style="success.TButton",
            state=DISABLED
        )
        self.download_btn.pack(pady=10)
        
        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            variable=self.progress_var,
            maximum=100,
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill=X, expand=YES)
        
        status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        status_label.pack(pady=5)
    
    def set_fetch_action(self, callback: Callable) -> None:
        """Set action for fetch button"""
        self.fetch_btn.config(command=callback)
    
    def set_browse_action(self, callback: Callable) -> None:
        """Set action for browse button"""
        self.browse_btn.config(command=callback)
    
    def set_download_action(self, callback: Callable) -> None:
        """Set action for download button"""
        self.download_btn.config(command=callback)
    
    def set_quality_change_action(self, callback: Callable) -> None:
        """Set action for quality selection"""
        self.quality_var.trace_add("write", lambda *args: callback(self.quality_var.get()))
    
    def get_url(self) -> str:
        """Get URL from entry"""
        return self.url_var.get().strip()
    
    def get_dir(self) -> str:
        """Get directory from entry"""
        return self.dir_var.get()
    
    def get_quality(self) -> str:
        """Get selected quality"""
        return self.quality_var.get()
    
    def set_dir(self, directory: str) -> None:
        """Set directory value"""
        self.dir_var.set(directory)
    
    def update_video_info(self, title: str, author: str, duration: str) -> None:
        """Update video information display"""
        self.title_label.config(text=f"Title: {title}")
        self.author_label.config(text=f"Author: {author}")
        self.length_label.config(text=f"Length: {duration}")
    
    def update_progress(self, progress: float) -> None:
        """Update progress bar"""
        self.progress_var.set(progress)
    
    def update_status(self, status: str) -> None:
        """Update status text"""
        self.status_var.set(status)
    
    def enable_download(self, enable: bool) -> None:
        """Enable or disable download button"""
        self.download_btn.config(state=NORMAL if enable else DISABLED)
    
    def show_error(self, message: str) -> None:
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message: str) -> None:
        """Show success message"""
        messagebox.showinfo("Success", message)
    
    def show_directory_dialog(self) -> str:
        """Show directory selection dialog"""
        return filedialog.askdirectory()