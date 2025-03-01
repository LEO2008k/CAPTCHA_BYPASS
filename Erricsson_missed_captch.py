import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Settings for opening an incognito tab and setting user agent for a mobile device
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36")

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "Ericsson_Vulnerability_by_Levko_Kravchuk.pdf")


# Setting screen size for mobile device
mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Creating webdriver instance with settings
driver = webdriver.Chrome(options=chrome_options)

try:
    # Opening the page
    url = "https://jobs.ericsson.com/careers?query=engineering"
    driver.get(url)

    # Delay after page load
    time.sleep(3)

    # Clicking on "Accept necessary only" button to dismiss popup
    try:
        accept_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonNecessary")
        accept_button.click()
        print("Clicked on 'Accept necessary only' button to dismiss popup.")
    except Exception as e:
        print("Error clicking on 'Accept necessary only' button:", e)

    # Delay after click
    time.sleep(2)

    # Clicking on "Select file" button
    try:
        select_file_button = driver.find_element(By.XPATH, "//a[contains(@class, 'browse-button') and contains(text(), 'Select file')]")
        select_file_button.click()
        print("Clicked on 'Select file' button.")
    except Exception as e:
        print("Error clicking on 'Select file' button:", e)

    # Delay after file select button click
    time.sleep(5)

    # Uploading file "empty.pdf" using JavaScript
    try:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        print("File uploaded successfully.")
    except Exception as e:
        print("Error uploading file:", e)

    # Waiting for file upload window to disappear
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element((By.XPATH, "//input[@type='file']")))
        print("File upload window disappeared.")
    except TimeoutException:
        print("Timeout. File upload window did not disappear.")

    # Waiting for "Agree" button to appear before clicking
    try:
        agree_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Agree']")))
        agree_button.click()
        print("Clicked on 'Agree' button after file upload.")
    except TimeoutException:
        print("Timeout. 'Agree' button did not become clickable.")
    
    # Waiting for error message
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Unexpected token') or contains(text(), 'Resume file too large')]"))
        )
        print("Error parsing resume:", error_message.text)
    except TimeoutException:
        print("Timeout. Error message did not appear.")

    # Checking for the presence of relevant jobs message
    try:
        relevant_jobs_message = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='position-count-message' and @role='status']"))
        )
        print("Found message about relevant jobs:", relevant_jobs_message.text)
    except TimeoutException:
        print("Timeout. Message about relevant jobs did not appear.")
    except Exception as e:
        print("Error waiting for or not finding message about relevant jobs:", e)
finally:
    # Closing the webdriver
    driver.quit()

