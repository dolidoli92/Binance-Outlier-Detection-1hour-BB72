# Binance-Outlier-Detection

Detect the outlier in Bollinger bands(7period, 2sigma)

You can configurate 'outlier_percent'

***
## Details on Program

1. Select the currencies except listed in 2 weeks 
  - Because it is so dangerous to catch a fluctuation<br /><br /><br />
 
2. Can configurate the Outlier percetage
  - i.e. 0%, input : 0.005%(real : 0.5%) ...<br /><br /><br />

3. If there are outliers, save the data to csv file
  - Outlier is found by 1h*7
  - From now, call the data in 7 hours, for example,
    now : 15:28
    data : 9:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:28
  - Therefore, it is not exact 7 hours but about 7 hours<br /><br /><br />


***
## Execution Result(print)
If the price is broken away, the program catch the outlier and print the status like below

i) There is no Outlier
1시간봉 평균이탈율: 2.5281 %

ii) There is a Outlier or many Outliers
1시간봉 이탈률: -0.067 % OAXBTC  매수 신호 발생. 

시간: 2018-05-08 13:25:10 하한선가격: 0.00008551 현재가격: 0.00008545 평균이탈율: 2.5005 %

and contents are saved in .csv file

***
## Execution Picture
***

![Execution_picture](./(18.05.08) Outlier_Detection(60).png)
