import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_ntut_posts():
    # 配置 Chrome 浏览器选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU
    chrome_options.add_argument("--no-sandbox")  # 无沙盒模式

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.facebook.com/taipeitech1912")
    wait = WebDriverWait(driver, 10)

    try:
        # 等待并点击“更多”按钮
        more_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/i'))
        )
        more_button.click()

        POST_XPATH = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/'

        def scroll_to_bottom():
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        def scroll_to_and_click(element):
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", element)
            time.sleep(1)
            element.click()
            time.sleep(1)

        start = 1
        end = 1

        for post_number in range(start, end + 1):
            # 检查是否在范围内
            if post_number not in range(1, end + 1):
                scroll_to_bottom()
                continue

            # 等待并获取“查看更多”按钮
            check_see_more = wait.until(
                EC.visibility_of_element_located((By.XPATH, f'{POST_XPATH}div[{post_number}]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div/div/span/div[last()]/div/div'))
            )
            see_more = "查看更多"
            post_context = wait.until(
                EC.visibility_of_element_located((By.XPATH, f'{POST_XPATH}div[{post_number}]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div/div'))
            )

            if see_more in check_see_more.text:
                scroll_to_and_click(check_see_more)
                return {"Context": post_context.text}
            else:
                return {"Context": post_context.text}

    finally:
        driver.quit()
