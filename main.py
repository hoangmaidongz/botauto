import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Thông tin đăng nhập Facebook
FB_EMAIL = "your_email"
FB_PASSWORD = "your_password"
GROUP_URL = "https://www.facebook.com/groups/YOUR_GROUP_ID/"
PAGE_URL = "https://www.facebook.com/YOUR_PAGE_ID/"

# Cấu hình trình duyệt không giao diện (headless)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Chạy không giao diện
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Đăng nhập Facebook
def login_facebook():
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(FB_EMAIL)
    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(FB_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

# Lấy bài viết mới nhất từ Page
def get_latest_post():
    driver.get(PAGE_URL)
    time.sleep(5)

    try:
        # Tìm bài viết đầu tiên
        post = driver.find_element(By.XPATH, "//div[@role='article']")
        post_link = post.find_element(By.TAG_NAME, "a").get_attribute("href")
        return post_link
    except:
        print("Không tìm thấy bài viết mới.")
        return None

# Chia sẻ bài viết lên Group
def share_post_to_group():
    post_link = get_latest_post()
    if not post_link:
        return
    
    driver.get(GROUP_URL)
    time.sleep(5)

    try:
        post_box = driver.find_element(By.XPATH, "//div[@aria-label='Viết gì đó...']")
        post_box.click()
        time.sleep(2)

        post_box.send_keys(f"📢 Bài viết mới từ Liên Đội: {post_link}")
        time.sleep(2)

        post_button = driver.find_element(By.XPATH, "//button[contains(text(),'Đăng')]")
        post_button.click()
        print("✅ Đã chia sẻ bài viết thành công!")
    except:
        print("❌ Không thể đăng bài.")

# Chạy bot
login_facebook()
share_post_to_group()
driver.quit()
