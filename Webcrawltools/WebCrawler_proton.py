#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pexpect
import sys
import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time


def StartVPN():
    country_code = ["AR","AU","AT","BE","BR","CA","HR","CZ","DK","FL","FR","GE","DE","GR","HK","GT","HN","HU","IS","ID","IN","IE","IT","JP","LT","LU","MY","MX","NL","NZ","NO","PL","SG","ES","SE","CH","UK","US"]
    dice = random.randint(0, len(country_code))
    print(country_code[dice])
    result = subprocess.run(['protonvpn','-v' ,'connect', '--country' ,country_code[dice]], capture_output=True, text=True)
    print(result.stdout)

def DownVPN():
    print("DownVPN")
    result = subprocess.run(['protonvpn', 'disconnect'], capture_output=True, text=True)
    print(result.stdout)


chrome_options = Options()
chrome_options.add_argument("--headless=new")  # or remove for visible browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")   # very important for docker / low /dev/shm
chrome_options.add_argument("--disable-gpu")             # often helps stability

# Optional: spoof a real user profile
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
chrome_options.add_argument("--enable-javascript")  # Ensure JavaScript is enabled
chrome_options.add_argument("--enable-cookies")  # Ensure cookies are enabled
chrome_options.add_argument("--blink-settings=imagesEnabled=true")  # Ensure images load
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation flags
chrome_options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension



def HTML_get(target,HTML_name):

    
    '''
    Examine the cookie yield. A properly cooperative site should furnish us with approximately 18–20 cookies. 
    Anything markedly below this threshold strongly suggests that we’ve been quietly shown the door by Cloudflare 
    (or similar) and are, regrettably, blocked.
    '''
    
    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # === APPLY STEALTH ===
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",           # or "NVIDIA Corporation"
            renderer="Intel Iris OpenGL Engine", # matches real devices
            fix_hairline=True,                   # fixes 1px hairline bug in headless
            hide_webdriver=True,                 # sets navigator.webdriver = undefined
            hide_automation=True,                # removes AutomationControlled blink feature
            exclude_switches_to_hide=["enable-automation", "enable-logging"],
            exclude_cdc=True,                    # removes $cdc_ variables
        )
    number_of_cookies = 0
    html_source = None
    Bot_detect_flag = 0
    while number_of_cookies < 4: 

        if Bot_detect_flag > 1:
            if Bot_detect_flag > 8:
                DownVPN()
                time.sleep(random.randint(30, 60))
            try:
                DownVPN()
                time.sleep(1)
                StartVPN()
                time.sleep(1)
            except Exception as exc:
                DownVPN()

        driver.get(target)
        time.sleep(random.randint(1, 5))
        html_source = driver.page_source
        cookies = driver.get_cookies()
        number_of_cookies = len(cookies)

        if number_of_cookies > 4:
            print(f"Cookies captured: {len(cookies)}")
            Bot_detect_flag = 0
            # Save to file
            with open(HTML_name, "w", encoding="utf-8") as f:
                f.write(html_source)
        else:
            Bot_detect_flag = Bot_detect_flag + 1
            print("Bot was detected !!! \n 有內鬼終止交易 !!!")
    
    
    driver.quit()
    return html_source

