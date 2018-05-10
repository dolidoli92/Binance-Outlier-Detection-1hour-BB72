from datetime import datetime
import secondaryindex
from client import Client
import exceptions
import requests
import sqlite3
import pandas as pd
import time
import csv

# API Key & Secret number / dolidoli92 API
my_binance = Client('NArFy5c2NYFW53j2PRprY0Di5yD7txbC5uqXNfS1EBMAlx0wBt0pmgmTS2YHelsD',
                    '3SkFX4pRDMjxml9YDWUuILLDZe9BlAzfpbfl4zbGgt7HgB6VHG9rRcEMW1Nr4S4U',
                    {"verify": True, "timeout": 20})


#################################################################################################
#          PART1. 프로그램 시작 준비(프로그램 설정/데이터 정리를 위해 기본데이터 수집)                 #
#################################################################################################
print ("--------------------------------------------------------")
print ("dolidoli92 API로 접속합니다.\n")

print ("접     속     시     간  : ",datetime.now().replace(microsecond=0))

all_currencies_count = len(my_binance.get_products()['data']) # 전체 상장 갯수
print ("Binance에 시장상장한 종목 : ",all_currencies_count)

# step1. Get list of currencies & length of currencies
currencies_btc_market = [] # The list of BTC market currencies
currencies_eth_market = [] # The list of ETH market currencies
currencies_bnb_market = [] # The list of BNB market currencies
currencies_usdt_market = [] # The list of USDT market currencies
get_products_data = my_binance.get_products()['data']

for i in range(0,all_currencies_count):
    if get_products_data[i]['symbol'][-3:] == 'BTC':
        currencies_btc_market.append(get_products_data[i]['symbol'])
        #print (get_products_data[i]['symbol'][-3:],"1")
    elif get_products_data[i]['symbol'][-3:] == 'ETH':
        currencies_eth_market.append(get_products_data[i]['symbol'])
        #print (get_products_data[i]['symbol'][-3:],"2")
    elif get_products_data[i]['symbol'][-3:] == 'BNB':
        currencies_bnb_market.append(get_products_data[i]['symbol'])
        #print (get_products_data[i]['symbol'][-3:],"3")
    elif get_products_data[i]['symbol'][-3:] == 'SDT':
        currencies_usdt_market.append(get_products_data[i]['symbol'])
        #print (get_products_data[i]['symbol'][-3:],"4")
    else:
        print ("Cant't classify")

my_BTC_free_balance = float(my_binance.get_asset_balance(asset="BTC")['free'])


print ("BTC  시장 상장 종목 갯수  : ",len(currencies_btc_market))
print ("ETH  시장 상장 종목 갯수  : ",len(currencies_eth_market))
print ("BNB  시장 상장 종목 갯수  : ",len(currencies_bnb_market))
print ("USDT 시장 상장 종목 갯수  : ",len(currencies_usdt_market))
print ("BTC  Balance ( free )   : ",my_BTC_free_balance)

currencies_btc_market_count = len(currencies_btc_market)
currencies_eth_market_count = len(currencies_eth_market)
currencies_bnb_market_count = len(currencies_bnb_market)
currencies_usdt_market_count = len(currencies_usdt_market)

# step2. Making a list for trading
currencies_btc_market_TRDING = [] # The list of BTC market currencies FOR TRADING
currencies_eth_market_TRDING = [] # The list of ETH market currencies FOR TRADING
currencies_bnb_market_TRDING = [] # The list of BNB market currencies FOR TRADING
currencies_usdt_market_TRDING = [] # The list of USDT market currencies FOR TRADING

# 최근 7*15시간 이내에 상장한 종목은 데이터가 없기 때문에 제외
print ("--------------------------------------------------------")
print ("Trading에 활용할 종목들을 선택합니다. 선택은 20초 소요됩니다.\n")


# 최근 15시간 내에 데이터가 없으면, 데이터 부족(안정성)으로 투자 목록에서 제외
# BTC 시장 trading 가능한 종목 추출
for i in range(0, currencies_btc_market_count):
    tmp_hour1_data = my_binance.get_klines(symbol=currencies_btc_market[i],
                                           interval=my_binance.KLINE_INTERVAL_1HOUR,
                                           limit=336)

    if len(tmp_hour1_data) >= 336:
        currencies_btc_market_TRDING.append(currencies_btc_market[i])

