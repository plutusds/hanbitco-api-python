from typing import Dict, Any, List

import requests

import hmac
import time
import json
import base64
import hashlib
import urllib.parse

from hanbitco.utils import convert_symbol, create_order_payload, furnish_cursors, private
from hanbitco.constants import ORIGIN, OrderType, OrderSide, OrderStatus


class HanbitcoAPI:

    def __init__(self, api_key=None, secret_key=None):
        self.id = "hanbitco"
        self.base_url = "https://" + ORIGIN
        self.api_key = api_key
        self.secret = secret_key

    def fetch_ticker(self, symbol: str = None):
        path = "/v1/ticker/"
        payload = {}
        if symbol:
            symbol = convert_symbol(symbol)
            payload["trading_pair_name"] = symbol
        return self.get(path, payload=payload)

    def fetch_order_book(self, symbol: str):
        currency_pair = convert_symbol(symbol)
        path = f"/v1/orderbook/"
        payload = {
            "trading_pair_name": currency_pair
        }
        return self.get(path, payload=payload)

    @private
    def fetch_balance(self):
        path = "/v1/accounts/"
        return self.get(path, private=True)

    @private
    def create_order(
        self, symbol: str, order_type: OrderType, order_side: OrderSide, price: str, amount: str
    ):
        currency_pair = convert_symbol(symbol)
        path = "/v1/orders/"
        payload = [create_order_payload(currency_pair, order_type, order_side, price, amount)]
        return self.post(path, payload)

    @private
    def create_orders(self, orders: List[Dict[str, Any]]):
        if not orders:
            raise Exception("pass more than one order")
        path = "/v1/orders/"
        payload = orders
        return self.post(path, payload)

    @private
    def fetch_order(self, order_id: str):
        path = "/v1/orders/"
        path += f"{order_id}/"
        return self.get(path, private=True)

    @private
    def get_orders(self, symbol: str = None, status: OrderStatus = None, cursor: str = None):
        path = "/v1/orders/"
        payload = {}
        if symbol:
            symbol = convert_symbol(symbol)
            payload["trading_pair_name"] = symbol
        if status:
            payload["state"] = status.value
        if cursor:
            payload = {"cursor": cursor}
        result = self.get(path, payload, private=True)
        result = furnish_cursors(result)
        return result

    def get_trades(self, symbol: str = None, cursor: str = None):
        path = "/v1/trades/"
        payload = {}
        if symbol:
            symbol = convert_symbol(symbol)
            payload = {
                "trading_pair_name": symbol
            }
        if cursor:
            payload = {"cursor": cursor}
        result = self.get(path, payload=payload)
        result = furnish_cursors(result)
        return result

    @private
    def cancel_order(self, order_id: str):
        path = "/v1/orders/"
        path += f"{order_id}/"
        return self.delete(path)

    @private
    def cancel_all_orders(self):
        path = "/v1/orders/cancel_all/"
        return self.delete(path)

    def get(self, path, payload=None, private=False):
        payload = {} if not payload else payload
        uri = urllib.parse.urljoin(self.base_url, path)
        if "cursor" in payload:
            uri += f"?cursor={payload['cursor']}"
        elif len(payload.keys()) > 0:
            req = requests.models.PreparedRequest()
            req.prepare_url(uri, payload)
            uri = req.url

        # some payloads added to uri
        if not uri.endswith(path):
            path += uri.split(path)[1]

        headers = {}
        if private:
            headers = self._generate_auth_header("GET", path)

        response = requests.get(uri, headers=headers)
        if (response.status_code // 100) != 2: # must be 200 range
            raise Exception(
                f"get({uri}, {payload}) failed (status code: {response.status_code}) (body: {response.text})"
            )

        json_data = json.loads(response.text) if response.text else None
        return json_data

    def post(self, path, payload):
        uri = urllib.parse.urljoin(self.base_url, path)

        headers = self._generate_auth_header("POST", path, payload)
        response = requests.post(uri, headers=headers, json=payload)
        if (response.status_code // 100) != 2:  # must be 200 range
            raise Exception(
                f"post({uri}, {payload}) failed (status code: {response.status_code}) (body: {response.text})"
            )

        json_data = json.loads(response.text) if response.text else None
        return json_data

    def delete(self, path):
        uri = urllib.parse.urljoin(self.base_url, path)

        headers = self._generate_auth_header("DELETE", path)
        response = requests.delete(uri, headers=headers)
        if (response.status_code // 100) != 2:  # must be 200 range
            raise Exception(
                f"delete({uri}) failed (status code: {response.status_code}) (body: {response.text})"
            )

        json_data = json.loads(response.text) if response.text else None
        return json_data

    def _generate_auth_header(self, method, path, payload=None):
        payload = {} if not payload else payload
        key = base64.b64decode(self.secret)
        nonce = str(time.time())
        method = method.upper()
        original_text = f"{nonce}\n{method}\n{ORIGIN}\n{path}"
        if payload:
            body = json.dumps(payload)
            original_text += f"\n{body}"
        signed_text = hmac.new(key, original_text.encode("utf-8"), hashlib.sha512)
        signature = base64.b64encode(signed_text.digest()).decode("utf-8")

        headers = {
            "API-KEY": self.api_key,
            "Signature": signature,
            "Nonce": nonce
        }
        return headers


if __name__ == "__main__":
    pass
