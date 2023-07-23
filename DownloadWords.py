import os
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
import json
import html
import re

def download_file(url, filename, foldername):
    filename = re.sub(r'[^a-zA-ZÀ-ÿ\s]',"", filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open("./" + foldername +"/audio/" + filename+ ".mp3", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def download_Image(url, filename, foldername):
    filename = re.sub(r'[^a-zA-ZÀ-ÿ\s]',"", filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open("./" + foldername +"/images/" + filename+ ".jpg", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")


def decode_html_entities(html_text):
    # Decode HTML entities
    decoded_text = html.unescape(html_text)
    return decoded_text

def parse_html_to_json(html_text):
    # Decode HTML entities
    decoded_text = decode_html_entities(html_text)

    # Parse to JSON
    json_data = {
        "decoded_text": decoded_text
    }

    return json_data
def getLinksToMp3(url):
    burp0_url = url
    burp0_cookies = {"guid": "96e824eb9636323d85a46b2ebbde6aa9b114d16d", "clickpath": "%7C%2Fczech-vocabulary-lists%2Fcomputer", "popin56": "Sun, 30 Jul 2023 17:15:33 GMT", "_gid": "GA1.2.2127057037.1690132533", "_fbp": "fb.1.1690132541654.1181895603", "_gcl_au": "1.1.1391290883.1690132534.1306245254.1690139400.1690139399", "guidmember": "104677", "_ga": "GA1.1.1355945867.1690132533", "_uetsid": "88981340297c11ee8ad5abe92cd5c64c", "_uetvid": "889813f0297c11ee90b261f7dd8c8df4", "_ga_BNNQ3EK1P2": "GS1.2.1690139388.2.1.1690139603.53.0.0", "_ga_58L2BT98MM": "GS1.1.1690139376.2.1.1690139608.48.0.0"}
    burp0_headers = {"Sec-Ch-Ua": "", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    
    #print(response.content)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        mp3_urls = set()  # Using a set to avoid duplicate URLs
        for link in soup.find_all("div", {"id": "vocab_page", 'data-wordlist': True}):
            data_wordlist = link.get("data-wordlist")
            try:
                json_wordlist = json.loads(data_wordlist)
                print(json.dumps(json_wordlist, indent=4))
                items = json_wordlist.get("items", [])
                for item in items:
                    print("CZECH: " + item["target"] + ". ENGLISH: " + item["english"] + ". DOWNLOAD: "+ item["audio"])

                    name_and_link = (item["target"],  item["audio"], item["english"], item["image"])
                    mp3_urls.add(name_and_link)
            except:
                print("that didnt work")
            # result_json = parse_html_to_json(data_wordlist)
            # json_str = json.dumps(result_json, indent=4)
            # print(json_str)
        return mp3_urls
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return None

def main():
    url = sys.argv[1]
    urls = getLinksToMp3(url)
    # 0: CZECH, 1: URL, 2: English, 3: Image
    foldername = url.rsplit('/', 1)[-1]

    if not os.path.exists(foldername):
        os.makedirs(foldername)
    if not os.path.exists("./" + foldername + "/audio"):
        os.makedirs("./" + foldername + "/audio")
    if not os.path.exists("./" + foldername + "/images"):
        os.makedirs("./" + foldername + "/images")
    with open(foldername + "/translations.txt", 'w', encoding="utf-8") as f:
        for i in urls:
            #filestr = "CZECH: " + i[0] + ". ENGLISH: " + i[2] + "\n"
            f.writelines("CZECH: " + i[0] + "\n")
            f.writelines("ENGLISH: " + i[2] + "\n")
            f.writelines("\n")
    for i in urls:
        print()
        download_file(i[1], i[0], foldername)
        print(i[3])
        download_Image(i[3], i[0], foldername)

    #print(urls)
    
if __name__ == "__main__":
    main()