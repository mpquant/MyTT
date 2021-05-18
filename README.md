# MyTT
MyTT将通达信,同花顺,文华麦语言等指标公式indicators,最简移植到Python中,核心库单个文件，仅百行代码,实现所有常见指标MACD,RSI,BOLL,ATR,KDJ,CCI,PSY等,全部基于numpy和pandas的函数封装，简洁且高性能，能非常方便的应用在各自股市分析，数字货币量化等领域

```python

#数字货币行情获取和指标计算演示
from  hb_hq_api import *
from  MyTT import *

#日线数据获取  1d:1天  4h:4小时   60m: 60分钟    15m:15分钟
df=get_price('btc.usdt',count=120,frequency='1d');      
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
