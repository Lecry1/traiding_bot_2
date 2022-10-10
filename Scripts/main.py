import time
import numpy as np
import talib
import datetime
from binance.client import Client

TIME_FRAME = "30m"  # 30 minutes
period = 200
BUY = "BUY"
SELL = "SELL"
all_coin = ['BNBUSDT', 'ROSEUSDT', 'SKLUSDT', 'GALAUSDT', 'LPTUSDT', 'LTCUSDT', 'NEOUSDT', 'RVNUSDT', 'IOTXUSDT',
            'HBARUSDT', 'FTMUSDT', 'GRTUSDT', 'GTCUSDT', 'ARUSDT', 'ANTUSDT', 'DUSKUSDT', 'EOSUSDT',
            'ONEUSDT', 'AXSUSDT', 'BAKEUSDT', 'BLZUSDT', 'SANDUSDT', 'COMPUSDT']
# этот список нужен для того чтобы несколько раз непереставлять стопп лос после активации лимитки(мне было лень писать цикл)))) )
lossActivate = {'BNBUSDT': False, 'ROSEUSDT': False, 'SKLUSDT': False, 'GALAUSDT': False, 'LPTUSDT': False,
                'LTCUSDT': False, 'NEOUSDT': False, 'RVNUSDT': False, 'IOTXUSDT': False,
                'HBARUSDT': False, 'FTMUSDT': False, 'GRTUSDT': False, 'GTCUSDT': False, 'ARUSDT': False,
                'ANTUSDT': False, 'DUSKUSDT': False, 'EOSUSDT': False,'ONEUSDT': False, 'AXSUSDT': False,
                'BAKEUSDT': False, 'BLZUSDT': False, 'SANDUSDT': False,'COMPUSDT': False}
# удалил 'SHIBUSDT' так как его символ 1000SHIBUSDT а это чисто условие под него загонять

# надо сделать так чтобы после выполнения лимитки переустанавливался TP для того чтобы не было проблемы Order would immediately trigger.

flag = True
orderStatus = False  # в поиске да\нет
flag_limit = False  # открыта ли лимитка
activeSymbol = "BTCUSDT"
currentSymbol = "BTCUSDT"
tradingAmount = 11  # сумма на которую торгуемся
i = 0

f = open('config.txt', 'r')
api_key, secret_key = f.read().split()
f.close()
client = Client(api_key, secret_key, testnet=False)


def couples():  # функция выполняет поиск всех пар к USDT и возвращает множество
    ticket = client.get_margin_all_pairs()  # список фьчерсных монет, НО ЭТО НЕ ТОЧНО
    pairs = list()
    for index in range(len(ticket)):  # пробегаем по всем монетам
        static = ticket[index]  # присваиваем словарь из ticker
        symbol = static.setdefault("symbol")  # присваиваем symbol значение ключа "symbol" из ticker
        if "USDT" in symbol:  # есть ли в symbol USDT? или через срез , допустим symbol =BTCUSDT обрезаем[-4:]
            # получаем USDT
            pairs.append(symbol)
    return pairs


