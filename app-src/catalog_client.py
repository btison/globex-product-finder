import os
import re
import requests
import urllib.parse
from flask import current_app

def products_per_category(categories):
    url = os.environ["CATALOG_URL"]
    path = os.environ["CATALOG_PRODUCT_BY_CATEGORY_PATH"]

    result = ''
    for i in categories:
        result += i
        result += ','
    result = result[:len(result)-1]
    result = urllib.parse.quote(result)

    service_url = url + re.sub("{.*}", result,  path)

    response = requests.get(service_url)
    if (response.status_code != 200):
        current_app.logger.warn('Call to catalog service with url ' + service_url + ' failed with status code: ' + str(response.status_code))
        return {'products': []}

    return {'products': response.json()}
