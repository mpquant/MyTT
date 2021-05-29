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

### 先看一个最简单的例子

```python

#数字货币行情获取和指标计算演示
from  hb_hq_api import *         #数字货币行情库
from  MyTT import *              #myTT麦语言工具函数指标库

#获取btc.usdt交易对120日的数据
df=get_price('btc.usdt',count=120,frequency='1d');     # ‘4h’是4小时

#-----------df结果如下表(股市也基本一样)-------------------------------------------
```

|  |open|	close|	high	|low|	vol|
|--|--|--|--|--|--|
|2021-05-16	|48983.62|	47738.24|	49800.00|	46500.0	|1.333333e+09 |
|2021-05-17	|47738.24|	43342.50|	48098.66|	42118.0	|3.353662e+09 |
|2021-05-18	|43342.50|	44093.24|	45781.52|	42106.0	|1.793267e+09 |


```python

#-------有数据了，下面开始正题 -------------
CLOSE=df.close.values;  OPEN=df.open.values
HIGH=df.high.values;    LOW=df.low.values             #基础数据定义

MA5=MA(CLOSE,5)                                       #获取5日均线序列
MA10=MA(CLOSE,10)                                     #获取10日均线序列

print('BTC5日均线', MA5[-1] )                          # 只取最后一个数   
print('BTC10日均线',RET(MA10))                         # RET(MA10) == MA10[-1]
print('今天5日线是否上穿10日线',RET(CROSS(MA5,MA10)))
print('最近5天收盘价全都大于10日线吗？',EVERY(CLOSE>MA10,5) )

```


### MyTT库中的部分工具函数
* n天前的数据：`REF`

```python
REF(CLOSE, 1)              # 截止到昨天收盘价 序列
```
* 从序列中取倒数第N个数据(单个)：RET

```python
RET(CLOSE, 1)             # 最近一天的收盘价，单个数据
```
* 从序列中所有元素四舍五入：RD

```python
RD(CLOSE)                    # 默认返回3位小数
```
* 移动平均线计算：MA

```python
MA(CLOSE, 5)             # 取得收盘价5日平均线
```

* 加权移动平均计算：EMA

```python
EMA(CLOSE, 5)            # 为了精度 ，  EMA至少需要120周期   
```

* 中国式的SMA计算：SMA

```python
SMA(CLOSE, 5)            # 为了精度 ，  SMA至少需要120周期   
```
*  返回序列标准差：STD

```python
STD(CLOSE, 5)             # 返回收盘价5日内标准差
```

*  平均绝对偏差：AVEDEV

```python
AVEDEV(CLOSE, 5)    # 序列与其平均值的绝对差的平均值
```

* 金叉判断：CROSS

```python
CROSS(MA(CLOSE, 5), MA(CLOSE, 10))    # 5日均线上穿10日均线
```
* 两个序列取最大值,最小值：MAX    MIN

```python
MAX(OPEN, CLOSE )                       # K线实体的最高价
```
* n天内满足条件的天数：COUNT

```python
COUNT(CLOSE > OPEN, 10)           # 最近10天收阳线的天数
```
* n天内全部满足条件的天数：EVERY

```python
EVERY(CLOSE >OPEN, 5)           # 最近5天都是收阳线
```
* n天内是否至少满足条件一次：EXIST

```python
EXIST(CLOSE >OPEN, 5)           # 最近5天是否有一天收阳线
```

* n天内最大值：HHV

```python
HHV(MAX(OPEN, CLOSE), 20)        # 最近20天K线实体的最高价
```
* n天内最小值：LLV

```python
LLV(MIN(OPEN, CLOSE), 60)          # 最近60天K线实体的最低价
```
* 求和n日数据 SUM

```python
SUM(CLOSE, 10)                            # 求和10天的收盘价
```
* 条件 IF

```python
IF(OPEN > CLOSE, OPEN, CLOSE)        #如果 开盘>收盘  返回OPEN ，否则返回CLOSE
```

