# weather_report.py
# 날씨 리포트 프로그램

# GitHub Repository:
# https://github.com/본인아이디/weather-report

import requests


def get_location(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "ko",
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "country": location.get("country", ""),
        "admin1": location.get("admin1", "")
    }


# 위도와 경도를 이용해 날씨 데이터를 받아오는 함수
def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation_probability,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min"
        ),
        "timezone": "auto",
        "forecast_days": 3
    }

    response = requests.get(url, params=params)

    return response.json()


def main():
    print("날씨 리포트 프로그램")
    print("-" * 40)

    city = input(
        "날씨를 확인할 지역을 입력하세요 "
        "(기본값: 천안): "
    ).strip()

    if city == "":
        city = "천안"

    location = get_location(city)

    if location is None:
        print("지역을 찾을 수 없습니다.")
        return

    print()
    print(
        f"{location['name']}의 날씨 정보를 "
        "가져오는 중입니다..."
    )

    weather_data = get_weather(
        location["latitude"],
        location["longitude"]
    )

    print()
    print("날씨 데이터를 성공적으로 가져왔습니다.")

    print(
        "예보 날짜:",
        weather_data["daily"]["time"]
    )


if __name__ == "__main__":
    main()