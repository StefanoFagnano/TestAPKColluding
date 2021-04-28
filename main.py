import os, requests
import time
from pathlib import Path
from selenium import webdriver
from pathlib import Path

from selenium.common.exceptions import ElementNotInteractableException

TEST_APK_FOLDER = '/Users/stefanofagnano/PycharmProjects/TestAPKColluding/apk_trusted/'
URL = 'http://192.168.1.23/upload_apk.html'

INJECTIONS = {'injection':'code':'2', 'folder': 'imei', 'url': 'http://192.168.1.23/upload_apk.html'], []}


def get_project_root() -> Path:
    return Path(__file__).parent.parent

def create_folder(folder_name):
    APP_ROOT = get_project_root()
    target_decompiled = os.path.join(APP_ROOT, folder_name)

    if not os.path.isdir(target_decompiled):
        os.mkdir(target_decompiled)
    folder = target_decompiled+'/'
    return folder

def init_driver(folder):
    pathch = '/usr/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    download_folder = create_folder(folder)
    print(download_folder)
    prefs = {'download.default_directory': download_folder}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("download.default_directory=" + download_folder)
    driver = webdriver.Chrome(pathch, options=options)

    return driver


def send_request(url, APKfile, injection, client, folder):
    driver = init_driver(folder)
    driver.get(url)

    file = driver.find_element_by_id('file')
    file.send_keys(TEST_APK_FOLDER+APKfile)
    if injection == 2:
        driver.find_element_by_xpath("//select[@name='injection']/option[text()='IMEI']").click()
    if injection == 3:
        driver.find_element_by_xpath("//select[@name='injection']/option[text()='PHONE']").click()
    if 'client' in client:
        driver.find_element_by_id('client-checker').click()
    driver.find_element_by_id('sub-btn').click()
    time.sleep(20)
    try:
        if not driver.find_element_by_id('first-dwn').is_displayed():
            print('error')
        else:
            driver.find_element_by_id('first-dwn').click()
    except ElementNotInteractableException:
        print("THis application isn't appropriated")

    time.sleep(5)
    driver.refresh()


    # with open(TEST_APK_FOLDER+'/'+file, 'rb') as f:
    #     r = requests.post(url, data=detail_injection, files={file: f})
    # print(r.text)


def test():
    list_apk = os.listdir(TEST_APK_FOLDER)  # dir is your directory path
    i = 0
    for file in list_apk:
        print(file+'APP NUMBER: '+str(i))
        send_request(URL, file, 2, 'client', 'Client')
        i = i+1




if __name__ == '__main__':
    test()
