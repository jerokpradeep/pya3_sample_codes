from pya3 import *

# User Credential
user_id=''
api_key=''

# Connect and get session Id
alice = Aliceblue(user_id=user_id,api_key=api_key)
alice.get_session_id()

LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []


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
            print(type(feed_message["tk"]))
            if feed_message["tk"] == '243769':
                print(feed_message)

    # Socket Connection Request
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                          socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)

    while not socket_opened:
        pass
    global subscribe_list, unsubscribe_list

    # Subscribe the Instrument
    print("Subscribe :",datetime.now())
    subscribe_list = [alice.get_instrument_by_token('MCX',243769),alice.get_instrument_by_token('MCX',243770)]
    alice.subscribe(subscribe_list)
    sleep(10)
    # print("Unsubscribe :",datetime.now())
    # unsubscribe_list = [alice.get_instrument_by_token("NFO",35018)]
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
    while True:
        # print(LTP)
        sleep(5)


if __name__ == "__main__":
    socket()
    strategy()
