from typing import Dict

from hanbitco import OrderType, OrderSide


def convert_symbol(symbol: str):
    if "/" not in symbol:
        raise Exception("symbol format should be QUOTE/BASE. ex) ETH/BTC.")
    tokens = symbol.split("/")
    return "-".join(tokens).upper()


def create_order_payload(
        symbol: str, order_type: OrderType, order_side: OrderSide, price: str, amount: str
):
    currency_pair = convert_symbol(symbol)
    payload = {
        "trading_pair": currency_pair,
        "side": order_side.value,
        "order_type": order_type.value,
        "price": float(price),
        "volume": float(amount)
    }
    return payload


def furnish_cursors(result: Dict[str, str]):
    if "previous" in result and "next" in result:
        result["previous"] = result["previous"].split("?cursor=")[1] if result["previous"] else None
        result["next"] = result["next"].split("?cursor=")[1] if result["next"] else None
    return result


def private(func):
    def inner(self, *args, **kwargs):
        if not self.api_key or not self.secret:
            raise Exception("private api not accessible. need api keys.")
        return func(self, *args, **kwargs)

    return inner
