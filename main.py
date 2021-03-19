from hanbitco import HanbitcoAPI, OrderType, OrderSide, OrderStatus, create_order_payload

api_key, secret_key = None, None

api = HanbitcoAPI(api_key, secret_key)

# Fetch all tickers (public)
result = api.fetch_ticker()
print(result)

# Fetch a ticker
result = api.fetch_ticker("ETH/BTC")
print(result)

# Fetch Orderbook (public)
result = api.fetch_order_book("ETH/BTC")
print(result)

# Fetch Orderbook (private)
result = api.fetch_balance()
print(result)

# Place an order (private)
result = api.create_order("ETH/BTC", OrderType.LIMIT, OrderSide.BUY, "0.01", "0.123")
print(result)

# Place orders in a bulk (private)
orders = []
for _ in range(5):
    order = create_order_payload("ETH/BTC", OrderType.LIMIT, OrderSide.BUY, "0.01", "0.123")
    orders.append(order)
result = api.create_orders(orders)
print(result)

# Fetch an order (private)
result = api.fetch_order("458153de-c1ae-4b9f-a79e-6d73aa8de751")
print(result)

# Get orders (private)
result = api.get_orders()
print(result)

# Get orders with Pagination (private)
next_page = None
while True:
    result = api.get_orders("ETH/BTC", OrderStatus.WAIT)
    next_page = result["next"]
    print(result)

    if not next_page:
        break

# Get recent trades (public)
result = api.get_trades()
print(result)

# Get recent trades with Pagination (public)
next_page = None
while True:
    result = api.get_trades("ETH/BTC", cursor=next_page)
    next_page = result["next"]
    print(result)

    if not next_page:
        break

# Cancel an order (private)
result = api.cancel_order("458153de-c1ae-4b9f-a79e-6d73aa8de751")  # returns None if already canceled previously
print(result)

# Cancel all orders (private)
result = api.cancel_all_orders()
print(result)
