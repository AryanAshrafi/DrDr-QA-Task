import pickle
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

print("Starting script...")

def click_with_retries(driver, by, value, retries=3, wait_time=20):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by, value)))
            element.click()
            return True
        except (StaleElementReferenceException, TimeoutException):
            print(f"Attempt {attempt + 1}/{retries} failed. Retrying...")
            time.sleep(1)
    print(f"Failed to click on the element with {by} = {value} after multiple attempts.")
    return False

service = Service(executable_path="/Users/aryan/DrDr QA-Task/chromedriver")
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://drdr.ir")

    print("Loading cookies...")
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("Cookies file not found. Please log in first.")

    print("Loading local storage...")
    try:
        with open("local_storage.json", "r") as local_file:
            local_storage = json.load(local_file)
            for key, value in local_storage.items():
                driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        print("Local storage loaded successfully.")
    except FileNotFoundError:
        print("Local storage file not found.")

    print("Loading session storage...")
    try:
        with open("session_storage.json", "r") as session_file:
            session_storage = json.load(session_file)
            for key, value in session_storage.items():
                driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}');")
        print("Session storage loaded successfully.")
    except FileNotFoundError:
        print("Session storage file not found.")

    driver.refresh()

    print("Finding the list button...")
    assert click_with_retries(driver, By.CLASS_NAME, "all_expertise_click_class"), "Failed to click the list button."
    print("List button clicked successfully.")

    print("Waiting for the heart section button...")
    assert click_with_retries(driver, By.LINK_TEXT, "قلب و عروق"), "Failed to click the heart section button."
    print("Heart section button clicked successfully.")

    print("Waiting for the doctors list...")
    doctors_list = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mui-1jzqsqy"))
    )
    assert doctors_list, "Doctors list not found."
    print("Doctors list found successfully.")

    print("Getting the first doctor...")
    first_doctor = doctors_list.find_element(By.TAG_NAME, 'section')
    print("Going to doctor's profile")
    first_doctor_link = first_doctor.find_element(By.TAG_NAME, 'a')
    first_doctor_link.click()

    print("Waiting for the reservation button...")
    reservation_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, "//div[contains(@class, 'mui-12pfwui')]//div[contains(@class, 'mui-1jauky')]//div[contains(@class, 'drdr-card-layout-footer-wrapper')]//button"
        ))
    )
    assert reservation_btn, "Reservation button not found."
    # Since there is a bug in process, it's not moving in with one click
    reservation_btn.click()
    time.sleep(3)
    reservation_btn.click()

    print("Waiting for reserve appointment button...")
    reserve_appointment = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@class='appointment-sidebar-container']")
        )).find_element(
            By.XPATH, "//*[@class='drdr-card-layout MuiBox-root mui-1cd7eb5']"
        ).find_element(
            By.XPATH, "//*[@class='drdr-card-layout-body-wrapper MuiBox-root mui-0']"
        ).find_element(
            By.XPATH, "//*[@class='mui-z3p3m5']"
        ).find_element(
            By.TAG_NAME, "button"
        )
    assert reserve_appointment, "Reserve appointment button not found."
    reserve_appointment.click()

    # print("Select user for appointment...")
    # user_selection = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "user-card MuiBox-root mui-5q4zn7"))
    # )
    # user_selection.click()

    print("Fisrtname input filling...")
    firstName_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "firstname"))
    )
    assert firstName_input, "First name input not found."
    firstName_input.send_keys("آرین")

    print("Lastname input filling...")
    lastName_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "lastname"))
    )
    assert lastName_input, "Last name input not found."
    lastName_input.send_keys("اشرفی")

    print("National code input filling...")
    nationalCode_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "national_code"))
    )
    assert nationalCode_input, "National code input not found."
    nationalCode_input.send_keys("1234567890")

    print("Gender selection")
    gender = driver.find_element(
        By.XPATH, "//div[contains(@class, 'MuiBox-root') and contains(@class, 'mui-e3j5cx')]//div[contains(@class, 'drdr-main-inner-container')]//div[contains(@class, 'drdr-content-container')]//div[contains(@class, 'drdr-title-icon-container')]//div[contains(@class, 'title is-disabled') and contains(@class, 'mui-4x7tdu')]"
    )
    assert gender, "Gender selection element not found."
    gender.click()

    print("Submitting information")
    buttonContainer = driver.find_element(
        By.CLASS_NAME, "button-container"
    )
    assert buttonContainer, "Submit button container not found."
    buttonContainer.click()

    print("Next button...")
    next = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@class='appointment-sidebar-container']")
        )).find_element(
            By.XPATH, "//*[@class='drdr-card-layout MuiBox-root mui-1cd7eb5']"
        ).find_element(
            By.XPATH, "//*[@class='drdr-card-layout-body-wrapper MuiBox-root mui-0']"
        ).find_element(
            By.XPATH, "//*[@class='mui-z3p3m5']"
        ).find_element(
            By.TAG_NAME, "button"
        )
    assert next, "Next button not found."
    next.click()

    time.sleep(20)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    print("Browser closed.")
