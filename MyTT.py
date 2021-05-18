# MyTT 麦语言-通达信-同花顺指标实现    https://github.com/mpquant/MyTT
  
import numpy as np; import pandas as pd


def RD(N,D=3):   return np.round(N,D)        #四舍五入取3位小数 
def RET(S,N=1):  return np.array(S)[-N]      #返回序列倒数第N个值,默认返回最后一个
def ABS(S):      return np.abs(S)            #返回N的绝对值
def MAX(S1,S2):  return np.maximum(S1,S2)    #序列max
def MIN(S1,S2):  return np.minimum(S1,S2)    #序列min
         
def MA(S,N):           #求序列的N日平均值，返回序列                    
    return pd.Series(S).rolling(N).mean().values

def REF(S, N=1):       # 对序列整体下移动N,返回序列(shift后会产生NAN)    
    return pd.Series(S).shift(N).values  

def DIFF(S, N=1):  #前一个值减后一个值,前面会产生nan 
    return pd.Series(S).diff(N)  #np.diff(S)直接删除nan，会少一行

def STD(S,N):           #求序列的N日标准差，返回序列    
    return  pd.Series(S).rolling(N).std(ddof=0).values     

def IF(S_BOOL,S_TRUE,S_FALSE):         # res=S_TRUE if S_BOOL==True  else  S_FALSE
    return np.where(S_BOOL, S_TRUE, S_FALSE)

def SUM(S, N):           #对序列求N天累计和，返回序列         
    return pd.Series(S).rolling(N).sum().values

def HHV(S,N):                           # HHV(C, 5)  # 最近5天收盘最高价        
    return pd.Series(S).rolling(N).max().values

def LLV(S,N):                          # LLV(C, 5)  # 最近5天收盘最低价     
    return pd.Series(S).rolling(N).min().values

def EMA(S,N):  #为了精度 S>4*N  EMA至少需要120周期       
    return pd.Series(S).ewm(span=N, adjust=False).mean().values    

def SMA(S, N, M=1):  #中国式的SMA,至少需要120周期才精确        
    K = pd.Series(S).rolling(N).mean()    #先求出平均值
    for i in range(N+1, len(S)):  K[i] = (M * S[i] + (N -M) * K[i-1]) / N  # 因为要取K[i-1]，所以 range(N+1, len(S))        
    return K

def AVEDEV(S,N):  # 平均绝对偏差  (序列与其平均值的绝对差的平均值)   
    avedev=pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean())    
    return avedev.values
    #--------------------------------------------------------------------        

def COUNT(S_BOOL, N):                   # COUNT(C>O, N):  最近N天满足S_BOO的天数  True的天数
    return SUM(S_BOOL,N)    

def EVERY(S_BOOL, N):                  # EVERY(C>O, 5)   最近N天是否都是True
    R=SUM(S_BOOL, N)
    return  IF(R==N, True, False)

def EXIST(S_BOOL, N=5):                # EXIST(CLOSE>3010, N=5)  n日内是否存在一天大于3000点
    R=SUM(S_BOOL,N)    
    return IF(R>0, True ,False)

def CROSS(S1,S2):                      # 判断穿越 CROSS(MA(C,5),MA(C,10))               
    CROSS_BOOL=IF(S1>S2, True ,False)   #;print(CROSS_BOOL)
    return COUNT(CROSS_BOOL>0,2)==1    # 上穿：昨天0 今天1   下穿：昨天1 今天0

#-----------------------------------下面是具体指标-------------------------------------
def MACD(CLOSE,SHORT=12,LONG=26,M=9):    # EMA的关系，S取120日，和雪球小数点2位相同
    DIF = EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);  
    DEA = EMA(DIF,M);      MACD=(DIF-DEA)*2
    return RD(DIF),RD(DEA),RD(MACD)

def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):   
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1*2-1));    D = EMA(K,(M2*2-1));        J=K*3-D*2
    return K, D, J

def RSI(CLOSE, N=24):      
    DIF = CLOSE-REF(CLOSE,1) 
    return RD(SMA(MAX(DIF,0), N) / SMA(ABS(DIF), N) * 100)  

def WR(CLOSE, N=10, N1=6):            #W&R 威廉指标
    WR = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR1 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    return RD(WR), RD(WR1)

def BIAS(CLOSE,L1=6, L2=12, L3=24):  # BIAS乖离率
    BIAS1 = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L2)) / MA(CLOSE, L2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L3)) / MA(CLOSE, L3) * 100
    return RD(BIAS1), RD(BIAS2), RD(BIAS3)

def BOLL(CLOSE,N=20, P=2):            #BOLL布林带    
    MID = MA(CLOSE, N); 
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return RD(UPPER), RD(MID), RD(LOWER)    

def PSY(CLOSE,N=12, M=6):  
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return RD(PSY),RD(PSYMA)


def CCI(CLOSE,HIGH,LOW,N=14):  
    TP=(HIGH+LOW+CLOSE)/3
    return (TP-MA(TP,N))/(0.015*AVEDEV(TP,N))
        
def ATR(CLOSE,HIGH,LOW, N=20):   #真实波动N日平均值
    TR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    return MA(TR, N)
    

    