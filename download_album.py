import os
import sys
import time
import timeit
import urllib
from Queue import Queue
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


baseURL = "http://facebook.com/"
username = ""
password = ""
albumLink = ""
albumName = ""
albumUser = ""
max_workers = 8

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            link = self.queue.get()
            fileName = link[::-1].split("/")[0][::-1].split("?")[0]
            urllib.urlretrieve(link, albumName + "/" + fileName)
            self.queue.task_done()

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(sys.argv[0]) + '/chromedriver.exe'):
        print "[chromedriver.exe not found in directory! It must be in this folder and named chromedriver.exe]"
        print "[Download: http://chromedriver.storage.googleapis.com/index.html?path=2.20/ ]"
        raw_input("Press any key to exit...")
    else: 
        print "[Facebook Album Downloader v1]"
        start = timeit.default_timer()

        extensions = webdriver.ChromeOptions()
        # hide images
        prefs = {"profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2}

        extensions.add_experimental_option("prefs", prefs)

        privateAlbum = raw_input("Private Album? (y/n)")

        if privateAlbum is 'y':
            username = raw_input("Email: ")
            password = raw_input("Password: ")

        albumLink = raw_input("Album Link: ")

        browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=extensions)
        browser.implicitly_wait(7)

        if privateAlbum is 'y':
            browser.get(baseURL)

            print "[Logging In]"

            browser.find_element_by_id("email").send_keys(username)
            browser.find_element_by_id("pass").send_keys(password)
            browser.find_element_by_id("loginbutton").click()

        print "[Loading Album]"
        browser.get(albumLink)

        # get album name
        albumName = browser.find_element_by_class_name("fbPhotoAlbumTitle").text

        # create album path
        if not os.path.exists(albumName):
            os.makedirs(albumName)

        queue = Queue()

        for x in range(max_workers):
            worker = DownloadWorker(queue)
            worker.daemon = True
            worker.start()

        print "[Getting Image Links]"

        # scroll to bottom
        previousHeight = 0
        reachedEnd = 0

        while reachedEnd != None:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            currentHeight = browser.execute_script("return document.body.scrollHeight")

            if previousHeight == currentHeight:
                reachedEnd = None


            previousHeight = currentHeight
            time.sleep(0.6)


        linkImages = browser.execute_script("var list = []; Array.prototype.forEach.call(document.querySelectorAll('.uiMediaThumb[ajaxify]:not(.coverWrap)'), function(el) { var src = el.getAttribute('ajaxify'); var key = 'src='; src = src.substr(src.indexOf(key) + key.length); src = unescape(src.substr(0, src.indexOf('&'))); list.push(src) }); return list;")
        totalImages = len(linkImages)

        print "[Found: " + str(len(linkImages)) + "]"

        for fullRes in linkImages:
            queue.put(fullRes)

        print "[Downloading...]"
        queue.join()

        browser.quit()

        stop = timeit.default_timer()
        print "[Time taken: %ss]" % str(stop - start)
        raw_input("Press any key to continue...")
