import urllib.request
import urllib.parse
import json
import os
import time

# 台灣 22 縣市 英文名
cities = {
    "臺北市": "Taipei",
    "新北市": "New Taipei",
    "桃園市": "Taoyuan",
    "臺中市": "Taichung",
    "臺南市": "Tainan",
    "高雄市": "Kaohsiung",
    "基隆市": "Keelung",
    "新竹市": "Hsinchu",
    "新竹縣": "Hsinchu County",
    "苗栗縣": "Miaoli",
    "彰化縣": "Changhua",
    "南投縣": "Nantou",
    "雲林縣": "Yunlin",
    "嘉義市": "Chiayi",
    "嘉義縣": "Chiayi County",
    "屏東縣": "Pingtung",
    "宜蘭縣": "Yilan",
    "花蓮縣": "Hualien",
    "臺東縣": "Taitung",
}

# API 設定
API_KEY = "VAZHVQTFXZYEVUFAST8QSFMYL"
UNIT = "metric"

# GitHub Pages 連結（天氣圖示）
ICON_BASE_URL = "https://jerrylin0230.github.io/weather-icons/icons/"

# 天氣條件的中英文對照
condition_translation = {
    "Clear": "晴朗",
    "Cloudy": "多雲",
    "Fog": "霧",
    "Partially cloudy": "局部多雲",
    "Overcast": "陰天",
    "Rain": "雨天",
    "Rain, Overcast": "陰天有雨",
    "Thunderstorm": "雷雨",
    "Wind": "有風",
    "unknown": "未知"
}

# 圖示對應
icon_mapping = {
    "Clear": "clear-day.svg",
    "Cloudy": "cloudy.svg",
    "Fog": "fog.svg",
    "Partially cloudy": "partly-cloudy-day.svg",
    "Overcast": "wind.svg",
    "Rain": "thunder-rain.svg",
    "Rain, Overcast": "thunder-rain.svg",
    "Thunderstorm": "thunder.svg",
    "Wind": "wind.svg",
    "unknown": "unknown.svg"
}


def fetch_weather(city_name, city_eng):
    """從 API 取得天氣資料並翻譯為中文"""
    city_eng_encoded = urllib.parse.quote(city_eng)  # 城市名稱編碼
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_eng_encoded}?unitGroup={UNIT}&key={API_KEY}&contentType=json"

    try:
        response = urllib.request.urlopen(url)
        json_data = json.load(response)

        # 提取天氣資訊
        weather_info = {
            "city": city_name,
            "weather": []
        }

        for day in json_data["days"][:10]:  # 10天的資料
            condition = day.get("conditions", "unknown")  # 取得天氣條件（英文）
            translated_condition = condition_translation.get(condition, "未知")  # 轉換為中文
            rain_chance = day.get("precipprob", 0)  # 降雨機率

            # 取得 icon 名稱
            icon_file = icon_mapping.get(condition, "unknown.svg")
            icon_url = f"{ICON_BASE_URL}{icon_file}"

            # Debug: 確認翻譯是否正確
            print(f"城市: {city_name}, 日期: {day['datetime']}, 原始: {condition}, 翻譯: {translated_condition}")

            weather_info["weather"].append({
                "date": day["datetime"],
                "temp_min": round(day["tempmin"]),
                "temp_max": round(day["tempmax"]),
                "weather_condition": translated_condition,  # ✅ 中文天氣條件
                "rain_probability": f"{rain_chance}%",
                "icon": icon_url
            })

        return weather_info

    except urllib.error.HTTPError as e:
        print(f"HTTP 錯誤: {e.code} - {e.read().decode()}")
    except urllib.error.URLError as e:
        print(f"URL 錯誤: {e.reason}")
    except Exception as e:
        print(f"發生錯誤: {e}")

    return None


def update_weather():
    """自動更新所有城市天氣資料"""
    weather_data = {}

    for city_name, city_eng in cities.items():
        print(f"更新 {city_name} 天氣資料...")
        weather_info = fetch_weather(city_name, city_eng)

        if weather_info:
            weather_data[city_name] = weather_info

        time.sleep(3)  # 避免 API 限制

    # 存 JSON 檔
    with open("./weather/Taiwan_Weather.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

    print("✅ 天氣資料已更新，儲存至 Taiwan_Weather.json")


# 主程式
if __name__ == "__main__":
    update_weather()
