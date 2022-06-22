import ast
import json
import operator
import re
from functools import reduce

import requests
import xmltodict


def get_orders():
    with open("employee_orders.xml") as xml_file:
        # 1. Get the list of order dishes
        data = xmltodict.parse(xml_file.read())
        data_dict = ast.literal_eval(json.dumps(data))
        xml_file.close()
        # collect ordres who has IsAttending=true
        atn_list = []
        for data in data_dict["Employees"]["Employee"]:
            if data["IsAttending"] == "true":
                atn_list.append(data)
        order_list = [item["Order"] for item in atn_list]

        # collect all dishes which are part of orders
        # e.g ['Kebap', 'Caesar Salad', 'Pizza Quattro Formaggi', '10x Fried Chicken']
        dish_lists = []
        pattern = r"^\dx\s|,\s\dx\s"
        for order in order_list:
            dishes = [dish for dish in re.split(pattern, order) if dish]
            dish_lists.append(dishes)
        dish_list = list(set(reduce(operator.concat, dish_lists)))
        dish_json = json.dumps(dish_list)

        # 2. get dish_id from API call using GET method
        # url = 'https://nourish.me/api/v1/menu'
        # header = if we have
        # params = dish_json (As a request body: JSON encoded list of available dishes)
        # resp = requests.get(url=url, header, params=dish_list)
        # data_dishID = resp.json()
        # As API endpoints are not real,
        # so let assume , we have now response as below after above API call
        data_dishID = {
            "dishes": [
                {"id": 13, "name": "Kebap"},
                {"id": 3, "name": "Pizza Quattro Formaggi"},
                {"id": 23, "name": "Fried Chicken"},
                {"id": 42, "name": "Caesar Salad"},
            ]
        }

        # 3. create JSON data as request body to generate actual order for given .xml file
        orders = []
        for item in atn_list:
            dishID_amt = []
            if ", " in item["Order"]:
                # more than one dish items are ordered
                # e.g 10x Fried Chicken, 1x Caesar Salad, 1x Kebap
                dishes = item["Order"].split(", ")
                amt_dish = [dish.split(" ", 1) for dish in dishes]
                for i in amt_dish:
                    dishID_amt.append(
                        {
                            "dish_id": get_dishID(data_dishID["dishes"], i[1]),
                            "amount": get_dish_amount(i),
                        }
                    )
            else:
                # only single dish item ordered
                # e.g. 3x Pizza Quattro Formaggi
                amt_dish = item["Order"].split(" ", 1)
                dishID_amt.append(
                    {
                        "dish_id": get_dishID(data_dishID["dishes"], amt_dish[1]),
                        "amount": get_dish_amount(amt_dish),
                    }
                )
            orders.append(
                {
                    "customer": {
                        "full_name": item["Name"],
                        "address": {
                            "street": item["Address"]["Street"],
                            "city": item["Address"]["City"],
                            "postal_code": item["Address"]["PostalCode"],
                        },
                    },
                    "dishes": dishID_amt,
                }
            )
        res_orders = {"orders": orders}
        return res_orders


def get_dishID(json_data, dishName):
    return [obj for obj in json_data if obj["name"] == dishName][0]["id"]


def get_dish_amount(dish):
    return int(re.findall(r"^\d+", dish[0])[0])


orders = get_orders()
# 4. create orders from API call using POST method
# url = 'nourish.me/api/v1/bulk/order'
# header = if we have
# data = expected request body
# resp = requests.post(url=url, header, data=orders)
print(orders)
