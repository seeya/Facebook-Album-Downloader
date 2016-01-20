import os
import sys
import time
import timeit
import requests
from PIL import Image
from Queue import Queue
from threading import Thread
from StringIO import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

cookies = {}
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
            r = requests.get('https://www.facebook.com/photo/download/?fbid=' + link,cookies=cookies)
            i = Image.open(StringIO(r.content))
            i.save(albumName + "/" + link + '.jpg')      
            self.queue.task_done()

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(sys.argv[0]) + '/chromedriver.exe'):
        print "[chromedriver.exe not found in directory! It must be in this folder and named chromedriver.exe]"
        print "[Download: http://chromedriver.storage.googleapis.com/index.html?path=2.20/ ]"
        raw_input("Press any key to exit...")
    else: 
        print "[Facebook Album Downloader v1.1]"
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
            all_cookies = browser.get_cookies()

            for s_cookie in all_cookies:
                cookies[s_cookie["name"]]=s_cookie["value"]

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


        linkImages = browser.execute_script("list = []; Array.prototype.forEach.call(document.querySelectorAll('.uiMediaThumb'), function(el) { var src = el.getAttribute('id'); if(src && src.indexOf('pic_') > -1) list.push(src.split('_')[1]); }); return list;")
        totalImages = len(linkImages)

        print "[Found: " + str(len(linkImages)) + "]"

        for fullRes in linkImages:
            queue.put(fullRes)

        browser.quit()

        print "[Downloading...]"
        queue.join()

        stop = timeit.default_timer()
        print "[Time taken: %ss]" % str(stop - start)
        raw_input("Press any key to continue...")
