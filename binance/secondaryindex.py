import time
import hmac
import hashlib
import pandas as pd
import sqlite3
import datetime
import math
from bittrex import Bittrex, API_V1_1

# Class 없이 단순히 def만 작성
######################################################################################################
def sum_list(list):
    """
    list의 원소들의 합산을 return 한다.

    input:
    list

    return:
    sum(int)
    """
    mysum = 0
    for i in range(0, len(list)):
        mysum = mysum + list[i]
    return mysum

def moving_average(list):
    """
    list의 평균을 return한다.

    input:
    list

    return:
    average(float)
    """
    mysum = 0
    for i in range(0, len(list)):
        mysum = mysum + list[i]

    return mysum / len(list)

def bollinger_bands_percent(list):
    """
    Bollinger Bands를 period에 계산하고, 하한선과 상한선을 뱉는다.

    input:
    list
    리스트의 갯수가 period로 직결
    e.g) len(list) = 7 이면, 7period에 2sigma 활용으로 지표 작성

    return:
    bands lower index
    bands upper index
    bands lower percent
    bands upper percent
    percent는 (-)가 되었을 때, 이탈한 것으로 판단

    input:
    list,period

    return:
    list[하한선,상한선]
    """
    list_MA = moving_average(list)
    list_length = len(list)

    stddev_sum = 0
    for i in range(0, list_length):
        stddev_sum = stddev_sum + (list[i] - list_MA) * (list[i] - list_MA)
    stddev = math.sqrt(stddev_sum / list_length)

    return [list_MA - 2 * stddev, list_MA + 2 * stddev,
            ((list[list_length - 1]) / (list_MA - 2 * stddev)) - 1,
            1 - ((list[list_length - 1]) / (list_MA + 2 * stddev))]

def RSI(list):
    """
    Relative Strength Index
    1. 가격이 전일 가격보다 상승한 날의 상승분은 U(up) 값이라고 하고,
    2. 가격이 전일 가격보다 하락한 날의 하락분은 D(down) 값이라고 한다.
    3. U값과 D값의 평균값을 구하여 그것을 각각 AU(average ups)와 AD(average downs)라 한다.
    4. AU를 AD값으로 나눈 것을 RS(relative strength) 값이라고 한다.
       RS 값이 크다는 것은 일정 기간 하락한 폭보다 상승한 폭이 크다는 것을 의미한다.
    5. 다음 계산에 의하여 RSI 값을 구한다.

    RSI = RS / (1 + RS)
    RSI = AU / (AU + AD)
    """
    list_length = len(list)
    u_list = []
    u_sum = 0
    d_list = []
    d_sum = 0

    try:
        for i in range(1, list_length):
            if (list[i] > list[i - 1]):  # 전일 가격보다 상승한 날
                u_list.append((list[i] - list[i - 1]))
                u_sum = u_sum + (list[i] - list[i - 1])
            elif (list[i] < list[i - 1]):  # 전일 가격보다 하락한 날
                d_list.append((list[i - 1] - list[i]))
                d_sum = d_sum + (list[i - 1] - list[i])
            else:
                pass

        if len(u_list) == 0:
            return 0
        else:
            AU = u_sum / len(u_list)

        if len(d_list) == 0:
            AD = 0
        else:
            AD = d_sum / len(d_list)

        return AU / (AU + AD)
    except ZeroDivisionError as e:
        return 0



def sum_list_for_datalist(list):
    """
    DB에 저장할 때, 기준일로부터 과거 데이터가 존재하지 않을 경우에는
    0을 return 한다.

    :param list:
    :return: float or int
    """
    mysum = 0
    for i in range(0, len(list)):
        if list[i] == 0:
            return 0

        mysum = mysum + list[i]
    return mysum


def moving_average_for_datalist(list):
    """
    DB에 저장할 때, 기준일로부터 과거 데이터가 존재하지 않을 경우에는
    0을 return 한다.

    :param list:
    :return: float or int
    """
    mysum = 0
    for i in range(0, len(list)):
        if list[i] == 0:
            return 0

        mysum = mysum + list[i]

    return mysum / len(list)


def bollinger_bands_percent_for_datalist(list):
    """
    DB에 저장할 때, 기준일로부터 과거 데이터가 존재하지 않을 경우에는
    0을 return 한다.

    :param list:
    :return: float or int
    """
    list_MA = moving_average_for_datalist(list)
    list_length = len(list)

    if list_MA == 0:
        return [0,0,0,0]

    stddev_sum = 0
    for i in range(0, list_length):
        stddev_sum = stddev_sum + (list[i] - list_MA) * (list[i] - list_MA)
    stddev = math.sqrt(stddev_sum / list_length)

    return [list_MA - 2 * stddev, list_MA + 2 * stddev,
            ((list[list_length - 1]) / (list_MA - 2 * stddev)) - 1,
            1 - ((list[list_length - 1]) / (list_MA + 2 * stddev))]

