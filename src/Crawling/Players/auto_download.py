from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.premierleague.com/players"

driver.get(url)
title = driver.title
time.sleep(3)

try:
    accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_button.click()
    print("Đã chấp nhận cookies.")
except Exception as e:
    print("Không tìm thấy nút 'Accept Cookies':", e)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    print('Đang cuộn!!!')
    # Cuộn xuống cuối trang
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Chờ tải nội dung (tuỳ thuộc vào tốc độ trang web, có thể điều chỉnh)
    time.sleep(3)
    
    # Lấy chiều cao mới sau khi cuộn
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Kiểm tra nếu không có sự thay đổi chiều cao
    if new_height == last_height:
        print("Đã cuộn đến cuối trang.")
        break
    
    # Cập nhật chiều cao để tiếp tục cuộn
    last_height = new_height


html_content = driver.page_source
with open('./data/overview/Premier League Players - Overview.html','w',encoding='utf-8') as file:
    file.write(html_content)


print('HTML đã được lưu tại Premier League Players - Overview.html')
driver.quit()