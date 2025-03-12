from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time


def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(options=chrome_options)


def scrape_tasty_tips_with_pagination(url):
    driver = setup_chrome_driver()
    all_tips = []
    page_num = 1

    try:
        driver.get(url)
        print(f"Navigated to {url}")

        while True:
            wait = WebDriverWait(driver, 10)

            time.sleep(2)

            try:
                wait.until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "tip-body")))
            except TimeoutException:
                print("No tip elements found on this page.")
                break

            tip_elements = driver.find_elements(
                By.CSS_SELECTOR, "p.tip-body.xs-mb05")
            page_tips = [tip.text.strip() for tip in tip_elements]
            all_tips.extend(page_tips)

            try:
                disabled_next = driver.find_element(
                    By.XPATH,
                    "//button[contains(@class, 'pagination__button') and contains(@class, 'pagination__button--next') and contains(@class, 'pagination__button--disabled')]"
                )
                break
            except NoSuchElementException:
                # check if there's an enabled next button (with only the first two classes)
                try:
                    next_button = driver.find_element(
                        By.XPATH,
                        "//button[contains(@class, 'pagination__button') and contains(@class, 'pagination__button--next') and not(contains(@class, 'pagination__button--disabled'))]"
                    )

                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)

                    try:  # try regular click else js click
                        next_button.click()
                    except ElementClickInterceptedException:
                        driver.execute_script(
                            "arguments[0].click();", next_button)

                    page_num += 1
                    if page_num == 10:
                        break

                    time.sleep(2)

                except NoSuchElementException:
                    print("No next button found. Stopping.")
                    break
                except Exception as e:
                    print(f"Error clicking next button: {str(e)}")
                    break
        return all_tips
    finally:
        driver.quit()


# URL of the recipe
url = 'https://tasty.co/recipe/creamy-lemon-garlic-chicken'

# Scrape the tips
tips = scrape_tasty_tips_with_pagination(url)

# Print the results
print(f"\nFound a total of {len(tips)} tips across all pages:")
for i, tip in enumerate(tips, 1):
    print(f"Tip {i}: {tip}")
