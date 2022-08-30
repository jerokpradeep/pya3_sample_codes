"""
#########Short Inverted Strategy#########
"""

from pya3 import *

# User Credential
user_id=''
api_key=''

# Connect and get session Id
alice = Aliceblue(user_id=user_id,api_key=api_key)
alice.get_session_id()

# Global Declaration Variable
LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []

# Socket will run in background as separate thread
def socket():
    def socket_open():  # Socket open callback function
        print("Connected")
        global socket_opened
        socket_opened = True
        if subscribe_flag:  # This is used to resubscribe the script when reconnect the socket.
            alice.subscribe(subscribe_list)

    def socket_close():  # On Socket close this callback function will trigger
        global socket_opened, LTP
        socket_opened = False
        LTP = 0
        print("Closed")

    def socket_error(message):  # Socket Error Message will receive in this callback function
        global LTP
        LTP = 0
        print("Error :", message)

    def feed_data(message):  # Socket feed data will receive in this callback function
        global LTP, subscribe_flag
        feed_message = json.loads(message)
        if feed_message["t"] == "ck":
            print("Connection Acknowledgement status :%s (Websocket Connected)" % feed_message["s"])
            subscribe_flag = True
            print("subscribe_flag :", subscribe_flag)
            print("-------------------------------------------------------------------------------")
            pass
        elif feed_message["t"] == "tk":
            print("Token Acknowledgement status :%s " % feed_message)
            print("-------------------------------------------------------------------------------")
            pass
        else:
            # print("Feed :", feed_message)
            LTP = feed_message['lp'] if 'lp' in feed_message else LTP  # If LTP in the response it will store in LTP variable

    # Socket Connection Request
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                          socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)

    while not socket_opened:
        pass

    global subscribe_list, unsubscribe_list

    # Subscribe the Instrument
    print("Subscribe :",datetime.now())
    subscribe_list = [alice.get_instrument_by_token('INDICES',26000)]
    alice.subscribe(subscribe_list)
    # sleep(10)
    # print("Unsubscribe :",datetime.now())
    # unsubscribe_list = [alice.get_instrument_by_token("INDICES",26000)]
    # alice.unsubscribe(unsubscribe_list)
    # sleep(8)

    # Stop the websocket
    # alice.stop_websocket()
    # sleep(10)
    # print(datetime.now())
    #
    # # Connect the socket after socket close
    # alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
    #                       socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)


# strategy Function here you can implement your strategy
def strategy():
    strategy_loop_flag=True
    print("--------------------------------------Strategy Initiated--------------------------------------")
    # Insert Strategy Execution Time
    strategy_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    print("Strategy will Execute at :",strategy_time)
    while strategy_loop_flag:
        # print("LTP", LTP)
        current__time = datetime.now()
        print("Current Time :",datetime.now())
        if strategy_time <= current__time:
            print("Last Traded Price:",LTP)
            base = 50 # else Bank Nifty base will be 100
            spot = round((float(LTP)) / base) * base
            print("Spot Price :",spot)
            """
            Place the order in the money call and put in difference 5 strikes from spot
            """
            strike_difference= 5
            call_strike = spot - (base * strike_difference)
            put_strike = spot + (base * strike_difference)
            exch = "NFO"
            symbol = "NIFTY"
            expiry_date = "29-09-2022"
            print("Call order:",alice.get_instrument_for_fno(exch=exch, symbol=symbol, expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True))
            print("Put order:",alice.get_instrument_for_fno(exch=exch, symbol=symbol, expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False))
            """
            Placing both CE and PE in bracket order
            """
            order1 = {"instrument": alice.get_instrument_for_fno(exch=exch, symbol=symbol, expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True),
                      "order_type": OrderType.Market,
                      "quantity": 1,
                      "transaction_type": TransactionType.Sell,
                      "product_type": ProductType.Intraday,
                      "order_tag": "Strategy Call Order"}
            order2 = {"instrument": alice.get_instrument_for_fno(exch=exch, symbol=symbol, expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False),
                      "order_type": OrderType.Market,
                      "quantity": 1,
                      "transaction_type": TransactionType.Sell,
                      "product_type": ProductType.Intraday,
                      "order_tag": "Strategy Put Order"}
            orders = [order1, order2]
            order_detail =alice.place_basket_order(orders)
            print("Place order details : ",order_detail)

            print("--------------------------------------Stop Loss Initiated--------------------------------------")

            order_history = alice.get_order_history('')
            basket = []
            for i in range(len(order_detail)):
                order_no = order_detail[i]['NOrdNo']
                for j in range(len(order_history)):
                    if order_history[j]['Nstordno'] == order_no:
                        tysm = order_history[j]['Trsym']
                        qty = order_history[j]['Fillshares']
                        exch = order_history[j]['Exchange']
                        trigg = round(float(order_history[j]['Avgprc']) * 1.25)
                        price = round(trigg * 1.05)

                        order = {"instrument": alice.get_instrument_by_symbol(exch, tysm),
                                 "order_type": OrderType.StopLossLimit,
                                 "quantity": qty,
                                 "transaction_type": TransactionType.Buy,
                                 "product_type": ProductType.Intraday,
                                 "price": price,
                                 "trigger_price": trigg,
                                 "order_tag": "Strategy Call Order"}
                        basket.append(order)

            print(alice.place_basket_order(basket))
            print("--------------------------------------Stop Loss Completed--------------------------------------")
            strategy_loop_flag = False
        sleep(1)
    print("--------------------------------------Strategy Ended--------------------------------------")



if __name__ == "__main__":
    socket()
    strategy()
