# weather_report.py
# 날씨 리포트 프로그램

# GitHub Repository:
# https://github.com/본인아이디/weather-report

import requests
from datetime import datetime


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


# 특정 날짜, 특정 시간의 날씨를 가져오기
def get_hour_weather(
    weather_data,
    date,
    hour
):

    target_time = (
        f"{date}T{hour:02d}:00"
    )

    times = weather_data[
        "hourly"
    ]["time"]

    if target_time not in times:
        return None

    index = times.index(target_time)

    temperature = weather_data[
        "hourly"
    ]["temperature_2m"][index]

    humidity = weather_data[
        "hourly"
    ]["relative_humidity_2m"][index]

    rain = weather_data[
        "hourly"
    ]["precipitation_probability"][index]

    code = weather_data[
        "hourly"
    ]["weather_code"][index]

    wind = weather_data[
        "hourly"
    ]["wind_speed_10m"][index]

    # km/h를 m/s로 변환
    wind = wind / 3.6

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rain": rain,
        "weather": weather_text(code),
        "wind": round(wind, 1)
    }


def print_report(
    location,
    weather_data
):

    day_names = [
        "오늘",
        "내일",
        "모레"
    ]

    print()
    print("=" * 50)

    print(
        f"{location['name']} "
        "3일 날씨 예보"
    )

    print("=" * 50)

    dates = weather_data[
        "daily"
    ]["time"]

    for i in range(3):

        date = dates[i]

        date_text = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%m월 %d일")

        print()
        print(
            f"[{day_names[i]}] "
            f"{date_text}"
        )

        print("-" * 50)

        for hour in [6, 15]:

            weather = get_hour_weather(
                weather_data,
                date,
                hour
            )

            if weather is None:
                continue

            if hour == 6:
                time_text = "오전 6시"
            else:
                time_text = "오후 3시"

            print()
            print(time_text)

            print(
                f"날씨 : "
                f"{weather['weather']}"
            )

            print(
                f"기온 : "
                f"{weather['temperature']} ℃"
            )

            print(
                f"강수확률 : "
                f"{weather['rain']} %"
            )

            print(
                f"습도 : "
                f"{weather['humidity']} %"
            )

            print(
                f"풍속 : "
                f"{weather['wind']} m/s"
            )

        minimum = weather_data[
            "daily"
        ]["temperature_2m_min"][i]

        maximum = weather_data[
            "daily"
        ]["temperature_2m_max"][i]

        print()
        print(
            f"최저기온 : {minimum} ℃"
        )

        print(
            f"최고기온 : {maximum} ℃"
        )

        print("=" * 50)


def main():

    print(
        "날씨 예보 프로그램"
    )

    print(
        "3일간 오전 6시 / "
        "오후 3시 날씨를 제공합니다."
    )

    city = input(
        "\n지역을 입력하세요 "
        "(기본값: 천안): "
    ).strip()

    if city == "":
        city = "천안"

    location = get_location(city)

    if location is None:

        print(
            "지역을 찾을 수 없습니다."
        )

        return

    print()
    print(
        f"{location['name']}의 "
        "날씨 정보를 가져옵니다..."
    )

    weather_data = get_weather(
        location["latitude"],
        location["longitude"]
    )

    print_report(
        location,
        weather_data
    )


if __name__ == "__main__":
    main()