import time

import requests
import logging
import pytest
import json
import jsonpath
from hamcrest import *
from jsonschema import validate

"""课程帖子 https://testerhome.com/topics/19849 """


class TestRequests(object):
    logging.basicConfig(level=logging.INFO)
    url = "https://testerhome.com/api/v3/topics.json?limit=2"

    def test_get(self):
        r = requests.get(self.url)
        logging.info(r)
        logging.info(r.text)
        logging.info(json.dumps(r.json(), indent=2))

    def test_get_param(self):
        r = requests.get(self.url,
                         params={"a": 1, "b": "string corntent"},
                         headers={"a": "1", "b": "b2"},
                         proxies={"https": "http://127.0.0.1:8888",
                                  "http": "http://127.0.0.1:8888"},  # 记得打开代理tool
                         verify=False
                         )
        logging.info(r.url)
        logging.info(r.text)
        logging.info(json.dumps(r.json(), indent=2))

    def test_post(self):
        # https://xueqiu.com/upload/web?category=web_behavior 下载雪球app
        r = requests.post("https://xueqiu.com/upload/web?category=web_behavio",
                          data={"category": "web_behavior"},
                          headers={"a": "1", "b": "b2"},
                          verify=False
                          )
        logging.info("返回是:%s" % r)

        logging.info(r.text)
        if r.status_code == 200:
            logging.info(json.dumps(r.json(), indent=2))

    def test_cookies(self):
        r = requests.get("http://47.95.238.18:8090/cookies", cookies={"a": "1", "b": "string content"})
        logging.info(r.text)

    def test_xueqiu_quote(self):
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?"
        r = requests.get(url,
                         params={"category": "2"},
                         headers={'User-Agent': 'Xueqiu Android 11.19'},
                         cookies={"u": "3446260779", "xq_a_token": "5806a70c6bc5d5fb2b00978aeb1895532fffe502"}
                         )
        logging.info(json.dumps(r.json(), indent=2))
        assert r.json()["data"]["category"] == 2
        assert r.json()["data"]["stocks"][0]["name"] == "华宝中短债债券C"
        assert jsonpath.jsonpath(r.json(),
                                 "$.data.stocks[?(@.symbol == 'F006947')].name")[0] == "华宝中短债债券A"
        assert_that(jsonpath.jsonpath(r.json(), "$.data.stocks[?(@.symbol == 'F006947')].name")[0],
                    equal_to("华宝中短债债券B"), "比较上市代码与名字")

    def test_xueqiu_portfolio(self):
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?"
        param = {"_t": "1NETEASEa68ae3bcde6345779961c5841d512b36.6610151720.1563679888590.1563685284150",
                 "_s": "855924",
                 "category": "1",
                 "pid": "-1",
                 "size": "10000",
                 "x": "0.251",
                 "page": "1"}
        cookies = {"u": "3446260779", "xq_a_token": "5806a70c6bc5d5fb2b00978aeb1895532fffe502"}
        header = {"User-Agent": "Xueqiu Android 11.26.2"}

        r = requests.get(url, params=param, headers=header, cookies=cookies)
        time.sleep(1)
        logging.info("-----返回是----\n", json.dumps(r.json(), indent=2))

    def test_xueqiu_list_schema(self):  # json_schema使用方法
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?"
        r = requests.get(url,
                         params={"category": "2"},
                         headers={'User-Agent': 'Xueqiu Android 11.19'},
                         cookies={"u": "3446260779", "xq_a_token": "5806a70c6bc5d5fb2b00978aeb1895532fffe502"}
                         )
        logging.info(json.dumps(r.json(), indent=2))

        schema = json.load(open("list_schema.json"))
        validate(instance=r.json(), schema=schema)

    def test_hamcrest(self):
        assert_that(0.1 * 0.1, close_to(0.01, 0.000000000000001))
        # assert_that(0.1 * 0.1, close_to(0.01, 0.000000000000000001))
        assert_that(
            ["a", "b", "c"],
            all_of(
                has_items("c", "d"),
                has_items("c", "a")
            )
        )

    def test_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
        }
        validate(instance={"name": "Ronaldo", "price": 168.38}, schema=schema)  # pass
        validate(instance={"name": "Eggs", "price": "34.99"}, schema=schema)  # failed
