#火币行情功能函数
import json,requests,urllib3,datetime;   import pandas as pd;  import numpy as np ; urllib3.disable_warnings()

huobi_domain='api.huobi.de.com'   #API地址   'api.huobi.pro'    api.huobi.be没有被墙  api.huobi.de.com

class Context:   #根类
    def __init__(self):  
        self.current_dt=datetime.datetime.now()

# #1d:1天  4h:4小时   60m: 60分钟    15m:15分钟
def get_price(code, end_date=None, count=1,frequency='1d', fields=['close']):    
    code=code.replace('.','')
    frequency=frequency.replace('d','day').replace('m','min').replace('h','hour')
    url = f'https://{huobi_domain}/market/history/kline?period={frequency}&size={count}&symbol={code}'
    res = requests.get(url,verify=False).text  
    df=pd.DataFrame(json.loads(res)['data']);      df=df.iloc[::-1]     #排序翻转
    df["time"] = pd.to_datetime(df["id"]+8*3600, unit='s')              #时间戳转时间，北京时间+8小时
    df=df[['time','open','close','high','low','vol']]                   #更正排序
    df.set_index(["time"], inplace=True);     df.index.name=''          #处理索引   
    return df

def get_last_price(code):        #获取某只股票最新价格函数04-25
    return get_price(code,count=1,frequency='1m', fields=['close']).close[0]

def attribute_history(security, count, unit='1d', fields=['open', 'close', 'high', 'low', 'volume', 'money']):   #获取历史行情     
    return get_price(security = security, end_date = context.current_dt, frequency=unit, fields=fields, fq = fq, count = count)[:-1]            


