from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
geckodriver_path = '/usr/local/bin/geckodriver'
login_url = 'login_url'
dashboard_url = 'target_page_url'
email = 'email'
password = 'pass'
screenshot_path = '/path/to/screenshot.png'

# Setup Firefox options
options = Options()
options.headless = True

print("Initializing Firefox driver...")
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

try:
    print("Navigating to login page...")
    driver.get(login_url)

    wait = WebDriverWait(driver, 10)
    
    # Wait for the body element to be present
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Focus on the email field
    print("Focusing on email field...")
    body.send_keys(Keys.TAB)
    time.sleep(1) 

    # Enter the email
    print("Entering email...")
    body.send_keys(email)
    time.sleep(1)

    # Focus on the password field
    print("Focusing on password field...")
    body.send_keys(Keys.TAB)
    time.sleep(1)

    # Enter the password
    print("Entering password...")
    body.send_keys(password)

    body.send_keys(Keys.TAB)
    time.sleep(1)
    body.send_keys(Keys.RETURN)

    # Wait for the login process to complete and redirect to dashboard
    print("Waiting for login process to complete...")
    wait.until(EC.url_to_be(dashboard_url))

    print("Navigating to dashboard page...")
    driver.get(dashboard_url)

    # optional for those who have 4k

    # print("Setting browser window size to 4K resolution...")
    # driver.set_window_size(3840, 2160)

    print("Waiting for dashboard to fully load...")
    time.sleep(5)

    print(f"Taking a full-page screenshot and saving to {screenshot_path}...")
    driver.save_screenshot(screenshot_path)
    print(f'Screenshot saved successfully to {screenshot_path}')

finally:
    print("Closing the browser...")
    driver.quit()
    print("Browser closed.")