def stddev_for_datalist(list):
    list_MA = moving_average_for_datalist(list)
    list_length = len(list)

    if list_MA == 0:
        return 0

    stddev_sum = 0
    for i in range(0, list_length):
        stddev_sum = stddev_sum + (list[i] - list_MA) * (list[i] - list_MA)
    stddev = math.sqrt(stddev_sum / list_length)

    return stddev




def RSI_for_datalist(list):
    """
    DB에 저장할 때, 기준일로부터 과거 데이터가 존재하지 않을 경우에는
    0을 return 한다.

    :param list:
    :return: float or int
    """
    list_length = len(list)
    u_list = []
    u_sum = 0
    d_list = []
    d_sum = 0

    for se in range(0,list_length):
        if list[se] == 0:
            return 0

    try:
        for i in range(1, list_length):
            if (list[i] > list[i - 1]):  # 전일 가격보다 상승한 날
                u_list.append((list[i] - list[i - 1]))
                u_sum = u_sum + (list[i] - list[i - 1])
            elif (list[i] < list[i - 1]):  # 전일 가격보다 하락한 날
                d_list.append((list[i - 1] - list[i]))
                d_sum = d_sum + (list[i - 1] - list[i])
            else:
                pass

        if len(u_list) == 0:
            AU = 0
        else:
            AU = u_sum / len(u_list)

        if len(d_list) == 0:
            AD = 0
        else:
            AD = d_sum / len(d_list)

        return AU / (AU + AD)
    except ZeroDivisionError as e:
        return 0





































if __name__ == '__main__':
    my_bittrex = Bittrex('5bb30ffc7d524752b66c47a778c01b14',
                         '8ca5bd574ff5442db26ac1fc66678c1c'
                         , api_version=API_V1_1)

    while (True):
        time.sleep(1)

        try:
            ADA = int(my_bittrex.get_market_summary('BTC-ADA')['result'][0]['Last'] * 100000000)
            SC = int(my_bittrex.get_market_summary('BTC-SC')['result'][0]['Last'] * 100000000)
            XLM = int(my_bittrex.get_market_summary('BTC-XLM')['result'][0]['Last'] * 100000000)
            TRX = int(my_bittrex.get_market_summary('BTC-TRX')['result'][0]['Last'] * 100000000)
            XVG = int(my_bittrex.get_market_summary('BTC-XVG')['result'][0]['Last'] * 100000000)
            BAT = int(my_bittrex.get_market_summary('BTC-BAT')['result'][0]['Last'] * 100000000)

            BTC_ADA = [3241, 3227, 3200, 3192, 3188, 3197, ADA]
            BTC_SC = [236, 236, 235, 232, 232, 229, SC]
            BTC_XLM = [4385, 4408, 4310, 4309, 4288, 4453, XLM]
            BTC_TRX = [601, 596, 588, 587, 594, 595, TRX]
            BTC_XVG = [753, 773, 748, 752, 840, 914, XVG]
            BTC_BAT = [4430, 4646, 4433, 4460, 4414, 4344, BAT]

            print(bollinger_bands_percent(BTC_ADA))
            print(bollinger_bands_percent(BTC_SC))
            print(bollinger_bands_percent(BTC_XLM))
            print(bollinger_bands_percent(BTC_TRX))
            print(bollinger_bands_percent(BTC_XVG))
            print(bollinger_bands_percent(BTC_BAT))
            print('\n')
        except:
            time.sleep(1)
            ADA = int(my_bittrex.get_market_summary('BTC-ADA')['result'][0]['Last'] * 100000000)
            SC = int(my_bittrex.get_market_summary('BTC-SC')['result'][0]['Last'] * 100000000)
            XLM = int(my_bittrex.get_market_summary('BTC-XLM')['result'][0]['Last'] * 100000000)
            TRX = int(my_bittrex.get_market_summary('BTC-TRX')['result'][0]['Last'] * 100000000)
            XVG = int(my_bittrex.get_market_summary('BTC-XVG')['result'][0]['Last'] * 100000000)
            BAT = int(my_bittrex.get_market_summary('BTC-BAT')['result'][0]['Last'] * 100000000)

            BTC_ADA = [3241, 3227, 3200, 3192, 3188, 3197, ADA]
            BTC_SC = [236, 236, 235, 232, 232, 229, SC]
            BTC_XLM = [4385, 4408, 4310, 4309, 4288, 4453, XLM]
            BTC_TRX = [601, 596, 588, 587, 594, 595, TRX]
            BTC_XVG = [753, 773, 748, 752, 840, 914, XVG]
            BTC_BAT = [4430, 4646, 4433, 4460, 4414, 4344, BAT]

            print(bollinger_bands_percent(BTC_ADA))
            print(bollinger_bands_percent(BTC_SC))
            print(bollinger_bands_percent(BTC_XLM))
            print(bollinger_bands_percent(BTC_TRX))
            print(bollinger_bands_percent(BTC_XVG))
            print(bollinger_bands_percent(BTC_BAT))
            print('\n')

