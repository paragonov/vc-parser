from __future__ import absolute_import, unicode_literals

import math
import requests
import re


from bs4 import BeautifulSoup

from celery import shared_task

from .configs_shops import config_mv, config_cl, config_dns
from .utils import save_db


@shared_task
def scraper_mv():
    product_num = 0
    products_result_mv = {}

    with requests.Session() as session_mv:
        response_pages = session_mv.get(
            url=config_mv.url_pages,
            params=config_mv.params_mv,
            cookies=config_mv.cookies_mv,
            headers=config_mv.headers_mv,
        )
        response_pages = response_pages.json()
        total_items_pages = response_pages.get("body").get("total")
        pages = math.ceil(total_items_pages / 24)

        for page in range(pages):
            offset = f"{page * 24}"
            config_mv.params_mv["offset"] = offset
            items_prices = {}
            response = session_mv.get(
                url=config_mv.url_id,
                params=config_mv.params_mv,
                cookies=config_mv.cookies_mv,
                headers=config_mv.headers_mv,
            )
            response = response.json()
            products_id = response.get("body").get("products")
            config_mv.json_data_mv["productIds"] = products_id
            products_id_str = ",".join(products_id)
            params_prices = {
                "productIds": products_id_str,
                "addBonusRubles": "true",
                "isPromoApplied": "true",
            }
            response_products_prices = session_mv.get(
                url=config_mv.url_prices,
                params=params_prices,
                cookies=config_mv.cookies_mv,
                headers=config_mv.headers_mv,
            )
            response_products_prices = response_products_prices.json()
            product_prices = response_products_prices.get("body").get("materialPrices")
            for item in product_prices:
                item_id = item.get("price").get("productId")
                item_price = item.get("price").get("basePrice")

                items_prices[item_id] = {"item_price": item_price}
            response_products_list = session_mv.post(
                url=config_mv.url_lists,
                cookies=config_mv.cookies_mv,
                headers=config_mv.headers_mv,
                json=config_mv.json_data_mv,
            )
            response_products_list = response_products_list.json()
            product_list = response_products_list.get("body").get("products")
            for product in product_list:
                product_id = product.get("productId")
                if product_id in items_prices:
                    product_num += 1
                    product_price = items_prices[product_id]
                    products_result_mv[product_num] = {
                        "product_name": product.get("name"),
                        "product_link": f"https://www.mvideo.ru/products/{product.get('nameTranslit')}-{product_id}",
                        "product_price": product_price.get("item_price"),
                        "product_available": True,
                    }

    return save_db(products_result_mv, "Мвидео")


@shared_task
def scraper_cl():
    with requests.Session() as session_cl:
        product_result_cl = {}
        product_num = 0
        response = session_cl.get(url=f"{config_cl.url}", headers=config_cl.headers_cl)
        response_pages_count_text = response.text
        soup = BeautifulSoup(response_pages_count_text, "lxml")
        pages_count_link = soup.find_all("a", class_="PaginationWidget__page")
        if pages_count_link:
            pages_count = int(pages_count_link[-1].text.strip())
        else:
            pages_count = 1

        for page in range(1, pages_count + 1):
            response = session_cl.get(
                f"{config_cl.url}&p={page}", headers=config_cl.headers_cl
            )
            response_text = response.text

            soup = BeautifulSoup(response_text, "lxml")
            prods = [
                prod for prod in soup.find_all("div", class_="product_data__gtm-js")
            ]

            for prod in prods:
                product_num += 1
                product_result_cl[product_num] = {
                    "product_name": prod.find(
                        "a", "ProductCardHorizontal__title"
                    ).text.strip(),
                    "product_link": f"https://www.citilink.ru{prod.find('a', 'ProductCardHorizontal__title').get('href')}",
                    "product_price": prod.find(
                        "span", "ProductCardHorizontal__price_current-price"
                    ).text.strip(),
                    "product_available": 1,
                }

    return save_db(product_result_cl, "Citilink")


@shared_task
def scraper_dns():
    with requests.Session() as session:
        product_result_dns = {}
        response_pagination = session.get(
            config_dns.url_dns,
            cookies=config_dns.cookies_dns,
            headers=config_dns.headers_dns,
        )
        soup_pagination = BeautifulSoup(response_pagination.text, "lxml")
        elem_pagination = soup_pagination.find_all(
            "a", class_="pagination-widget__page-link pagination-widget__page-link_last"
        )
        pages_count = int(
            re.findall(r"p=(\d*)", str(elem_pagination[0].get("href")))[0]
        )
        products_name = []
        products_price = []
        products_available = []

        for page in range(1, pages_count + 1):
            response = session.get(
                f"{config_dns.url_dns}&p={page}",
                cookies=config_dns.cookies_dns,
                headers=config_dns.headers_dns,
            )
            soup = BeautifulSoup(response.text, "lxml")
            products_name.extend(
                soup.find_all("a", class_="catalog-product__name ui-link ui-link_black")
            )
            product_id1 = soup.find_all(
                "span", class_="catalog-product__buy product-buy"
            )
            product_id2 = soup.find_all(
                "div", class_="catalog-product ui-button-widget"
            )
            products_ids = list(zip(product_id1, product_id2))

            prices = []
            avails = []

            for ind, pid in enumerate(products_ids):
                data_price = (
                    f'data={{"type":"product-buy","containers":'
                    f'[{{"id":"{str(pid[0].get("id"))}","data":{{"id":"{str(pid[1].get("data-product"))}"}}}}]}}'
                )
                data_avail = (
                    f'data={{"type":"avails","containers":'
                    f'[{{"id":"{str(pid[0].get("id"))}","data":{{"id":"{str(pid[1].get("data-product"))}", "type":0,"useNotInStock":true}}}}]}}'
                )

                while True:
                    response_price = session.post(
                        config_dns.url_price_dns,
                        cookies=config_dns.cookies1_dns,
                        headers=config_dns.headers1_dns,
                        data=data_price,
                        params=config_dns.params_dns,
                    )
                    response_avail = session.post(
                        config_dns.url_avail_dns,
                        params=config_dns.params_dns,
                        cookies=config_dns.cookies1_dns,
                        headers=config_dns.headers1_dns,
                        data=data_avail,
                    )

                    if response_price.ok and response_avail.ok:
                        current = response_price.json()["data"]["states"][0]["data"][
                            "price"
                        ]["current"]
                        avail = response_avail.json()["data"]["states"][0]["data"][
                            "html"
                        ]
                        avails.append(avail)
                        prices.append(current)
                        break
                    else:
                        continue
            products_price.extend(prices)
            products_available.extend(avails)

        product_count = 0

        products_list = list(zip(products_name, products_price, products_available))

        for prod in products_list:
            product_count += 1
            avail_soup = BeautifulSoup(prod[2], "lxml")
            avail_res = avail_soup.text
            product_result_dns[product_count] = {
                "product_name": prod[0].text,
                "product_link": f"https://www.dns-shop.ru{prod[0].get('href')}",
                "product_price": prod[1],
                "product_available": True,
            }

    return save_db(product_result_dns, "DNS")
