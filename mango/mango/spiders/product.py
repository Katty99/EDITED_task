import json
import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    start_url = "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"

    def start_requests(self):
        url = 'https://shop.mango.com/services/garments/1704202099'

        # response.text -> cacheId
        headers = {
            "stock-id": "068.IN.0.false.false.v4",
        }

        req = scrapy.http.JsonRequest(url, headers=headers)
        yield req

    def parse(self, response):
        response = response.body
        info = json.loads(response)

        # Obtain the product's name
        name = info["name"]

        # Obtain the product's price
        price = info["price"]["price"]

        # Obtain the default colour knowing that its id is contained in the product url
        color_id = self.start_url[-2:]
        default_color = ''
        for color in info["colors"]["colors"]:
            if color["id"] == str(color_id):
                default_color = color["label"]

        # Obtain all the product's sizes, assuming that availability does not affect the output
        sizes = []
        for size in info["colors"]["colors"]:
            if size["id"] == str(color_id):
                sizes = [size["label"] for size in size["sizes"]]

        yield {
            "name": name,
            "price": price,
            "color": default_color,
            "size": sizes,
        }
