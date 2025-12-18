'''
The following pair of functions has been implemented to start and stop the Surfshark VPN service using its native 
Linux command-line interface. Since the Surfshark client operates at sudo level and will invariably request the 
administrative password, the solution utilises Pexpect to handle the prompt programmatically, inserting the requisite 
password that has been securely predefined for this purpose.
'''
import pexpect
import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
password = "davidisdumb" # Hardcoded Sudo password

def StartVPN():
    #i = random.randint(0, 140) # Randomly selects a Surfshark server location from the available list
    print("Starting VPN")
    command = "sudo surfshark-vpn attack"
    
    # Spawn the process
    child = pexpect.spawn(command, encoding='utf-8')

    # Expect the password prompt
    child.expect('.*password.*:')
        
    # Send the password
    child.sendline(password)

    #child.expect("press enter for next page")
    #child.sendline('ls -l')
    #child.sendline('ls -l')
    #child.sendline('ls -l')
    #child.sendline('ls -l')
    #child.sendline('ls -l')
    #child.expect("Enter a number to select the location")   
    #child.sendline(str(i))
    time.sleep(1)
    # Expect the  prompt
    child.expect("Enter a number to select the VPN connection type. For default UDP, press ENTER")
    
    child.sendline('ls -l')

    # Capture output until the process completes
    child.expect(pexpect.EOF)
        
    # Print the output
    print(child.before)
    print("---------------------------------------------------------------")
    child.terminate(force=True)

def DownVPN():
    command = "sudo surfshark-vpn down"
    # Spawn the process
    child = pexpect.spawn(command, encoding='utf-8')
    # Expect the password prompt
    child.expect('.*password.*:')       
    # Send the password
    child.sendline(password)
    # Capture output until the process completes
    child.expect(pexpect.EOF)
    # Print the output
    print(child.before)
    child.terminate(force=True)


chrome_options = Options()
chrome_options.add_argument("--headless=new")  # or remove for visible browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Optional: spoof a real user profile
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
chrome_options.add_argument("--enable-javascript")  # Ensure JavaScript is enabled
chrome_options.add_argument("--enable-cookies")  # Ensure cookies are enabled
chrome_options.add_argument("--blink-settings=imagesEnabled=true")  # Ensure images load
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation flags
chrome_options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension

def HTML_get(target,HTML_name):
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
    '''
    Examine the cookie yield. A properly cooperative site should furnish us with approximately 18–20 cookies. 
    Anything markedly below this threshold strongly suggests that we’ve been quietly shown the door by Cloudflare 
    (or similar) and are, regrettably, blocked.
    '''
    number_of_cookies = 0
    html_source = None
    Bot_detect_flag = 0
    while number_of_cookies < 4: 
        
        if Bot_detect_flag > 1:
            DownVPN()
            time.sleep(1)
            StartVPN()
        
        
        driver.get(target)
        time.sleep(random.randint(1, 8))
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
   

