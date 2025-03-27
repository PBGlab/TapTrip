from celery import shared_task
from .booking import scrape_booking
import json
import os
import re

# ✅ 共用的命名清洗函式（保留中文字與英數）
def clean_filename(text):
    import re
    # ✅ 僅移除特殊字元，保留「臺」不轉換
    return re.sub(r"[^\w\u4e00-\u9fa5]", "", text)
    
@shared_task
def run_booking_scraper(city, checkin, checkout, adults, children):
    try:
        print(f"🚀 Celery 任務啟動：{city}")
        results = list(scrape_booking(city, checkin, checkout, adults, children))

        safe_city = clean_filename(city)
        file_path = f"/tmp/hotel-result-{safe_city}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

        print(f"✅ 已寫入結果檔案：{file_path}")

    except Exception as e:
        error_path = f"/tmp/hotel-error-{clean_filename(city)}.log"
        with open(error_path, "w") as f:
            f.write(str(e))
        print(f"❌ 寫入錯誤檔案：{error_path}")