# ETH 시장 trading 가능한 종목 추출
for i in range(0, currencies_eth_market_count):
    tmp_hour1_data = my_binance.get_klines(symbol=currencies_eth_market[i],
                                           interval=my_binance.KLINE_INTERVAL_1HOUR,
                                           limit=336)

    if len(tmp_hour1_data) >= 336:
        currencies_eth_market_TRDING.append(currencies_eth_market[i])

# BNB 시장 trading 가능한 종목 추출
for i in range(0, currencies_bnb_market_count):
    tmp_hour1_data = my_binance.get_klines(symbol=currencies_bnb_market[i],
                                           interval=my_binance.KLINE_INTERVAL_1HOUR,
                                           limit=336)

    if len(tmp_hour1_data) >= 336:
        currencies_bnb_market_TRDING.append(currencies_bnb_market[i])

# USDT 시장 trading 가능한 종목 추출
for i in range(0, currencies_usdt_market_count):
    tmp_hour1_data = my_binance.get_klines(symbol=currencies_usdt_market[i],
                                           interval=my_binance.KLINE_INTERVAL_1HOUR,
                                           limit=336)

    if len(tmp_hour1_data) >= 336:
        currencies_usdt_market_TRDING.append(currencies_usdt_market[i])


currencies_btc_market_TRDING_count = len(currencies_btc_market_TRDING)
currencies_eth_market_TRDING_count = len(currencies_eth_market_TRDING)
currencies_bnb_market_TRDING_count = len(currencies_bnb_market_TRDING)
currencies_usdt_market_TRDING_count = len(currencies_usdt_market_TRDING)

all_currencies_TRADING_count = currencies_btc_market_TRDING_count + \
                                currencies_eth_market_TRDING_count + \
                                currencies_bnb_market_TRDING_count + \
                                currencies_usdt_market_TRDING_count

print ("Binance총 가능 종목 갯수  : ",all_currencies_TRADING_count)
print ("BTC  거래 가능 종목 갯수  : ",currencies_btc_market_TRDING_count)
print ("ETH  거래 가능 종목 갯수  : ",currencies_eth_market_TRDING_count)
print ("BNB  거래 가능 종목 갯수  : ",currencies_bnb_market_TRDING_count)
print ("USDT 거래 가능 종목 갯수  : ",currencies_usdt_market_TRDING_count)
print ("--------------------------------------------------------")



# 최소 주문 수량(자릿 수 포함) / 최소 주문 가격(자릿 수 포함) 데이터 저장(dictionary)
"""
최소주문수량(currencies_LOT_SIZE_dict)
i.e.
'ETHBTC': '0.00100000',
'LTCBTC': '0.01000000',
'BNBBTC': '0.01000000',
'NEOBTC': '0.01000000',

최소주문가격(currencies_PRICE_FILTER_dict)
i.e.
'ETHBTC': '0.00000100',
'LTCBTC': '0.00000100',
'BNBBTC': '0.00000010',
'NEOBTC': '0.00000100'
"""
get_exchange_info_data = my_binance.get_exchange_info()['symbols']
currencies_LOT_SIZE_dict = {}
currencies_PRICE_FILTER_dict = {}

print ("LOT_SIZE, PRICE_FILTER 데이터를 받습니다.\n")
for i in range(0, all_currencies_TRADING_count):
    currencies_LOT_SIZE_dict[get_exchange_info_data[i]['symbol']] = \
        get_exchange_info_data[i]['filters'][1]['minQty']
    currencies_PRICE_FILTER_dict[get_exchange_info_data[i]['symbol']] = \
        get_exchange_info_data[i]['filters'][0]['tickSize']

#################################################################################################
#                              PART2. 프로그램 기본데이터 수집                                     #
#################################################################################################
# step1. determine parameter value
outlier_percent = 0 # outlier percent 지정
rate_of_profit = 1.01 # the rate of profit 지정
amount_invest_btc = 0.045 # The amount of investment btc 지정

