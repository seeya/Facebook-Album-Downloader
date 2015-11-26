Facebook album downloader
Uses selenium chromedriver

Instructions
- Uses python 2.7
- Chrome must be installed on your computer
- chromedriver should be in your PATH  (http://chromedriver.storage.googleapis.com/index.html?path=2.20/)
- Remember to install selenium (pip install selenium)

Downloading Album
- If the album is private enter your details in the prompt
- python download_album.py


Making an Exe
- Tested with pyinstaller, runnable with an exe.
- pyinstaller --onefile download_album.py
- Just make sure chromedriver is in the same directory when you run the exe
