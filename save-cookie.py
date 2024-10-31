import undetected_chromedriver as uc
import ssl
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from selenium.webdriver.chrome.service import Service

ssl._create_default_https_context = ssl._create_stdlib_context

if __name__ == '__main__':
    mobile = "09146514699"
    code = "736136"

    options = webdriver.ChromeOptions()
    service = Service(executable_path="/Users/aryan/DrDr QA-Task/chromedriver")
    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get('https://drdr.ir')

        browser.find_element(By.CLASS_NAME, 'user-button-container').click()

        browser.find_element(By.ID, "phoneNumber").send_keys(mobile)
        browser.find_element(By.CLASS_NAME, "submit-button-wrapper").click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'MuiInputBase-input'))
        )

        otp_inputs = browser.find_elements(By.CLASS_NAME, 'MuiInputBase-input')

        if len(otp_inputs) < len(code):
            print(f"Not enough OTP input fields found: {len(otp_inputs)} available, {len(code)} required.")
        else:
            for i, digit in enumerate(code):
                otp_inputs[i].send_keys(digit)

        time.sleep(20)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cookies = browser.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))
        
        local_storage = browser.execute_script("return JSON.stringify(window.localStorage);")
        session_storage = browser.execute_script("return JSON.stringify(window.sessionStorage);")

        with open("local_storage.json", "w") as local_file:
            local_file.write(local_storage)

        with open("session_storage.json", "w") as session_file:
            session_file.write(session_storage)

        print("Local and session storage saved.")
        
        browser.quit()