print ("이 탈 률 : ", outlier_percent*100,"% 로 지정되었습니다.")
print ("수 익 률 : ", "{0:.3f}".format((rate_of_profit-1)*100),"% 로 지정되었습니다.")
print ("투자 BTC : ", "{0:.6f}".format(amount_invest_btc),"로 지정되었습니다.") # 자동적으로 full로 하는 것보다, 직접 적는 것이 좋음
print ("--------------------------------------------------------")

# 최근 7*1시간 기준 시간봉(close) 데이터 만들기( Dictionary of list )
# step2. Load data for algorithm
print ("최근 7*1시간 시간봉 데이터를 로드하고 있습니다. 약 15초의 시간이 소요됩니다.")

hour7_last_data = {}
for i in range(0, currencies_btc_market_TRDING_count):
    tmp_hour1_data = my_binance.get_klines(symbol=currencies_btc_market_TRDING[i],
                                           interval=my_binance.KLINE_INTERVAL_1HOUR,
                                           limit = 7)

    for j in range(0, 7):
        if j == 0:
            hour7_last_data[currencies_btc_market_TRDING[i]] = [float(tmp_hour1_data[j][4])]  # 'Close' data
        else:
            try:
                hour7_last_data[currencies_btc_market_TRDING[i]].append(float(tmp_hour1_data[j][4]))
            except IndexError as e:
                print (e, ",PART2. step1 오류 발생") # 발생하지 않아야 함

print ("최근 7*1시간 시간봉 데이터를 로드를 완료했습니다.")

# 최근 7*15분 기준 15분봉(close) 데이터 만들기( Dictionary of list )
print ("최근 7*15분 15분봉 데이터를 로드하고 있습니다. 약 10초의 시간이 소요됩니다.")

min15_last_data = {}
for i in range(0, currencies_btc_market_TRDING_count):
    tmp_min15_data = my_binance.get_klines(symbol=currencies_btc_market_TRDING[i],
                                           interval=my_binance.KLINE_INTERVAL_15MINUTE,
                                           limit=7)
    for j in range(0, 7):
        if j == 0:
            min15_last_data[currencies_btc_market_TRDING[i]] = [float(tmp_min15_data[j][4])]  # 'Close' data
        else:
            try:
                min15_last_data[currencies_btc_market_TRDING[i]].append(float(tmp_min15_data[j][4]))
            except IndexError as e:
                print(e, ",PART2. step1 오류 발생") # 발생하지 않아야 함


print ("최근 7*15분 15분봉 데이터를 로드를 완료했습니다.\n")
print ("--------------------------------------------------------")

now_second = -1
fish_list_hour1 = {}
fish_list_min15 = {}
buy_order_list = []
sell_order_list = []

