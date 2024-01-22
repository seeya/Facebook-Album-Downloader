Facebook Album Downloader (Windows only)
======

## Dependencies
1. Uses [Python 3](https://www.python.org/download/releases/3/)
2. Uses `selenium chromedriver` - included in the repository
3. More information [here](https://sites.google.com/a/chromium.org/chromedriver/getting-started)
4. [Google Chrome](https://www.google.com/chrome/browser/desktop/) must be installed on your computer
5. Remember to install selenium `pip install selenium`

## Instructions
1. chromedriver should be in your [PATH](http://chromedriver.storage.googleapis.com/index.html?path=2.20/)

## Introduction
1. If the album is private enter your details in the prompt
2. CD into Facebook-Album-Downloader-master
3. Run `python download_album.py`

## Making an .exe
1. Tested with pyinstaller, runnable with an exe.
2. pyinstaller --onefile download_album.py
3. Just make sure chromedriver is in the same directory when you run the exe
