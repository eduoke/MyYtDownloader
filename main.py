import ttkbootstrap as ttk
from controllers import YouTubeController

def main():
    root = ttk.Window(themename="superhero") # Use my custom theme `superhero`
    app = YouTubeController(root)
    root.mainloop()

if __name__ == "__main__":
    main()