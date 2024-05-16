import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

visited_urls = set()
depth_limit = 5

# Hardcoded credentials for login pages
USERNAME = 'your_username'
PASSWORD = 'your_password'

# Function to capture input controls
def capture_input_controls(driver):
    logger.info('Capturing input controls from the page.')
    input_controls = []

    try:
        # Capture text boxes
        text_boxes = driver.find_elements(By.TAG_NAME, 'input')
        for tb in text_boxes:
            if tb.get_attribute('type') in ['text', 'password', 'email', 'number']:
                input_controls.append({
                    'type': 'textbox',
                    'name': tb.get_attribute('name'),
                    'id': tb.get_attribute('id'),
                    'value': tb.get_attribute('value')
                })

        # Capture text areas
        text_areas = driver.find_elements(By.TAG_NAME, 'textarea')
        for ta in text_areas:
            input_controls.append({
                'type': 'textarea',
                'name': ta.get_attribute('name'),
                'id': ta.get_attribute('id'),
                'value': ta.get_attribute('value')
            })

        # Capture dropdowns
        dropdowns = driver.find_elements(By.TAG_NAME, 'select')
        for dd in dropdowns:
            options = [option.text for option in Select(dd).options]
            input_controls.append({
                'type': 'dropdown',
                'name': dd.get_attribute('name'),
                'id': dd.get_attribute('id'),
                'options': options
            })

        # Capture buttons
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            input_controls.append({
                'type': 'button',
                'name': btn.get_attribute('name'),
                'id': btn.get_attribute('id'),
                'text': btn.text
            })

    except Exception as e:
        logger.error(f"Error while capturing input controls: {e}")

    logger.info('Finished capturing input controls.')
    return input_controls

# Function to check if the page is a login page and perform login if true
def handle_login_page(driver):
    logger.info('Checking if the page is a login page.')
    try:
        username_field = None
        password_field = None
        login_button = None

        inputs = driver.find_elements(By.TAG_NAME, 'input')
        for input_field in inputs:
            if input_field.get_attribute('type') == 'text' and ('user' in input_field.get_attribute('name').lower() or 'user' in input_field.get_attribute('id').lower()):
                username_field = input_field
            elif input_field.get_attribute('type') == 'password':
                password_field = input_field

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            if 'login' in button.text.lower() or 'submit' in button.text.lower():
                login_button = button
                break

        if username_field and password_field and login_button:
            logger.info('Login page detected. Attempting to log in.')
            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            login_button.click()
            time.sleep(2)  # wait for the login action to complete
            return True
        else:
            logger.info('This page does not seem to be a login page.')
            return False

    except Exception as e:
        logger.error(f"Error while handling login page: {e}")
        return False

# Recursive function to navigate and capture controls
def navigate_and_capture(driver, url, depth):
    if depth > depth_limit:
        return

    if url in visited_urls:
        return

    visited_urls.add(url)
    logger.info(f'Navigating to URL: {url}, Depth: {depth}')
    driver.get(url)
    time.sleep(2)  # wait for the page to load

    # Handle login if it's a login page
    if handle_login_page(driver):
        # If login is successful, update the current URL after login
        url = driver.current_url

    # Capture input controls
    input_controls = capture_input_controls(driver)

    # Get the full HTML source
    html_source = driver.page_source
    logger.info('Captured HTML source.')

    # Save HTML source and input controls to JSON
    result = {
        'url': url,
        'html_source': html_source,
        'input_controls': input_controls
    }

    output_file = f'page_data_depth_{depth}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    logger.info(f'Data saved to {output_file}')

    # Find and navigate to links and buttons
    links = driver.find_elements(By.TAG_NAME, 'a')
    buttons = driver.find_elements(By.TAG_NAME, 'button')

    for link in links:
        href = link.get_attribute('href')
        if href and href not in visited_urls:
            navigate_and_capture(driver, href, depth + 1)

    for button in buttons:
        try:
            button.click()
            time.sleep(2)  # wait for the page to load after button click
            navigate_and_capture(driver, driver.current_url, depth + 1)
            driver.back()  # go back to the previous page
            time.sleep(2)  # wait for the page to load
        except Exception as e:
            logger.error(f"Error while clicking button: {e}")

# Main function to execute the script
def main(url):
    logger.info(f'Starting WebDriver for URL: {url}')

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=chrome_options)

    try:
        navigate_and_capture(driver, url, 0)
    except Exception as e:
        logger.error(f"Error during execution: {e}")
    finally:
        driver.quit()
        logger.info('WebDriver closed.')

if __name__ == '__main__':
    target_url = 'http://example.com'  # Replace with your target URL
    main(target_url)
