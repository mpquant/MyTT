# MyTT
各种交易指标的最简单封装，通达信-同花顺指标实现

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
