# 获取城市 天气、空气质量、生活指数、天气预报
import bisect
from collections import namedtuple
from typing import Tuple

import requests
from loguru import logger

from web.configs.get_token import get_all_api

City = namedtuple("City", ["name", "Lat", "Lon"])
city = City("NanQuan",  29.422037, 106.595346)

AGICN_TOKEN = get_all_api()["AGICN_TOKEN"]
def get_weather(city: City, token = AGICN_TOKEN):
    token = get_all_api()["AGICN_TOKEN"]
    url = f"https://api.waqi.info/feed/geo:{city.Lat};{city.Lon}/?token={token}"
    response = requests.get(url)
    res = response.json()
    if res["status"] != "ok":
        raise ValueError(f"Error: {res['data']}")

    return res

class ParseWeather:
    def __init__(self, weather: dict):
        self.weather = weather
        self.city, self.aqi, self.time = self.parse_weather()

    @staticmethod
    def get_pm25_rank(value, breakpoint=[50, 100, 150, 200, 300, 500], ranks=("优", "良", "轻度污染", "中度污染", "重度污染", "严重污染")):
        i = bisect.bisect(breakpoint, value)  # 查找分数所在的区间
        # 如果大于 则返回lens, 小于则返回0， 所以grades可以有lens + 1个
        return ranks[i]
    def parse_weather(self) -> Tuple:
        city = self.weather["data"]["city"]["name"]
        aqi = self.weather["data"]["aqi"]
        aqi = f"{aqi}-{self.get_pm25_rank(aqi)}"
        time = self.weather["data"]["time"]["s"]
        logger.info(f"City: {city}, AQI: {aqi}, Time: {time}")
        return city, aqi, time
def main():
    #weather = {"status":"ok","data":{"aqi":177,"idx":1421,"attributions":[{"url":"http://www.cepb.gov.cn/","name":"Chongqing Environmental Protection Bureau (重庆市主城区空气质量)"},{"url":"https://waqi.info/","name":"World Air Quality Index Project"}],"city":{"geo":[29.4272,106.591],"name":"Nánquán, Chongqing (重庆南泉)","url":"https://aqicn.org/city/china/zhongqing/nanquan","location":""},"dominentpol":"pm25","iaqi":{"co":{"v":8.2},"dew":{"v":3},"h":{"v":39},"no2":{"v":5.5},"o3":{"v":36.6},"p":{"v":1024},"pm10":{"v":78},"pm25":{"v":177},"so2":{"v":6.6},"t":{"v":17},"w":{"v":2.5}},"time":{"s":"2024-02-11 14:00:00","tz":"+08:00","v":1707660000,"iso":"2024-02-11T14:00:00+08:00"},"forecast":{"daily":{"o3":[{"avg":1,"day":"2024-02-09","max":2,"min":1},{"avg":5,"day":"2024-02-10","max":26,"min":1},{"avg":5,"day":"2024-02-11","max":25,"min":2},{"avg":2,"day":"2024-02-12","max":18,"min":1},{"avg":1,"day":"2024-02-13","max":2,"min":1},{"avg":1,"day":"2024-02-14","max":1,"min":1},{"avg":2,"day":"2024-02-15","max":6,"min":1},{"avg":1,"day":"2024-02-16","max":2,"min":1}],"pm10":[{"avg":28,"day":"2024-02-09","max":28,"min":28},{"avg":33,"day":"2024-02-10","max":46,"min":19},{"avg":28,"day":"2024-02-11","max":40,"min":19},{"avg":26,"day":"2024-02-12","max":28,"min":19},{"avg":45,"day":"2024-02-13","max":46,"min":32},{"avg":55,"day":"2024-02-14","max":68,"min":46},{"avg":48,"day":"2024-02-15","max":58,"min":46},{"avg":49,"day":"2024-02-16","max":58,"min":46},{"avg":46,"day":"2024-02-17","max":46,"min":46}],"pm25":[{"avg":89,"day":"2024-02-09","max":89,"min":89},{"avg":92,"day":"2024-02-10","max":124,"min":68},{"avg":89,"day":"2024-02-11","max":120,"min":68},{"avg":84,"day":"2024-02-12","max":89,"min":68},{"avg":134,"day":"2024-02-13","max":138,"min":99},{"avg":153,"day":"2024-02-14","max":169,"min":138},{"avg":108,"day":"2024-02-15","max":158,"min":89},{"avg":119,"day":"2024-02-16","max":138,"min":89},{"avg":128,"day":"2024-02-17","max":138,"min":99}]}},"debug":{"sync":"2024-02-11T15:26:51+09:00"}}}
    weather = get_weather(city)
    parse_weather = ParseWeather(weather)
    print(weather)

if __name__ == "__main__":
    main()
