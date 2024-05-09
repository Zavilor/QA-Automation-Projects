import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_directory = os.getcwd()
logs_directory = os.path.join(current_directory, "..", "Logs")

if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

log_file_path = os.path.join(logs_directory, "selenium_log.txt")
log_file = open(log_file_path, "w")

sys.stdout = log_file
sys.stderr = log_file

# Locators
LOGIN_LINK = (By.LINK_TEXT, "Log in")
LOGOUT_LINK = (By.ID, "logout2")
SIGNUP_LINK = (By.LINK_TEXT, "Sign up")
USERNAME_INPUT = (By.ID, "loginusername")
PASSWORD_INPUT = (By.ID, "loginpassword")
LOGIN_BUTTON = (By.XPATH, '//button[contains(text(), "Log in")]')
SIGNUP_BUTTON = (By.XPATH, '//button[contains(text(), "Sign up")]')
WELCOME_MESSAGE = (By.ID, "nameofuser")

# Valid credentials
VALID_USERNAME = "username"
VALID_PASSWORD = "password"

# Invalid credentials
INVALID_CREDENTIALS = "invaaaaaaalid"

# Setting up the browser
driver = webdriver.Chrome()

def handle_alert(expected_message):
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    actual_message = alert.text
    alert.accept()  # Close alert
    return actual_message == expected_message
def login_tests():

    try:
        # Test 1: Check if the given valid credentials work
        driver.get("https://www.demoblaze.com/")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_LINK))
        login_button.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(USERNAME_INPUT)).send_keys(VALID_USERNAME)
        driver.find_element(*PASSWORD_INPUT).send_keys(VALID_PASSWORD)
        driver.find_element(*LOGIN_BUTTON).click()
        welcome_message = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(WELCOME_MESSAGE))

        if welcome_message.text == "Welcome username":
            print("Valid credentials test passed")
        else:
            print("Valid credentials test failed")

        # Test 2: Log out
        logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGOUT_LINK))
        logout_button.click()

        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(LOGOUT_LINK))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_LINK))

        if login_button.is_displayed():
            print("Log out test passed")
        else:
            print("Log out test passed")

        # Test 3: Check if the given wrong credentials work
        driver.get("https://www.demoblaze.com/")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_LINK))
        login_button.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(USERNAME_INPUT)).send_keys(INVALID_CREDENTIALS)
        driver.find_element(*PASSWORD_INPUT).send_keys(INVALID_CREDENTIALS)
        driver.find_element(*LOGIN_BUTTON).click()

        if handle_alert("User does not exist."):
            print("Wrong credentials test passed")
        else:
            print("Wrong credentials test failed")

        # Test 4: Check for empty credentials
        driver.get("https://www.demoblaze.com/")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_LINK))
        login_button.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGIN_BUTTON)).click()

        if handle_alert("Please fill out Username and Password."):
            print("Empty test credentials passed")
        else:
            print("Empty credentials test failed")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        # time.sleep(5)
        driver.quit()

def sign_in_tests():

    def generate_unique_username():
        # Create an username
        prefix = "user"
        unique_value = str(int(time.time()))
        return f"{prefix}_{unique_value}"

    try:
        # Test 1: Correct sign-in flow
        username = generate_unique_username()
        driver.get("https://www.demoblaze.com/")
        signup_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SIGNUP_LINK))
        signup_button.click()

        username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-username")))
        username_input.send_keys(username)
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-password")))
        password_input.send_keys("newPassword")
        driver.find_element(*SIGNUP_BUTTON).click()
        print("Mi username es: " + username)

        if handle_alert("Sign up successful."):
            print("Sign up flow test passed")
        else:
            print("Sign up flow test failed")

        # Test 2: Field validation
        driver.get("https://www.demoblaze.com/")
        signup_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SIGNUP_LINK))
        signup_button.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SIGNUP_BUTTON)).click()

        if handle_alert("Please fill out Username and Password."):
            print("Sign up form, empty fields test passed")
        else:
            print("Sign up form, empty fields test failed")

        # Test 3: Existing user
        driver.get("https://www.demoblaze.com/")
        signup_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SIGNUP_LINK))
        signup_button.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-username"))).send_keys(VALID_USERNAME)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-password"))).send_keys(VALID_PASSWORD)
        driver.find_element(*SIGNUP_BUTTON).click()

        if handle_alert("This user already exist."):
            print("Creating existing user test passed")
        else:
            print("Creating existing user test failed")


    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        log_file.close()
        driver.quit()

# Run the login_test
print("Log in tests results: ")
login_tests()
# Run other tests
print("Sign in tests results: ")
sign_in_tests()
