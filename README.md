# MyTT
MyTT将通达信,同花顺,文华麦语言等指标公式indicators,最简移植到Python中,核心库单个文件，仅百行代码,实现所有常见指标MACD,RSI,BOLL,ATR,KDJ,CCI,PSY等,全部基于numpy和pandas的函数封装，简洁且高性能，能非常方便的应用在各自股市分析，数字货币量化等领域

# 功能特点
* 核心库轻量化： 项目库就一个文件MyTT.py,不用安装，不用设置，随用随走 ( from  MyTT import * 即可 )

* 代码人类化：)  没有什么炫耀的编程花样，初学者也能看懂，自己就能自行增加指标，马上就能用在项目中。

* 不需要安装ta-lib库,是纯python代码实现的的核心逻辑，很多人都有安装ta-lib库的痛苦经历

* 和通达信，同花顺的指标写法完全兼容，一个新的指标基本不用做修改，直接拿来即可使用

* 超高性能，基本不用循环，全是靠numpy,pandas的内置函数实现各种指标

* 和Talib库一样是多天参数进，多天指标出（序列进，序列出），便于画图和观察趋势

* MyTT实现的各种指标和通达信，同花顺，雪球等软件的指标一致到小数点后2位

```python

#数字货币行情获取和指标计算演示
from  hb_hq_api import *
from  MyTT import *

#日线数据获取  1d:1天  4h:4小时   60m: 60分钟    15m:15分钟
df=get_price('btc.usdt',count=120,frequency='1d');   
#-----------df结果如下表--------------------------------------------
```

|open|	close|	high	|low|	vol|
|--|--|--|--|--|
|2021-05-16	|48983.62|	47738.24|	49800.00|	46500.0	|1.333333e+09
|2021-05-17	|47738.24|	43342.50|	48098.66|	42118.0	|3.353662e+09
|2021-05-18	|43342.50|	44093.24|	45781.52|	42106.0	|1.793267e+09

```python
CLOSE=df.close.values;  OPEN=df.open.values;   HIGH=df.high.values;   LOW=df.low.values   #基础数据定义

MA5=MA(CLOSE,5)
MA10=MA(CLOSE,10)
CROSS_TODAY=RET(CROSS(MA5,MA10))

print(f'BTC5日均线{ MA5[-1]}    BTC10日均线 {MA10[-1]}' )
print('今天5日线是否上穿10日线',CROSS_TODAY)
print('最近5天收盘价全都大于5日线吗？',EVERY(CLOSE>MA10,5) )

DIF,DEA,MACD=MACD(CLOSE)
print('MACD值',DIF,DEA,MACD)
```




## 需安装第三方库
* requests
* pandas
 
----------------------------------------------------
### 巴特量化
* 数字货币 股市量化工具 行情系统软件开发

* BTC虚拟货币量化交易策略开发 自动化交易策略运行

----------------------------------------------------

![加入群聊](https://github.com/mpquant/huobi_intf/blob/main/img/qrcode.png) 