def cheak_status_order(actSymbol):
    global flag_limit
    global orderStatus
    status = False

    # есть ли лимитка
    listik = client.futures_get_open_orders(symbol=actSymbol)
    print(
        f"проверка статуса ордера {actSymbol} price_order2: {price_order_2state} tp: {take_profit} кол-во ордеров {len(listik)}")
    for ch in listik:
        if ch["type"] == "LIMIT":
            flag_limit = True
            orderStatus = True
            break
        else:
            flag_limit = False

    if len(listik) == 1 or len(listik) == 0:
        client.futures_cancel_all_open_orders(symbol=actSymbol)
        orderStatus = False
        flag_limit = False
        status = False
        d.pop(actSymbol, 20)
        f = open('saveDataPosition.txt', 'r')
        data = f.readlines()
        stre = ''
        for b in data:
            if actSymbol in b:
                indexs = data.index(b)
                data.pop(indexs)
                for a in data:
                    stre += a
                f = open('saveDataPosition.txt', 'w')
                f.write(stre)
                break
        f.close()
        lossActivate[actSymbol] = False
        print(f"закрытие всех позиций по {actSymbol} + появляется доступ к открытию сделки1")

    elif len(listik) == 2:
        if flag_limit == True:
            client.futures_cancel_all_open_orders(symbol=actSymbol)
            orderStatus = False
            flag_limit = False
            status = False
            d.pop(actSymbol)
            f = open('saveDataPosition.txt', 'r')
            data = f.readlines()
            stre = ''
            for b in data:
                if actSymbol in b:
                    indexs = data.index(b)
                    data.pop(indexs)
                    for a in data:
                        stre += a
                    f = open('saveDataPosition.txt', 'w')
                    f.write(stre)
                    break
            f.close()
            lossActivate[actSymbol] = False
            print(f"закрытие всех позиций по {actSymbol} + появляется доступ к открытию сделки2")
        else:
            if lossActivate[actSymbol] == False:
                try:
                    print("переносим стопп лоосс")
                    client.futures_cancel_all_open_orders(symbol=actSymbol)
                    client.futures_create_order(symbol=actSymbol, side=side_pos, type="TAKE_PROFIT_MARKET",
                                                stopPrice=round(take_profit, pricePrecision[actSymbol]),
                                                closePosition="true")
                    client.futures_create_order(symbol=actSymbol, side=side_pos, type="STOP_MARKET",
                                                stopPrice=round(price_order_2state, pricePrecision[actSymbol]),
                                                closePosition="true")
                    status = True
                    lossActivate[actSymbol] = True
                except Exception:
                    lossActivate[actSymbol] = False
                    print("Order would immediately trigger.")
            orderStatus = True
    elif len(listik) == 3:
        if flag_limit == True:
            orderStatus = True
            status = True
        else:
            client.futures_cancel_all_open_orders(symbol=actSymbol)
            orderStatus = False
            flag_limit = False
            status = False
            d.pop(actSymbol)
            f = open('saveDataPosition.txt', 'r')
            data = f.readlines()
            stre = ''
            for b in data:
                if actSymbol in b:
                    indexs = data.index(b)
                    data.pop(indexs)
                    for a in data:
                        stre += a
                    f = open('saveDataPosition.txt', 'w')
                    f.write(stre)
                    break
            f.close()
            lossActivate[actSymbol] = False
            print(f"закрытие всех позиций по {actSymbol} + появляется доступ к открытию сделки3")
            lossActivate[actSymbol] = False
            status = False
    time.sleep(2)
    print(f"orderStatus {orderStatus} and flag_limit {flag_limit}")
    return status


def get_data(data, value):  # получение исторических данных клина
    return_data = []  # создаём список return_data
    for each in data:  # проходим по листу и т.к. это for то мы присваеваем each  значение res
        return_data.append(float(each[value]))  # закрытие свечи находиться в 5ой ячейке поэтому добавляем в лист
    return np.array(return_data)  # создаем массив и возращаем


def macd_custom(source, fast_length, slow_length, signal_length):
    fastMA = talib.EMA(source, fast_length)  #
    slowMA = talib.EMA(source, slow_length)  #
    macd = fastMA - slowMA  # out_macd кординаты линии магди которая толстая
    signal = talib.SMA(macd, signal_length)  # outSignal Кординаты сигнальной тонкой линии
    if (macd[-2] > signal[-2] and signal[-1] > macd[-1]) or \
            (macd[-3] > signal[-3] and signal[-1] == macd[-1] and signal[-1] > macd[-1]):
        # если быстрая скользящая пересекает медленную , то это сигнал в шорт
        position_state = "short"
    elif (signal[-2] > macd[-2] and macd[-1] > signal[-1]) or (
            signal[-3] > macd[-3] and macd[-2] == signal[-2] and macd[-1] > signal[-1]):
        # если медленная пересекает быструю , то это сигнал в лонг
        position_state = "long"
    else:
        position_state = "none"
    if macd[-1] > 0 and signal[-1] > 0:
        where_intersection = "high"
    elif macd[-1] < 0 and signal[-1] < 0:
        where_intersection = "low"
    else:
        where_intersection = "none"
    return where_intersection, position_state


def super_trend(hight, low, close):  # atr = p
    periods = 10
    multiplier = 1.5
    atr = list(talib.ATR(hight, low, close, timeperiod=periods))
    trend = 1
    up_b = (hight[15] + low[15]) / 2 - (multiplier * atr[15])
    dn_b = (hight[15] + low[15]) / 2 + (multiplier * atr[15])
    for i in range(15, len(hight)):
        a = i - 1
        src = (hight[i] + low[i]) / 2  # текущее среднее бара

        up = src - (multiplier * atr[i])
        up1 = up_b
        if close[a] > up1:
            up_b = max(up, up1)
        else:
            up_b = up
        dn = src + (multiplier * atr[i])
        dn1 = dn_b
        if close[a] < dn1:
            dn_b = min(dn, dn1)
        else:
            dn_b = dn
        if trend == -1 and close[i] > dn1:
            trend = 1
        else:
            if trend == 1 and close[i] < up1:
                trend = -1

    return trend, up_b, dn_b


