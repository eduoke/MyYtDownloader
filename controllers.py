import os
import threading 

from .models import YouTubeModel
from .views import YouTubeView


class YouTubeController:
    """Controller: Connects model and view, handles user actions"""
    
    def __init__(self, root):
        # Create model and view
        self.model = YouTubeModel()
        self.view = YouTubeView(root)
        
        # Initialize view with model data
        self.view.set_dir(self.model.download_path)
        self.view.update_status(self.model.status)
        
        # Register model change observer
        self.model.register_observer(self.update_view)
        
        # Connect view actions to controller methods
        self.view.set_fetch_action(self.fetch_video)
        self.view.set_browse_action(self.browse_directory)
        self.view.set_download_action(self.download_video)
        self.view.set_quality_change_action(self.change_quality)
    
    def update_view(self) -> None:
        """Update view with model data"""
        # Update video info
        video_info = self.model.get_video_info()
        self.view.update_video_info(
            video_info["title"], 
            video_info["author"], 
            video_info["duration"]
        )
        
        # Update status and progress
        self.view.update_status(self.model.status)
        self.view.update_progress(self.model.download_progress)
        
        # Enable/disable download button
        self.view.enable_download(video_info["available"])
    
    def fetch_video(self) -> None:
        """Fetch video information"""
        url = self.view.get_url()
        if not url:
            self.view.show_error("Please enter a YouTube URL")
            return
        
        # Clear UI before fetching
        self.view.update_video_info("", "", "")
        self.view.enable_download(False)
        self.view.update_status("Fetching video info...")
        
        # Use a thread to avoid freezing UI
        threading.Thread(
            target=self._fetch_video_thread,
            args=(url,),
            daemon=True
        ).start()
    
    def _fetch_video_thread(self, url: str) -> None:
        """Thread function for fetching video"""
        success, error = self.model.set_url(url)
        if not success:
            # Use root.after to update UI from thread
            self.view.root.after(0, lambda: self.view.show_error(f"Could not fetch video info: {error}"))
    
    def browse_directory(self) -> None:
        """Browse for download directory"""
        directory = self.view.show_directory_dialog()
        if directory:
            self.model.set_download_path(directory)
            self.view.set_dir(directory)
    
    def change_quality(self, quality: str) -> None:
        """Change download quality"""
        self.model.set_quality(quality)
    
    def download_video(self) -> None:
        """Start video download"""
        output_path = self.view.get_dir()
        
        if not os.path.isdir(output_path):
            self.view.show_error("Please select a valid directory")
            return
        
        # Disable download button during download
        self.view.enable_download(False)
        
        # Use a thread to avoid freezing UI
        threading.Thread(
            target=self._download_video_thread,
            daemon=True
        ).start()
    
    def _download_video_thread(self) -> None:
        """Thread function for downloading video"""
        success, result = self.model.download_video()
        
        if success:
            # Show success message in main thread
            self.view.root.after(0, lambda: self.view.show_success(
                f"Video downloaded successfully!\n\nSaved to: {result}"
            ))
        else:
            # Show error message in main thread
            self.view.root.after(0, lambda: self.view.show_error(f"Download failed: {result}"))
        
        # Re-enable download button in main thread
        self.view.root.after(0, lambda: self.view.enable_download(True))
