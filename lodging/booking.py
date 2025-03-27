def scrape_booking(city, checkin, checkout, adults, children):
    import urllib.parse
    import time, re
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    encoded_city = urllib.parse.quote(city)
    url = f"https://www.booking.com/searchresults.zh-tw.html?ss={encoded_city}&checkin={checkin}&checkout={checkout}&group_adults={adults}&group_children={children}"
    print("🧪 開啟 URL：", url)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--remote-debugging-port=9222")  # 防止崩潰
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")


    service = Service(ChromeDriverManager().install())
    options.binary_location = "/usr/bin/google-chrome"

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print("❌ Chrome 啟動失敗！", e)
        raise e

    try:
        driver.get(url)

        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
            print("🍪 已自動接受 Cookie")
        except:
            print("🍪 沒有 Cookie 按鈕")

        # ✅ 等待頁面出現飯店資料（先等 loading 消失、再等卡片出現）
        try:
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, "b-loading-circle"))
            )
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]'))
            )
            print("✅ 飯店資料已出現")
        except Exception as e:
            print("⚠️ 等待飯店資料失敗，進行截圖與原始碼保存")
            driver.save_screenshot("debug.png")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise e

        print("✅ 已打開 Booking 頁面")



        print("✅ 找到飯店元素！")
        time.sleep(5)

        hotel_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        print(f"📦 抓到 {len(hotel_elements)} 間飯店")

        for item in hotel_elements:
            try:
                name = item.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text or 'N/A'
                rating_raw = item.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text or 'N/A'
                rating_match = re.search(r'(\d+(\.\d+)?)', rating_raw)
                rating = f"{rating_match.group(0)}分" if rating_match else 'N/A'

                price = item.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text or 'N/A'
                address = item.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text.strip() or 'N/A'
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') or 'N/A'
                image_url = item.find_element(By.CSS_SELECTOR, 'img[data-testid="image"]').get_attribute('src') or 'N/A'

                hotel = {
                    '名稱': name,
                    '評價': rating,
                    '連結': link,
                    '價格': price,
                    '地址': address,
                    '圖片': image_url
                }
                print("✅ 傳送飯店：", hotel['名稱'])
                yield hotel

            except Exception as e:
                print("❌ 單筆解析錯誤：", e)
    except Exception as e:
        print("❌ 無法抓到飯店清單：", e)
    finally:
        driver.quit()
        print("🧹 已關閉 Chrome")
