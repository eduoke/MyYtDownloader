import ttkbootstrap as ttk
from .controllers import YouTubeController

def main():
    root = ttk.Window()
    app = YouTubeController(root)
    root.mainloop()

if __name__ == "__main__":
    main()