import os
import sys
import time
import requests
import webbrowser
import tempfile
from colorama import Fore, Style
from Static.Values import StaticValues
import re
import urllib
import json
from bs4 import BeautifulSoup
import hashlib
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium_stealth
import zipfile
from tqdm import tqdm
import shutil

class StaticMethods:
    @staticmethod
    def get_proxies():
        with open('proxies.txt', 'w') as f:
            pass

        response = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies')
        
        if response.status_code == 200:
            with open('proxies.txt', 'a') as f:
                proxies = response.text.strip().split('\n')
                for proxy in proxies:
                    f.write(proxy.strip() + '\n')
        return 1

    @staticmethod
    def is_first_run():
        file_path = os.path.join(tempfile.gettempdir(), 'TtkReporter.txt')
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                file.write("Don't Worry, this isn't a virus, just a check to see if it's your first time. :)")
            print(f"{StaticValues.INFO}First Time Detected. Welcome! (This won't appear anymore){Style.RESET_ALL}")
            webbrowser.open("https://discord.gg/nAa5PyxubF")

    @staticmethod
    def show_credits():
        print(f"{StaticValues.INFO}{Fore.BLUE}Provided to you by {Fore.CYAN}Sneezedip.{Style.RESET_ALL}")
        print(f"{StaticValues.INFO}{Fore.BLUE}Join Our Discord For More Tools! {Fore.GREEN}"
              f"https://discord.gg/nAa5PyxubF{Style.RESET_ALL}")

    @staticmethod   
    def get_match(match, url):
        format = re.search(rf'{match}', url)
        if format:
            format_x = format.group(1)
            return urllib.parse.unquote(format_x)

    @staticmethod
    def _solve_name(user):
        if "https" in user and "@" in user:
            return user
        elif not "https" in user and "@" in user:
            return f"https://www.tiktok.com/{user}"
        elif not "https" in user and not "@" in user:
            return f"https://www.tiktok.com/@{user}"

    @staticmethod
    def get_userData(user, infotype):
        # === VERSION 2025 FONCTIONNELLE – SELENIUM STEALTH + AUTO DRIVER ===
        url = StaticMethods._solve_name(user)
        print(f"{StaticValues.WAITING}Récupération des données TikTok (furtif)...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")
        selenium_stealth.stealth(driver,
            languages=["fr-FR", "fr", "en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        try:
            driver.get(url)
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            script = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})

            if script and script.string:
                data = json.loads(script.string)
                try:
                    value = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"][infotype]
                    driver.quit()
                    return value
                except:
                    driver.quit()
                    return "Invalid Profile"
            else:
                driver.quit()
                return "Invalid Profile"
        except:
            driver.quit()
            return "Invalid Profile"

    @staticmethod
    def _getpayload(timestamp, useragent, deviceID, odinId, victim_data, report_type):
        return {
            "WebIdLastTime": timestamp,
            "aid": 1988,
            "app_language": "en",
            "app_name": "tiktok_web",
            "r_language": "en-US",
            "browser_name": "Mozilla",
            "browser_online": True,
            "browser_platform": "Win32",
            "browser_version": useragent,
            "channel": "tiktok_web",
            "cookie_enabled": True,
            "current_region": "PT",
            "data_collection_enabled": True,
            "device_id": deviceID,
            "device_platform": "web_pc",
            "focus_state": True,
            "from_page": "user",
            "history_len": 2,
            "is_fullscreen": False,
            "is_page_visible": True,
            "lang": "en",
            "nickname": victim_data["nickname"],
            "object_id": victim_data["id"],
            "odinId": odinId,
            "os": "windows",
            "owner_id": victim_data["id"],
            "priority_region": "",
            "reason": report_type,
            "referer": "",
            "region": "PT",
            "report_type": "user",
            "screen_height": 1080,
            "screen_width": 1920,
            "secUid": victim_data["secUid"],
            "target": victim_data["id"],
            "tz_name": "Atlantic/Azores",
            "user_is_login": False,
            "webcast_language": "en",
        }

    @staticmethod
    def download(download_url, destination='.'):
        print(f'{StaticValues.INFO}Downloading new version, please wait...{Style.RESET_ALL}')
        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        zip_path = os.path.join(destination, "downloaded_file.zip")

        with open(zip_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                      desc=f"{StaticValues.WAITING}Downloading New Version {Style.RESET_ALL}") as pbar:
                for data in response.iter_content(1024):
                    file.write(data)
                    pbar.update(len(data))

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            total_files = len(zip_ref.infolist())
            with tqdm(total=total_files, unit='file',
                      desc=f"{StaticValues.WAITING}Extracting New Version{Style.RESET_ALL}") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, destination)
                    pbar.update(1)
        os.remove(zip_path)

        if 'Sneezedip' in download_url:
            with os.scandir('Tiktok-Reporter-main') as entries:
                for entry in entries:
                    if entry.is_dir():
                        with os.scandir(entry) as entries_folder:
                            for entry_folder in entries_folder:
                                try:
                                    os.replace(f"Tiktok-Reporter-main/{entry.name}/{entry_folder.name}",
                                               f"./{entry.name}/{entry_folder.name}")
                                except Exception as e:
                                    print(e)
                    if entry.is_file():
                        try:
                            os.replace(f"Tiktok-Reporter-main/{entry.name}", f"./{entry.name}")
                        except Exception as e:
                            print(e)
            shutil.rmtree("Tiktok-Reporter-main")
        print(f'{StaticValues.SUCCESS}{Fore.WHITE}New Version Downloaded and Extracted Successfully!{Style.RESET_ALL}')
        print(f'{StaticValues.WARNING}{Fore.WHITE}Please Restart the program!{Style.RESET_ALL}')

    @staticmethod
    def check_version(current_version):
        response = requests.get("https://raw.githubusercontent.com/Sneezedip/Tiktok-Reporter/main/VERSION")
        if response.text.strip() != current_version:
            while True:
                u = input(f"{StaticValues.WARNING}NEW VERSION FOUND. Want to update? (y/n){Style.RESET_ALL}").lower()
                if u == "y":
                    StaticMethods.download("https://codeload.github.com/Sneezedip/Tiktok-Reporter/zip/refs/heads/main", "./")
                    sys.exit(1)
                elif u == "n":
                    return