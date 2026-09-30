# weather_report.py
# 날씨 리포트 프로그램

# GitHub Repository:
# https://github.com/본인아이디/weather-report

import requests


# 날씨 코드 숫자를 한글 날씨 상태로 변경
def weather_text(code):

    weather_codes = {
        0: "맑음",
        1: "대체로 맑음",
        2: "구름 조금",
        3: "흐림",

        45: "안개",
        48: "서리 안개",

        51: "약한 이슬비",
        53: "이슬비",
        55: "강한 이슬비",

        61: "약한 비",
        63: "비",
        65: "강한 비",

        71: "약한 눈",
        73: "눈",
        75: "강한 눈",

        80: "약한 소나기",
        81: "소나기",
        82: "강한 소나기",

        95: "천둥번개"
    }

    return weather_codes.get(
        code,
        "알 수 없음"
    )


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
        "longitude": location["longitude"]
    }


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

    weather_data = get_weather(
        location["latitude"],
        location["longitude"]
    )

    print()
    print(f"지역: {location['name']}")

    # 첫 번째 시간대 날씨 코드 확인
    code = weather_data[
        "hourly"
    ]["weather_code"][0]

    print(f"날씨 코드: {code}")
    print(f"날씨 상태: {weather_text(code)}")


if __name__ == "__main__":
    main()