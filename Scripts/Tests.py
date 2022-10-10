# from binance.client import Client
# import time
# import talib
# import numpy as np
# import math
# client = Client("8GgdsLXJAkS9vV10yWAwe523WQvul6sgMSD4cnO8f2PXPOgHJAuZXFU2pz5wsP8z",
#                 "50SeAQd2S82bjVZn1tABBImjtiznbta0UzsXg1af9mjh5bBuUtyzCucWy0HWySyG", testnet=True)
# SELL = 'SELL'
# BUY = 'BUY'
# period = 200
# TIME_FRAME = "30m"
# all_coin = ['BNBUSDT', 'TRXUSDT', 'XRPUSDT', 'EOSUSDT', 'LINKUSDT', 'ONTUSDT', 'ADAUSDT', "ATAUSDT", 'ETCUSDT',
#             'LTCUSDT', 'XLMUSDT', 'XMRUSDT', 'NEOUSDT', 'ATOMUSDT', 'DASHUSDT', 'ZECUSDT', 'MATICUSDT', 'BATUSDT',
#             'IOSTUSDT', 'VETUSDT', 'QTUMUSDT', 'IOTAUSDT', 'XTZUSDT', 'BCHUSDT', 'RVNUSDT', 'ZILUSDT', 'ONEUSDT',
#             'ANKRUSDT', 'IOTXUSDT', 'HBARUSDT', 'FTMUSDT', 'SXPUSDT', 'DOTUSDT', 'ALGOUSDT', 'THETAUSDT', 'COMPUSDT',
#             'KNCUSDT', 'OMGUSDT', 'KAVAUSDT', 'DOGEUSDT', 'WAVESUSDT', 'SNXUSDT', 'CRVUSDT', 'SUSHIUSDT', 'UNIUSDT',
#             'MANAUSDT', 'AVAXUSDT', 'NEARUSDT', 'FILUSDT', 'SRMUSDT', 'AAVEUSDT', 'SANDUSDT', 'CHZUSDT', 'COTIUSDT',
#             'CHRUSDT', 'GRTUSDT', 'LRCUSDT', 'KSMUSDT', 'ROSEUSDT', 'REEFUSDT', 'ENJUSDT', 'RUNEUSDT', 'SKLUSDT',
#             'EGLDUSDT', '1INCHUSDT', 'SOLUSDT', 'LINAUSDT', 'GTCUSDT', 'AUDIOUSDT', 'DENTUSDT', 'FTTUSDT', 'ARUSDT',
#             'DYDXUSDT', 'UNFIUSDT', 'AXSUSDT', 'ENSUSDT', 'ALICEUSDT', 'C98USDT', 'FLOWUSDT', 'BAKEUSDT',
#             'GALAUSDT', 'DARUSDT', 'ANTUSDT', 'BNXUSDT', 'KLAYUSDT', 'JASMYUSDT', 'LPTUSDT', 'DUSKUSDT', 'HOTUSDT',
#             'SFPUSDT', 'ICXUSDT', 'CELOUSDT', 'BLZUSDT', 'MTLUSDT', 'PEOPLEUSDT', 'HNTUSDT', 'CVCUSDT', 'GMTUSDT',
#             'APEUSDT', 'API3USDT', 'CTKUSDT', 'WOOUSDT', 'OPUSDT']
# def quantity_round_solve():
#     qty = {}
#     price_pre = {}
#     ticksize = {}
#     ticket = client.futures_exchange_info()['symbols']
#     for index in ticket:
#         if "USDT" in index["symbol"]:
#             qty[index["symbol"]] = index['filters'][1]['minQty']
#             price_pre[index["symbol"]] = index['pricePrecision']
#             ticksize[index["symbol"]] = index['filters'][0]['tickSize']
#     return qty, price_pre, ticksize

import websocket

def on_message(_wsa,data):
    print(data,"\n\n")
symbol = "BNBUSDT".lower()

print(symbol)
stream_name = "%s@kline_30m" % symbol
wss = "wss://fstream.binance.com/ws/%s" % stream_name
wsa = websocket.WebSocketApp(wss,on_message=on_message)
wsa.run_forever()
print("hipe")