#################################################################################################
#                              Part3. 지속적인 알고리즘 반복 수행                                  #
#################################################################################################
while True:
    before_second = now_second
    time_now = datetime.now()  # datetime.datetime(2018, 5, 3, 21, 19, 25, 334686)
    now_second = time_now.second
    now_minute = time_now.minute
    buy_price_order = 0

    # step1.Update the data
    """
    i.e.
    hour7_last_data['ETHBTC'] = [0.071975, 0.072054, 0.072083, 0.07296, 0.072704, 0.072741, 0.073209]

    time_last_data[symbol][6] 을 1초마다 계속적으로 update
    """
    if before_second != now_second:
        try:
            ticker_data = my_binance.get_all_tickers()  # 1 request

            # all_currencies_count
            # all_currencies_TRADING_count
            if len(ticker_data) == all_currencies_count:
                for i in range(0, all_currencies_count):
                    try:
                        if ticker_data[i]['symbol'][-3:] == 'BTC':
                            hour7_last_data[ticker_data[i]['symbol']][6] = float(ticker_data[i]['price'])
                    except KeyError as e:
                        # 새로 상장했을 때, hour7_last_data에 그 종목이 존재하지 않아서 KeyError 발생
                        # print(e, "is current frozen, get_all_ticker() function error")
                        pass
            else:
                # 간혹가다가 get_ticker()에서 모든 데이터를 긁어오지 못하는 경우가 존재
                print("get ticker error, error length", len(ticker_data))


        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, exceptions.BinanceAPIException) as e:
            print("Part2 : Update the data ", e)

    # step2. Rebuild the data in every hour
    if now_minute == 0 and now_second < 8:
        print("\n정각이 되어 데이터를 초기화합니다.\n")
        hour7_last_data = {}
        min15_last_data = {}
        for i in range(0, currencies_btc_market_TRDING_count):
            tmp_hour1_data = my_binance.get_klines(symbol=currencies_btc_market_TRDING[i],
                                                   interval=my_binance.KLINE_INTERVAL_1HOUR,
                                                   limit=7)
            for j in range(0, 7):
                if j == 0:
                    hour7_last_data[currencies_btc_market_TRDING[i]] = [float(tmp_hour1_data[j][4])]  # 'Close' data
                else:
                    hour7_last_data[currencies_btc_market_TRDING[i]].append(float(tmp_hour1_data[j][4]))

            tmp_min15_data = my_binance.get_klines(symbol=currencies_btc_market_TRDING[i],
                                                   interval=my_binance.KLINE_INTERVAL_15MINUTE,
                                                   limit=7)
            for jj in range(0, 7):
                if jj == 0:
                    min15_last_data[currencies_btc_market_TRDING[i]] = [float(tmp_min15_data[jj][4])]  # 'Close' data
                else:
                    min15_last_data[currencies_btc_market_TRDING[i]].append(float(tmp_min15_data[jj][4]))




    # step3. Buy&Sell by algorithm
    if before_second != now_second:
        print ("\n")
        try:
            fish_list_hour1 = {}
            fish_list_min15 = {}
            average_lower_percent = 0
            sum_lower_percent = 0

            for j in range(0, currencies_btc_market_TRDING_count):
                [lower_price_hour1, upper_price_hour1, lower_percent_hour1, upper_percent_hour1] = \
                    secondaryindex.bollinger_bands_percent(hour7_last_data[currencies_btc_market_TRDING[j]])

                sum_lower_percent = sum_lower_percent + lower_percent_hour1

            average_lower_percent = sum_lower_percent/currencies_btc_market_TRDING_count * 100
            average_lower_percent = "{0:.4f}".format(average_lower_percent)
            print ("1시간봉 평균이탈율:",average_lower_percent,"%")

            for i in range(0, currencies_btc_market_TRDING_count):
                try:
                    # 1시간봉 이탈률 계산
                    [lower_price_hour1, upper_price_hour1, lower_percent_hour1, upper_percent_hour1] = \
                        secondaryindex.bollinger_bands_percent(hour7_last_data[currencies_btc_market_TRDING[i]])

                    #################################################################################################
                    #                                       물고기 무게 결정                                          #
                    #################################################################################################
                    if lower_percent_hour1 < outlier_percent:  # 이탈률 지정
                        # 물고기 목록 추가
                        fish_list_hour1[currencies_btc_market_TRDING[i]] = \
                            [lower_price_hour1, upper_price_hour1, lower_percent_hour1, upper_percent_hour1]

                        buy_price_order = lower_price_hour1
                        print("1시간봉 이탈률:", "{0:.3f}".format(lower_percent_hour1 * 100), "%",
                              currencies_btc_market_TRDING[i], " 매수 신호 발생. 시간:",
                              time_now.replace(microsecond=0),
                              "하한선가격:", "{0:.8f}".format(lower_price_hour1),
                              "현재가격:", "{0:.8f}".format(float(hour7_last_data[currencies_btc_market_TRDING[i]][6])),
                              "평균이탈율:",average_lower_percent,"%")



                        with open("H:\\[4] Binance_database\\analysis\\180509-.csv", 'a',encoding='utf-8',newline='') as program_log:
                            program_log_csv = csv.writer(program_log)
                            program_log_csv.writerow(["outlier percent","{0:.3f}".format(lower_percent_hour1 * 100)+"%",
                                                      currencies_btc_market_TRDING[i],"BuySignal","Time",
                                                      time_now.strftime("%Y-%m-%d %H:%M:%S"),
                                                      "Low line Price","{0:.8f}".format(lower_price_hour1),
                                                      "now Price","{0:.8f}".format(float(hour7_last_data[currencies_btc_market_TRDING[i]][6])),
                                                      "Average low percent",average_lower_percent+"%"])
                            program_log.close()

                except KeyError as e:
                    print("KeyError 2424", e)

        except exceptions.BinanceAPIException as e:
            print(e)



