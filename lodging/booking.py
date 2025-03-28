from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re





def scrape_booking(city, checkin, checkout, adults, children):

    url = f"https://www.booking.com/searchresults.zh-tw.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults={adults}&group_children={children}"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  
    driver.get(url)
    
    

    hotels = []
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')))
        time.sleep(5)
        hotel_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        
        for item in hotel_elements:
            try:
                name = item.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text if item.find_elements(By.CSS_SELECTOR, 'div[data-testid="title"]') else 'N/A'
                rating_raw = item.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text if item.find_elements(By.CSS_SELECTOR, 'div[data-testid="review-score"]') else 'N/A'
                rating_match = re.search(r'(\d+(\.\d+)?)', rating_raw)
                rating = f"{rating_match.group(0)}分" if rating_match else 'N/A'
                
                price = item.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text if item.find_elements(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]') else 'N/A'
                address_raw = item.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text if item.find_elements(By.CSS_SELECTOR, 'span[data-testid="address"]') else 'N/A'
                address = address_raw.strip()
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                image_url = item.find_element(By.CSS_SELECTOR, 'img[data-testid="image"]').get_attribute('src') if item.find_elements(By.CSS_SELECTOR, 'img[data-testid="image"]') else 'N/A'
                
                hotels.append( {
                    '名稱': name,
                    '評價': rating,
                    '連結': link,
                    '價格': price,
                    '地址': address,
                    '圖片': image_url
                })
                
                yield hotels[-1]  # 逐筆回傳
            except Exception as e:
                print(f"無法解析飯店資訊: {e}")
    except Exception as e:
        print(f"頁面載入錯誤: {e}")
    finally:
        
        driver.quit()
    # return hotels