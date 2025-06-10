import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_todo_crud(driver):
    driver.get("https://todothelist-react.netlify.app/")
    wait = WebDriverWait(driver, 10)

    input_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter a Task...']")))
    add_button = driver.find_element(By.CLASS_NAME, "add-button")

    input_box.send_keys("Buy milk")
    add_button.click()
    time.sleep(5)

    tasks = driver.find_elements(By.CLASS_NAME, "text")
    assert any("Buy milk" in task.text for task in tasks)
    print("✅ Task added")

    for task in driver.find_elements(By.CLASS_NAME, "text"):
        if task.text == "Buy milk":
            delete_btn = task.find_element(By.XPATH, "../button[@class='delete-button']")
            delete_btn.click()
            break
    time.sleep(5)

    updated_tasks = driver.find_elements(By.CLASS_NAME, "text")
    assert all("Buy milk" not in t.text for t in updated_tasks)
    print("🗑 Task deleted")
