import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert

# Define test cases: each is a dict of form input values and the expected alert (if any)
test_cases = [
    {"id": "12345678901", "age": "20", "email": "test@test.com", "password": "secret", "expected": "ID must not contain more than 10 characters"},
    {"id": "123456", "age": "9", "email": "test@test.com", "password": "secret", "expected": "Age must be between 10 and 40"},
    {"id": "123456", "age": "20", "email": "testtest.com", "password": "secret", "expected": "Email must contain '@'"},
    {"id": "123456", "age": "20", "email": "test@test.com", "password": "", "expected": "Password must not be empty"},
    {"id": "123456", "age": "20", "email": "test@test.com", "password": "secret", "expected": None}
]

# Replace with path or URL to the solution file
url = "ex1.html"

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome()
url = 'file://' + os.path.abspath('ex1.html')  # or your HTML filename
driver.get(url)

# Wait for the page and API to load
time.sleep(5)

pass_count = 0

for idx, case in enumerate(test_cases, start=1):
    # Reset the form before each test
    reset_button = driver.find_element(By.NAME, "reset")
    reset_button.click()
    time.sleep(0.2) # Give time for the form to reset

    id_input = driver.find_element(By.NAME, "id")
    age_input = driver.find_element(By.NAME, "age")
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")

    id_input.clear()
    id_input.send_keys(case["id"])
    age_input.clear()
    age_input.send_keys(case["age"])
    email_input.clear()
    email_input.send_keys(case["email"])
    password_input.clear()
    password_input.send_keys(case["password"])

    print(id_input.get_attribute("value"), age_input.get_attribute("value"))

    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(0.5)
    try:
        alert = Alert(driver)
        alert_text = alert.text
        alert.accept()
    except:
        alert_text = None

    result = ""
    if case["expected"] is None and alert_text is None:
        result = f"Test {idx}: PASS"
        pass_count += 1
    elif case["expected"] is not None and case["expected"] in (alert_text or ""):
        result = f"Test {idx}: PASS (Got alert: '{alert_text}')"
        pass_count += 1
    else:
        result = f"Test {idx}: FAIL (Expected: '{case['expected']}', Got: '{alert_text}')"
    print(result)

driver.quit()
print(f"\nPassed {pass_count} out of {len(test_cases)} tests.")
