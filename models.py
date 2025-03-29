import tkinter as tk 
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pytube import YouTube
import threading 
import os 
import re 
from typing import Callable, Dict, List, Optional, Tuple 


class YoutubeModel:
    """
      Model: Handles data and business logic
    """
    
    def __init__(self):
        self.yt: Optional[Youtube] = None 
        self.download_path: str = os.path.join(os.path.expanduser("~"), "Downloads")
        self.quality: str = "highest"
        self.download_progress: float = 0
        self.status: str = "Ready"
        self.observers: List[Callable] = []
        
    def register_observer(self, callback: Callable) -> None:
        """
        Register an observer to notify when model changes
        """
        self.observers.append(callback) 
        
    def notify_observers(self) -> None:
        """Notify all observers of model changes"""
        for callback in self.observers:
            callback()
    
    def set_url(self, url: str) -> Tuple[bool, str]:
        """Set YouTube URL and fetch video information"""
        try:
            self.yt = YouTube(url)
            self.yt.register_on_progress_callback(self._on_progress_callback)
            self.status = "Video info fetched successfully"
            self.notify_observers()
            return True, ""
        except Exception as e:
            self.status = f"Error: {str(e)}"
            self.notify_observers()
            return False, str(e) 
        
    def set_download_path(self, path: str) -> None:
        """Set download path"""
        self.download_path = path
        self.notify_observers()
        
    def set_quality(self, quality: str) -> None:
        """Set download quality"""
        self.quality = quality
        self.notify_observers()
        
    def get_video_info(self) -> Dict:
        """Get information about the video"""
        if not self.yt:
            return {
                "title": "",
                "author": "",
                "duration": "",
                "available": False
            }
        
        # Format duration
        duration_seconds = self.yt.length
        minutes, seconds = divmod(duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = f"{minutes}:{seconds:02d}"
        
        return {
            "title": self.yt.title,
            "author": self.yt.author,
            "duration": duration_str,
            "available": True
        }
        
    def download_video(self) -> Tuple[bool, str]:
        """Download the video with specified quality and path"""
        if not self.yt:
            return False, "No video selected"
        
        try:
            # Reset progress
            self.download_progress = 0
            self.status = "Starting download..."
            self.notify_observers()
            
            # Get the stream based on quality selection
            if self.quality == "highest":
                stream = self.yt.streams.get_highest_resolution()
            elif self.quality == "lowest":
                stream = self.yt.streams.get_lowest_resolution()
            elif self.quality == "audio_only":
                stream = self.yt.streams.get_audio_only()
            else:
                stream = self.yt.streams.get_highest_resolution()
            
            # Clean filename
            filename = re.sub(r'[^\w\s-]', '', self.yt.title)
            filename = re.sub(r'[-\s]+', '-', filename).strip('-_')
            
            # Download the file
            self.status = "Download started..."
            self.notify_observers()
            
            output_file = stream.download(output_path=self.download_path, filename=filename)
            
            self.status = "Download complete!"
            self.download_progress = 100
            self.notify_observers()
            
            return True, output_file
            
        except Exception as e:
            self.status = f"Download failed: {str(e)}"
            self.notify_observers()
            return False, str(e)
        
    def _on_progress_callback(self, stream, chunk, bytes_remaining):
        """Callback for download progress updates"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        self.download_progress = percentage
        self.status = f"Downloading: {percentage:.1f}%"
        self.notify_observers()