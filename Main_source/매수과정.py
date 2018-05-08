"""
# open order 체크
open_order_list = my_binance.get_open_orders()
open_order_list_count = len(open_order_list)

# 물고기 매수 주문
if open_order_list_count == 0:  # open order 이 없을 경우
    if fish_list_count == 0:
        print("물고기가 없습니다.")
    elif fish_list_count == 1:  # 물고기 종류 1개
        # 물고기 정보
        fish_entire_data = my_binance.get_ticker(symbol=fish_list[0])

        # 물고기 수량 계산
        fish_volume = fish_entire_data['volume']
        buy_order_quantity = my_balance_btc / float(fish_entire_data['lastPrice'])
        buy_order_quantity = "{0:.3}".format(buy_order_quantity)


        # 주문
        my_binance.order_limit_buy(symbol=fish_list[0],
                                   quantity=buy_order_quantity,
                                   price=fish_entire_data['lastPrice'])

        print(fish_list[0], " 물고기 매수 주문! 가격:", fish_entire_data['lastPrice'], \
              "  ,수량:", buy_order_quantity)

    else:  # 물고기 종류가 2개 이상
        best_quality_fish = fish_list[0]

        # 질이 제일 좋은 물고기 추출(Get max)
        for i in range(0, fish_list_count):
            if my_binance.get_ticker(symbol=fish_list[i])['quoteVolume'] > \
                    my_binance.get_ticker(symbol=best_quality_fish)['quoteVolume']:
                best_quality_fish = fish_list[i]

        fish_entire_data = my_binance.get_ticker(symbol=fish_list[0])

        # 물고기 수량 계산
        fish_volume = fish_entire_data['volume']
        buy_order_quantity = my_balance_btc / float(fish_entire_data['lastPrice'])
        buy_order_quantity = "{0:.3}".format(buy_order_quantity)


        # 주문
        my_binance.order_limit_buy(symbol=fish_list[0],
                                   quantity=buy_order_quantity,
                                   price=fish_entire_data['lastPrice'])

        print(fish_list[0], " 물고기 매수 주문! 가격:", fish_entire_data['lastPrice'], \
              "  ,수량:", buy_order_quantity)

else:
    print("이미 open-order 이 존재합니다.")
"""