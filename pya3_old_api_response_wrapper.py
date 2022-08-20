from pya3 import *

# User Credential
user_id=''
api_key=''

# Connect and get session Id
alice = Aliceblue(user_id=user_id,api_key=api_key)
alice.get_session_id()

"""
Balance Wrapper Request
"""
# get_balance_response=alice.get_balance()
# print(Alice_Wrapper.get_balance(get_balance_response))

"""
Profile Wrapper Request
"""
# get_profile_response=alice.get_profile()
# print(Alice_Wrapper.get_profile(get_profile_response))

"""
Daywise Position Request
"""
# get_daywise_positions_response=alice.get_daywise_positions()
# print(Alice_Wrapper.get_daywise_positions(get_daywise_positions_response))

"""
Netwise Position Request
"""
# get_netwise_positions_response=alice.get_netwise_positions()
# print(Alice_Wrapper.get_netwise_positions(get_netwise_positions_response))

"""
Holding Position Request
"""
# get_holding_positions_response=alice.get_holding_positions()
# print(Alice_Wrapper.get_holding_positions(get_holding_positions_response))

"""
Place Order Wrapper
"""
# place_order_response=alice.place_order(transaction_type = TransactionType.Buy,instrument = alice.get_instrument_by_token('NSE',14366),quantity = 1,order_type = OrderType.Limit,product_type = ProductType.Delivery,price = 8.10,trigger_price = None,stop_loss = None,square_off = None,trailing_sl = None,is_amo = False,order_tag='order1')
# print(Alice_Wrapper.place_order(place_order_response))

"""
Basket Order Wrapper
"""
# order1 = {  "instrument"        : alice.get_instrument_by_symbol('NSE', 'INFY'),
#             "order_type"        : OrderType.Market,
#             "quantity"          : 1,
#             "transaction_type"  : TransactionType.Buy,
#             "product_type"      : ProductType.Delivery,
#             "order_tag"         : "Order1"}
# order2 = {  "instrument"        : alice.get_instrument_by_symbol('NSE', 'SBIN'),
#             "order_type"        : OrderType.Limit,
#             "quantity"          : 2,
#             "price"             : 280.0,
#             "transaction_type"  : TransactionType.Sell,
#             "product_type"      : ProductType.Intraday,
#             "order_tag"         : "Order2"}
# orders = [order1, order2]
# place_basket_order_response=alice.place_basket_order(orders)
# print(Alice_Wrapper.place_basket_order(place_basket_order_response))

"""
Modify Order Wrapper
"""
# modify_order_response = alice.modify_order(transaction_type = TransactionType.Buy,
#                      instrument = alice.get_instrument_by_token('MCX', 243894),
#                      order_id="220817000186214",
#                      quantity = 1,
#                      order_type = OrderType.Limit,
#                      product_type = ProductType.Delivery,
#                      price=00.11,
#                      trigger_price = None)
# print(Alice_Wrapper.modify_order(modify_order_response))

"""
Order history Wrapper
"""
# get_order_history_response=alice.get_order_history('')
# print(Alice_Wrapper.get_order_history(get_order_history_response))

"""
Trade Book Wrapper
"""
# get_trade_book_response=alice.get_trade_book()
# print(Alice_Wrapper.get_trade_book(get_trade_book_response))

"""
Cancel Order Wrapper
"""
# cancel_order_response=alice.cancel_order(alice.get_instrument_by_token('NSE', 14366),'220818000186250')
# print(Alice_Wrapper.cancel_order(cancel_order_response))