### 具体指标的实现，全部基于MyTT库中的工具函数 （更多指标可以自行添加）

```python
def MACD(CLOSE,SHORT=12,LONG=26,M=9):    # EMA的关系，CLOSE取120日，结果能精确到雪球小数点2位
    DIF = EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);  
    DEA = EMA(DIF,M);      MACD=(DIF-DEA)*2
    return RD(DIF),RD(DEA),RD(MACD)
```

```python
def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):   
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1*2-1));    D = EMA(K,(M2*2-1));        J=K*3-D*2
    return K, D, J
```

```python
def RSI(CLOSE, N=24):      
    DIF = CLOSE-REF(CLOSE,1) 
    return RD(SMA(MAX(DIF,0), N) / SMA(ABS(DIF), N) * 100)  
```

```python
def WR(CLOSE, HIGH, LOW, N=10, N1=6):            #W&R 威廉指标
    WR = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR1 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    return RD(WR), RD(WR1)
```

```python
def BIAS(CLOSE,L1=6, L2=12, L3=24):  # BIAS乖离率
    BIAS1 = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L2)) / MA(CLOSE, L2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L3)) / MA(CLOSE, L3) * 100
    return RD(BIAS1), RD(BIAS2), RD(BIAS3)
```

```python
def BOLL(CLOSE,N=20, P=2):            #BOLL布林带    
    MID = MA(CLOSE, N); 
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return RD(UPPER), RD(MID), RD(LOWER)    
```

```python
def PSY(CLOSE,N=12, M=6):  
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return RD(PSY),RD(PSYMA)
```

```python
def CCI(CLOSE,HIGH,LOW,N=14):  
    TP=(HIGH+LOW+CLOSE)/3
    return (TP-MA(TP,N))/(0.015*AVEDEV(TP,N))
```

```python
def ATR(CLOSE,HIGH,LOW, N=20):   #真实波动N日平均值
    TR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    return MA(TR, N)
```

### 因为语法的问题 =: 是不能用了，python就是=号 ，条件与是& ，条件或是|
```python

# 收盘价在10日均线上 且10日均线在20日均线上
(C > MA(C, 10)) & (MA(C, 10) > MA(C, 20))

# 收阳线 或 收盘价大于昨收
(C > O) | (C > REF(C, 1))

```

### 自定义指标示例
对于 DMI 这个指标，你会发现 TALib 算出来的结果，和同花顺等软件的结果不一样，是因为同花顺的公式和 TALib 的计算公式不一样，对于这种情况，只要把同花顺的公式搬过来，就可以算出和同花顺一样的结果。

```python
M1, M2 = 14, 6
TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
HD = HIGH - REF(HIGH, 1)
LD = REF(LOW, 1) - LOW

DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
DI1 = DMP * 100 / TR
DI2 = DMM * 100 / TR
ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
ADXR = (ADX + REF(ADX, M2)) / 2

print(DI1, DI2, ADX, ADXR)
```

### BOLL带指标数据获取和做图演示 (上证综指)

```python
up,mid,lower=BOLL(CLOSE)                                        #获取布林带数据 

plt.figure(figsize=(15,8))  
plt.plot(CLOSE,label='上证');    plt.plot(up,label='up');        #画图显示 
plt.plot(mid,label='mid');      plt.plot(lower,label='lower');

```
<div  align="center"> <img src="/img/boll.png" width = "960" height = "400" alt="Boll线" /> </div>



## 需安装第三方库（无需ta-lib库，所有指标实现仅需要安装pandas既可）
* pandas
 
----------------------------------------------------
### 巴特量化
* 数字货币 股市量化工具 行情系统软件开发

* BTC虚拟货币量化交易策略开发 自动化交易策略运行

----------------------------------------------------

![加入群聊](https://github.com/mpquant/huobi_intf/blob/main/img/qrcode.png) 