def base(ema, where_intersection, state_macd, trend, dn_lose, up_lose, price_now):
    take_profit = 0
    limit_orderPrice = 0
    if where_intersection == "low" and state_macd == "long" and trend == 1 and price_now > ema:  # открытие позиции лонг установка стопп лосс и тейк профит и 25 процентов закрыть надо
        take_profit = price_now * (100 + (price_now / dn_lose * 100 - 100) * 1.5) / 100
        limit_orderPrice = price_now * (price_now / dn_lose * 100) / 100
        position_order = BUY
    elif where_intersection == "high" and state_macd == "short" and trend == -1 and price_now < ema:  # открытие позиции шорт установка стопп лосс и тейк профит
        take_profit = price_now * (100 - (up_lose / price_now * 100 - 100) * 1.5) / 100
        limit_orderPrice = price_now * (100 - (up_lose / price_now * 100 - 100)) / 100
        position_order = SELL
    else:  # error
        position_order = "empty"

    return position_order, dn_lose, up_lose, take_profit, limit_orderPrice, price_now


def start():
    current_minutes = int(int(time.time() / 60) % 60)
    counter = 0
    List1 = [symbol for symbol in all_coin]  # заполняем массив тем кол-вом монет котороые в all_coin
    if current_minutes in range(28, 32) or current_minutes in range(58, 60):
        print('не попали в диапозон')
        time.sleep(200)
        for symbol in all_coin:
            king_res = client.get_klines(symbol=symbol, interval=TIME_FRAME, limit=1000)  # получаем листы в листах
            List1[counter] = king_res
            counter += 1
    else:
        print('в диапозоне')
        for symbol in all_coin:
            king_res = client.get_klines(symbol=symbol, interval=TIME_FRAME, limit=1000)  # получаем листы в листах
            List1[counter] = king_res
            counter += 1
    print("закончили первую запись в массив")
    return List1


def quantity_round_solve():
    qty = {}
    price_pre = {}
    ticksize = {}
    ticket = client.futures_exchange_info()['symbols']
    for index in ticket:
        if "USDT" in index["symbol"]:
            qty[index["symbol"]] = index['filters'][1]['minQty']
            price_pre[index["symbol"]] = index['pricePrecision']
            ticksize[index["symbol"]] = index['filters'][0]['tickSize']
    return qty, price_pre, ticksize


