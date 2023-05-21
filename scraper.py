from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
  
def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        '__cflb': '02DiuEcwseaiqqyPC5qrDCss6XuWcthYNpohydfQ6aCFM',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cflb=02DiuEcwseaiqqyPC5qrDCss6XuWcthYNpohydfQ6aCFM',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'MnlSdEc0',
    }

    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    
    downloadLink = downloadSoup.a["href"]

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

print("STEP 1: Open Chrome browser")
driver = webdriver.Chrome()
driver.get("https://www.tiktok.com/@bigdbsun")

time.sleep(1)

scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

print("STEP 2: Scrolling page")
while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

print(f"STEP 3: Time to download {len(videos)} videos")
print(len(videos))
for index, video in enumerate(videos):
    downloadVideo(video.a["href"], index)
    time.sleep(10)
