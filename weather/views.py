import json
import os

    
def get_weather_data(city_name):
    """從 Taiwan_Weather.json 讀取指定城市的 10 天天氣"""
    json_path = os.path.join(os.path.dirname(__file__), "Taiwan_Weather.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            weather_data = json.load(f)
        
        # 確保回傳完整天氣資訊
        return [
            {
                "date": day["date"],
                "temp_min": day["temp_min"],
                "temp_max": day["temp_max"],
                "weather": day["weather_condition"],  # 新增天氣狀況
                "rain_chance": day["rain_probability"]  # 新增降雨機率
            }
            for day in weather_data.get(city_name, {}).get("weather", [])
        ]
    except FileNotFoundError:
        return []