def open_order(active_Symbol, side, opposite_side, stop_loss, takeprofit, quan, limitquantity, limitorderprice,
               roundPrice_order, ticksize):
    global orderStatus
    global flag_limit
    client.futures_cancel_all_open_orders(symbol=active_Symbol)
    client.futures_create_order(symbol=active_Symbol, side=side, type='MARKET', quantity=quan)
    time.sleep(3)
    client.futures_create_order(symbol=active_Symbol, side=opposite_side, type="STOP_MARKET",
                                stopPrice=round(stop_loss, roundPrice_order), closePosition="true")
    client.futures_create_order(symbol=active_Symbol, side=opposite_side, type="TAKE_PROFIT_MARKET",
                                stopPrice=round(takeprofit, roundPrice_order),
                                closePosition="true")
    client.futures_create_order(symbol=active_Symbol, side=opposite_side, type="LIMIT", quantity=limitquantity,
                                price=round(limitorderprice // float(ticksize) * float(ticksize), 9), timeInForce="GTC",
                                reduceOnly="true")
    orderStatus = True
    flag_limit = True


def cheak(dtclose, lose, dtamax, dtmin, side, dtopen, symbolOrder):
    ccxetchick = 0
    ema200 = talib.EMA(dtclose, period)[-15:]
    for j in range(1, 11):
        if dtamax[-j] > ema200[-j] and dtmin[-j] < ema200[-j]:
            ccxetchick += 1
    max200 = max(ema200)
    min200 = min(ema200)
    ema = talib.EMA(dtclose, period)[-1]
    move_price = True
    suma = 0
    for i in range(0, len(dtclose)):
        suma += abs(dtclose[i] - dtopen[i])
    avarage_move = suma
    where_stop = 0
    far_ema = 0
    if side == BUY:
        where_stop = (dtclose[-1] / lose * 100 - 100) < 2.25  # далеко ли стоп
        far_ema = (dtclose[-1] / ema * 100 - 100) < 10
        for i in range(1, 5):  # от -1 первой свечи до -4
            if dtclose[-i] - dtopen[-i] * 1.2 > avarage_move:
                move_price = False
                break
    elif side == SELL:
        where_stop = (lose / dtclose[-1] * 100 - 100) < 2.25  # далеко ли стоп
        far_ema = (ema / dtclose[-1] * 100 - 100) < 10
        for i in range(1, 5):  # от -1 первой свечи до -4
            if dtopen[-i] - dtclose[-i] * 1.2 > avarage_move:
                move_price = False
                break
    intersection_with_ema = ccxetchick < 4
    move_ema_bok = (max200 / min200 * 100 - 100) > 0.13

    flagrepitOrder = True
    keys = d.keys()
    for a in keys:
        if symbolOrder == a:
            flagrepitOrder = False
            break
    chek_result = where_stop and intersection_with_ema and move_ema_bok and far_ema and move_price and flagrepitOrder
    print("cheak:", where_stop, intersection_with_ema, move_ema_bok, far_ema, move_price, flagrepitOrder)
    return chek_result


qty, pricePrecision, ticksize = quantity_round_solve()
mainList = start()

# ----------------------проверка сделок после отключения--------------
f = open('saveDataPosition.txt', 'r')
listochek = f.read().split("\n")
listochek_2 = listochek.copy()
print(listochek)
d = {}
stre = ''
if listochek[0] == '':
    print("не обнаружене в памяти открытые сделки")
else:
    for kek in listochek:
        if not kek == "":
            secondList = kek.split()
            print(kek)
            currentSymbol, take_profit, price_order_2state, side_pos, position = secondList
            take_profit = float(take_profit)
            price_order_2state = float(price_order_2state)
            if cheak_status_order(currentSymbol):
                d[secondList[0]] = [take_profit, price_order_2state, side_pos, position]
            else:
                indexs = listochek_2.index(kek)
                listochek_2.pop(indexs)
        else:
            indexs = listochek_2.index(kek)
            listochek_2.pop(indexs)
for a in listochek_2:
    if not a == listochek_2[-1]:
        stre += a + "\n"
    else:
        stre += a
f = open('saveDataPosition.txt', 'w')
f.write(stre)
f.close()
# -------------------------------------------------------------------
print("старт")

while flag:
    # --------------первоначальные найстройки-----------------------
    Time = time.time()  # кол во секунд вообще
    secondsNow = int(Time % 60)  # текущее кол во секунд
    current_minutes = int(Time / 60 % 60)  # текущее время минут
    hour = int(Time / 3600 + 3) % 24  # текущий час
    if current_minutes in range(1, 28) and current_minutes in range(31,
                                                                    58):  # делаем задержку дабы не работать каждую тик
        time.sleep(59)
    if current_minutes == 30 or current_minutes == 0:
        time.sleep(4)  # спим так как время пула отстаёт
        # ----------------------баланс-----------------------------------
        balance = float(client.futures_account_balance()[6]['balance'])
        if balance > 11:
            tradingAmount = balance
            amount_of_deals = 5
        else:
            amount_of_deals = (balance - 1) // 1.15
        # --------------------------обновляем лист---------------------
        print("обновление листа")
        for SYMBOL in all_coin:
            res = client.get_klines(symbol=SYMBOL, interval=TIME_FRAME, limit=2)  # получаем листы в листах
            now_list = mainList[i]
            del now_list[0]
            now_list.append(res[-2])
            mainList[i] = now_list
            i += 1
        i = 0
        # --------проверка изменился ли супер тренд-----------------

        # key = d.keys()
        # d2 = d.copy()
        # for g in d2:
        #     cheak_status_order(g)
        #     if orderStatus == True:  # проверка изменился ли супер тренд
        #         Value = mainList[all_coin.index(g)]
        #         dt_hight = get_data(Value, 2)
        #         dt_low = get_data(Value, 3)
        #         dt_close = get_data(Value, 4)
        #         trend, dn_lose, up_lose = super_trend(dt_hight, dt_low, dt_close)
        #         print("проверка супертренда, trend:", trend)
        #         if position == BUY and trend == -1:
        #             qtyy = quantity
        #             if flag_limit == False:
        #                 qtyy = quantity - limit_quantity
        #             client.futures_create_order(symbol=g, side=SELL, type='MARKET', quantity=qtyy)
        #             client.futures_cancel_all_open_orders(symbol=g)
        #             flag_limit = False
        #             orderStatus = False
        #             lossActivate[g] = False
        #         if position == SELL and trend == 1:
        #             qtyy = quantity
        #             if flag_limit == False:
        #                 qtyy = quantity - limit_quantity
        #             client.futures_create_order(symbol=g, side=BUY, type='MARKET', quantity=qtyy)
        #             client.futures_cancel_all_open_orders(symbol=g)
        #             flag_limit = False
        #             orderStatus = False
        #             lossActivate[g] = False

        # --------------------------анализ--------------------------
        print("анализ")
        file = open("log_order.txt", "a")
        dt = datetime.datetime.now()
        dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
        for nowValue in mainList:
            dt_open = get_data(nowValue, 1)
            dt_hight = get_data(nowValue, 2)
            dt_low = get_data(nowValue, 3)
            dt_close = get_data(nowValue, 4)
            ematalib = talib.EMA(dt_close, period)
            intersection, state = macd_custom(dt_close, 12, 26, 9)  # intersection - пересечение , state - лонг,шорт
            trend, dn_lose, up_lose = super_trend(dt_hight, dt_low, dt_close)
            position, dn_stopLose, up_stopLose, take_profit, limit_order_price, price_order_2state = base(
                ematalib[-1], intersection, state, trend, dn_lose, up_lose, dt_close[-1])
            activeSymbol = all_coin[i]
            qty_active = float(qty[activeSymbol])
            quantity = round(tradingAmount / dt_close[-1] // qty_active * qty_active, 9)
            limit_quantity = round((quantity * 0.25 // qty_active) * qty_active, 9)
            # -------------------------------------------основа-------------------------------------------
            if position == BUY:  # покупаем ,стопы
                print(activeSymbol, position, dn_stopLose, up_stopLose, take_profit, limit_order_price, dt_close[-1])
                print("ema " + str(ematalib[-1]) + " trend " + str(trend))
                cheaking = cheak(dt_close, dn_lose, dt_hight, dt_low, BUY, dt_open, activeSymbol)
                if cheaking:  # проверка на кол-во процентов
                    file.write(f"{activeSymbol} LONG {dt_string}" + "\n")
                    if len(d) < amount_of_deals and quantity > 0 and limit_quantity > 0:
                        open_order(activeSymbol, BUY, SELL, dn_lose, take_profit, quantity, limit_quantity,
                                   limit_order_price, pricePrecision[activeSymbol], ticksize[activeSymbol])
                        side_pos = SELL
                        f = open('saveDataPosition.txt', 'a')
                        f.write(f"{activeSymbol} {take_profit} {price_order_2state} {side_pos} {position}\n")
                        f.close()
                        print(f"открытие сделки в ЛОНГ стоп{dn_lose} ,тейк профит{take_profit}")
                        currentSymbol = activeSymbol
                        d[currentSymbol] = [take_profit, price_order_2state, side_pos, position]

            elif position == SELL:  # продаём, стопы
                print(activeSymbol, position, dn_stopLose, up_stopLose, take_profit, limit_order_price, dt_close[-1])
                print("ema " + str(ematalib[-1]) + " trend " + str(trend))
                cheaking = cheak(dt_close, up_lose, dt_hight, dt_low, SELL, dt_open, activeSymbol)
                if cheaking:
                    file.write(f"{activeSymbol} SHORT {dt_string}" + "\n")
                    if len(d) < amount_of_deals and quantity > 0 and limit_quantity > 0:
                        open_order(activeSymbol, SELL, BUY, up_lose, take_profit, quantity, limit_quantity,
                                   limit_order_price, pricePrecision[activeSymbol], ticksize[activeSymbol])
                        side_pos = BUY
                        f = open('saveDataPosition.txt', 'a')
                        f.write(f"{activeSymbol} {take_profit} {price_order_2state} {side_pos} {position}\n")
                        f.close()
                        print(f"открытие сделки в ШОРТ стоп{up_lose} ,тейк профит{take_profit}")
                        currentSymbol = activeSymbol
                        d[currentSymbol] = [take_profit, price_order_2state, side_pos, position]
            i += 1
        f = open('saveDataPosition.txt', 'r')
        data = f.read().split("\n")
        data2 = data.copy()
        stre = ''
        for b in data:
            if '' == b:
                indexs = data2.index(b)
                data2.pop(indexs)
        for a in data2:
            if not a == data[-1]:
                stre += a + '\n'
            else:
                stre += a
        f.close()
        f = open('saveDataPosition.txt', 'w')
        f.write(stre)
        f.close()
        file.close()
        i = 0
        time.sleep(60)
        print(f"{dt_string}")

    if (
            current_minutes == 29 or current_minutes == 59 or current_minutes == 10 or current_minutes == 20 or current_minutes == 40 or current_minutes == 50) and secondsNow == 1  and len(
        d) > 0:
        print(f"{hour} : {current_minutes}")
        key = d.keys()
        d2 = d.copy()
        for g in d2:
            take_profit, price_order_2state, side_pos, position = d2[g]
            take_profit = float(take_profit)
            price_order_2state = float(price_order_2state)
            cheak_status_order(g)