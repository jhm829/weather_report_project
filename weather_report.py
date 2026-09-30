# weather_report.py
# 날씨 리포트 프로그램

# GitHub Repository:
# https://github.com/본인아이디/weather-report

import requests


# 지역 이름을 입력받아 위도와 경도를 구하는 함수
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
    print("검색된 지역")
    print(f"지역명: {location['name']}")
    print(f"위도: {location['latitude']}")
    print(f"경도: {location['longitude']}")


if __name__ == "__main__":
    main()