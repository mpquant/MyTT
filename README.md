# MyTT (My麦语言 T通达信 T同花顺)
MyTT是您量化工具箱里的瑞士军刀，精炼而高效，它将通达信,同花顺,文华麦语言等指标公式indicators,最简移植到Python中,核心库单个文件，仅百行代码,实现和转换同花顺通达信所有常见指标MACD,RSI,BOLL,ATR,KDJ,CCI,PSY等,全部基于numpy和pandas的函数封装，简洁且高性能，能非常方便的应用在各自股票股市技术分析，股票自动程序化交易,数字货币BTC等量化等领域.Mini Python library with most stock market indicators.

[![license](https://img.shields.io/:license-gpl-blue.svg)](https://badges.gpl-license.org/)

# 功能特点
* 核心库轻量化： 项目库就一个文件 [MyTT.py](https://github.com/mpquant/MyTT/blob/main/MyTT.py),不用安装设置，可自由裁剪，随用随走 `from MyTT import *` 即可 

* 代码人类化：)  没有什么炫耀的编程花样，初学者也能看懂，自己就能自行增加指标，马上就能用在项目中。

* 不需要安装ta-lib库,是纯python代码实现的的核心逻辑，很多人都有安装ta-lib库的痛苦经历

* 和通达信，同花顺的指标写法完全兼容，一个新的指标基本不用做修改，直接拿来即可使用

* 超高性能，基本不用循环，全是靠numpy,pandas的内置函数实现各种指标

* 和Talib库一样是多天参数进，多天指标出（序列进，序列出），便于画图和观察趋势

* MyTT实现的各种指标和通达信，同花顺，雪球等软件的技术指标一致到小数点后2位

* MyTT高级进阶版本，收录了高级复杂用法的函数和实验验证函数 [MyTT_plus](https://github.com/mpquant/MyTT/blob/main/MyTT_plus.py)

* MyTT也能在python2的老版本pandas中使用，请用此python2版本 [MyTT_python2](https://github.com/mpquant/MyTT/blob/main/MyTT_python2.py)


### 先看一个最简单的例子  

```python

#数字货币行情获取和指标计算演示
from  hb_hq_api import *         #数字货币行情库
from  MyTT import *              #myTT麦语言工具函数指标库

#获取btc.usdt交易对120日的数据
df=get_price('btc.usdt',count=120,frequency='1d');     #'1d'是1天, '4h'是4小时

#-----------df结果如下表(股市也基本一样)-------------------------------------------
```

|  |open|	close|	high	|low|	vol|
|--|--|--|--|--|--|
|2021-05-16	|48983.62|	47738.24|	49800.00|	46500.0	|1.333333e+09 |
|2021-05-17	|47738.24|	43342.50|	48098.66|	42118.0	|3.353662e+09 |
|2021-05-18	|43342.50|	44093.24|	45781.52|	42106.0	|1.793267e+09 |


```python

#-------有数据了，下面开始正题 -------------
CLOSE=df.close.values;  OPEN=df.open.values           #基础数据定义，只要传入的是序列都可以   
HIGH=df.high.values;    LOW=df.low.values             #例如 CLOSE=list(df.close) 都是一样

MA5=MA(CLOSE,5)                                       #获取5日均线序列
MA10=MA(CLOSE,10)                                     #获取10日均线序列

print('BTC5日均线', MA5[-1] )                          # 只取最后一个数   
print('BTC10日均线',RET(MA10))                         # RET(MA10) == MA10[-1]
print('今天5日线是否上穿10日线',RET(CROSS(MA5,MA10)))
print('最近5天收盘价全都大于10日线吗？',EVERY(CLOSE>MA10,5) )

```
### 安装方法
* 直接拷贝 MyTT.py到你的项目下 `from MyTT import *` 即可调用文件中的所有函数

* 传统标准库安装 `pip install MyTT`

```python
from  MyTT import *                 #声明调用MyTT， 请注意大小写
S=np.random.randint(1,99,[10])      #生成1-99内的10个数序列 
EMA(S,6)                            #对这个序列S进行6周期EMA指数平均计算
```

### 教程和案例应用
* [通达信公式转Python神器——MyTT库](https://www.joinquant.com/view/community/detail/a6cc7d1fb73a57dbac4b77044a33b15d)  

* [利用MyTT库整合通达信指标公式](https://www.joinquant.com/view/community/detail/4237ebaa5db39a5a9a2195338e8be588)  

* [MyTT库应用示例及计算精度验证](https://www.joinquant.com/view/community/detail/bd26874654a6f9f1958f23043ca06149)  

* [如何在聚宽研究环境中建立myTT.py库文件](https://www.joinquant.com/view/community/detail/2abf0cc457352b59ef2e873ad7c4e430)  

* [基于MyTT来编写Python版通达信指标](https://www.joinquant.com/view/community/detail/7a0297fb7bd717cfb2be40b4c8062eeb)  

* [MyTT基础函数EMA指数平均的公式推导](https://www.joinquant.com/view/community/detail/ab76489c8fdfd1f201b6df47f11a5360)


### MyTT库中的部分工具函数
* n天前的数据：`REF`
```python
REF(CLOSE, 1)              # 截止到昨天收盘价 序列
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

*  平均绝对偏差：`AVEDEV`
```python
AVEDEV(CLOSE, 5)    # 序列与其平均值的绝对差的平均值
```

* 金叉判断：CROSS
```python
CROSS(MA(CLOSE, 5), MA(CLOSE, 10))       #5日均线上穿10日均线
```

* 两个序列取最大值,最小值：`MAX`  `MIN`
```python
MAX(OPEN, CLOSE )                       #K线实体的最高价
```

* n天内满足条件的天数：COUNT
```python
COUNT(CLOSE > OPEN, 10)                 #最近10天收阳线的天数
```

* n天内全部满足条件的天数：EVERY
```python
EVERY(CLOSE >OPEN, 5)                   #最近5天都是收阳线
```

* 从前A日到前B日一直满足条件 ：LAST
```python
LAST(CLOSE>OPEN,5,3)                    #5天前到3天前是否都收阳线
```

* n天内是否至少满足条件一次：EXIST
```python
EXIST(CLOSE>OPEN, 5)                   #最近5天是否有一天收阳线
```

* 上一次条件成立到当前的周期：BARSLAST
```python
BARSLAST(CLOSE/REF(CLOSE)>=1.1)         #上一次涨停到今天的天数
```

* 返回序列的线性回归斜率：`SLOPE`
```python
SLOPE(MA(CLOSE,10),5)                   #得到10日平均线最近5天的斜率(其实就是MA均线的方向)
```

* 取回线性回归后的预测值：`FORCAST`
```python
FORCAST(CLOSE,20)                       #根据最近20日的走势预测明天的收盘价
```

*  n天内最大值：`HHV`
```python
HHV(MAX(OPEN, CLOSE), 20)               #最近20天K线实体的最高价
```

* n天内最小值：`LLV`
```python
LLV(MIN(OPEN, CLOSE), 60)              #最近60天K线实体的最低价
```

* 条件 `IF`
```python
IF(OPEN > CLOSE, OPEN, CLOSE)          #如果 开盘>收盘  返回OPEN ，否则返回CLOSE
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
def RSI(CLOSE, N=24):                     #RSI指标
    DIF = CLOSE-REF(CLOSE,1) 
    return RD(SMA(MAX(DIF,0), N) / SMA(ABS(DIF), N) * 100)  
```

```python
def WR(CLOSE, HIGH, LOW, N=10, N1=6):    #W&R 威廉指标
    WR = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR1 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    return RD(WR), RD(WR1)
```

```python
def BIAS(CLOSE,L1=6, L2=12, L3=24):      #BIAS乖离率
    BIAS1 = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L2)) / MA(CLOSE, L2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L3)) / MA(CLOSE, L3) * 100
    return RD(BIAS1), RD(BIAS2), RD(BIAS3)
```

```python
def BOLL(CLOSE,N=20, P=2):                #BOLL布林带    
    MID = MA(CLOSE, N); 
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return RD(UPPER), RD(MID), RD(LOWER)    
```

```python
def PSY(CLOSE,N=12, M=6):                 #PSY心理线指标
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return RD(PSY),RD(PSYMA)
```

```python
def CCI(CLOSE,HIGH,LOW,N=14):            #CCI顺势指标
    TP=(HIGH+LOW+CLOSE)/3
    return (TP-MA(TP,N))/(0.015*AVEDEV(TP,N))
```

```python
def ATR(CLOSE,HIGH,LOW, N=20):           #真实波动N日平均值
    TR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    return MA(TR, N)
```

```python
def BBI(CLOSE,M1=3,M2=6,M3=12,M4=20):    #BBI多空指标   
    return (MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4  
```


```python
def TAQ(HIGH,LOW,N):                         #唐安奇通道(海龟)交易指标，大道至简，能穿越牛熊
    UP=HHV(HIGH,N);    DOWN=LLV(LOW,N);    MID=(UP+DOWN)/2
    return UP,MID,DOWN
```

```python
def KTN(CLOSE,HIGH,LOW,N=20,M=10):           #肯特纳交易通道, N选20日，ATR选10日
    MID=EMA((HIGH+LOW+CLOSE)/3,N)
    ATRN=ATR(CLOSE,HIGH,LOW,M)
    UPPER=MID+2*ATRN;   LOWER=MID-2*ATRN
    return UPPER,MID,LOWER   
```

```python
def TRIX(CLOSE,M1=12, M2=20):                #三重指数平滑平均线
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)
    return TRIX, TRMA
```

```python
def BRAR(OPEN,CLOSE,HIGH,LOW,M1=26):         #BRAR-ARBR 情绪指标  
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100
    return AR, BR
```

```python
def MTM(CLOSE,N=12,M=6):                    #动量指标
    MTM=CLOSE-REF(CLOSE,N);         MTMMA=MA(MTM,M)
    return MTM,MTMMA
```
```python
def ROC(CLOSE,N=12,M=6):                     #变动率指标
    ROC=100*(CLOSE-REF(CLOSE,N))/REF(CLOSE,N);    MAROC=MA(ROC,M)
    return ROC,MAROC
```
```python
def EXPMA(CLOSE,N1=12,N2=50):                #EMA指数平均数指标
    return EMA(CLOSE,N1),EMA(CLOSE,N2);
``` 
```python
def OBV(CLOSE,VOL):                          #能量潮指标
    return SUM(IF(CLOSE>REF(CLOSE,1),VOL,IF(CLOSE<REF(CLOSE,1),-VOL,0)),0)/10000
``` 

```python
def MFI(CLOSE,HIGH,LOW,VOL,N=14):            #MFI指标是成交量的RSI指标
    TYP = (HIGH + LOW + CLOSE)/3
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N)  
    return 100-(100/(1+V1))    
``` 



* 更多指标看库文件  [MyTT.py](https://github.com/mpquant/MyTT/blob/main/MyTT.py)

### 因为语法的问题 =: 是不能用了，python就是=号 ，条件与是& ，条件或是|
```python

#通达信函数 VAR1:=(C>REF(C,1) AND C>REF(C,2));
 python写法： VAR1=( (CLOSE>REF(CLOSE,1)) & (CLOSE>REF(CLOSE,2)) );

# 收盘价在10日均线上 且10日均线在20日均线上
python写法： (C > MA(C, 10)) & (MA(C, 10) > MA(C, 20))

# 收阳线 或 收盘价大于昨收
python写法： (CLOSE > O) | (CLOSE > REF(CLOSE, 1))

```


### BOLL带指标数据获取和做图演示 (上证综指)

```python
up,mid,lower=BOLL(CLOSE)                                        #获取布林带数据 

plt.figure(figsize=(15,8))  
plt.plot(CLOSE,label='上证');    plt.plot(up,label='up');        #画图显示 
plt.plot(mid,label='mid');      plt.plot(lower,label='lower');

```
<div  align="center"> <img src="/img/boll.png" width = "960" height = "400" alt="Boll线" /> </div>


### 唐安奇交易通道指标计算和做图演示 (沪深300指数)

```python
up,mid,down=TAQ(HIGH,LOW,20)                                    #获取唐安奇交易通道数据，大道至简，能穿越牛熊
plt.figure(figsize=(15,8))  
plt.plot(CLOSE,label='沪深300指数')                                  
plt.plot(up,label='唐安奇-上轨');     plt.plot(mid,label='唐安奇-中轨');      plt.plot(down,label='唐安奇-下轨')
```
<div  align="center"> <img src="/img/taq.jpg" width = "960" height = "400" alt="taq" /> </div>


### 需安装第三方库（无需ta-lib库，所有指标实现仅需要安装pandas既可）
* pandas


### 代码贡献者Contributors 
    火焰，jqz1226, stanene, bcq


----------------------------------------------------
### 团队其他开源项目 - 如果本项目能帮助到您，请右上角帮我们点亮 ★star 以示鼓励！
* [MyTT 通达信,同花顺公式指标，文华麦语言的python实现](https://github.com/mpquant/MyTT)

* [Ashare最简股票行情数据接口API,A股行情完全开源免费](https://github.com/mpquant/Ashare)



----------------------------------------------------

![加入群聊](https://github.com/mpquant/Ashare/blob/main/img/qrcode.png) 

> #### 股市程序化交易大群,数字货币量化交易探讨, 圈内大咖量化策略分享
> #### 全是干货，无闲聊 ，物以类聚,人以群分，一起感受思维碰撞的力量!
