# MyTT 麦语言-通达信-同花顺指标实现     https://github.com/mpquant/MyTT
# 高级函数版本，本文件函数计算结果经过验证完全正确，可以正常使用，但代码比较复杂，做为进阶使用。
# MyTT团队对每个函数精益求精，力争效率速度，代码优雅的完美统一，如果您有更好的实现方案，请不吝赐教！
# 感谢以下团队成员的努力和贡献： 火焰，jqz1226, stanene, bcq

#------------------------工具函数---------------------------------------------

def HHV(S, N):  #HHV,支持N为序列版本
    # type: (np.ndarray, Optional[int,float, np.ndarray]) -> np.ndarray
    """
    HHV(C, 5)  # 最近5天收盘最高价
    """
    if isinstance(N, (int, float)):
        return pd.Series(S).rolling(N).max().values
    else:
        res = np.repeat(np.nan, len(S))
        for i in range(len(S)):
            if (not np.isnan(N[i])) and N[i] <= i + 1:
                res[i] = S[i + 1 - N[i]:i + 1].max()
        return res

    
def LLV(S, N):   #LLV,支持N为序列版本
    # type: (np.ndarray, Optional[int,float, np.ndarray]) -> np.ndarray
    """
    LLV(C, 5)  # 最近5天收盘最低价
    """
    if isinstance(N, (int, float)):
        return pd.Series(S).rolling(N).min().values
    else:
        res = np.repeat(np.nan, len(S))
        for i in range(len(S)):
            if (not np.isnan(N[i])) and N[i] <= i + 1:
                res[i] = S[i + 1 - N[i]:i + 1].min()
        return res


def DSMA(X, N):    # 偏差自适应移动平均线   type: (np.ndarray, int) -> np.ndarray
    """
    Deviation Scaled Moving Average (DSMA)    Python by: jqz1226, 2021-12-27
    Referred function from myTT: SUM, DMA
    """
    a1 = math.exp(- 1.414 * math.pi * 2 / N)
    b1 = 2 * a1 * math.cos(1.414 * math.pi * 2 / N)
    c2 = b1
    c3 = -a1 * a1
    c1 = 1 - c2 - c3        
    Zeros = np.pad(X[2:] - X[:-2],(2,0),'constant')          
    Filt = np.zeros(len(X))
    for i in range(len(X)):
        Filt[i] = c1 * (Zeros[i] + Zeros[i-1]) / 2 + c2 * Filt[i-1] + c3 * Filt[i-2]    
    
    RMS = np.sqrt(SUM(np.square(Filt), N) / N)
    ScaledFilt = Filt / RMS
    alpha1 = np.abs(ScaledFilt) * 5 / N    
    return DMA(X, alpha1)    



def SUMBARSFAST(X, A): 
    # type: (np.ndarray, Optional[np.ndarray, float, int]) -> np.ndarray
    """
    通达信SumBars函数的Python实现  by jqz1226
    SumBars函数将X向前累加，直到大于等于A, 返回这个区间的周期数。例如SUMBARS(VOL, CAPITAL),求完全换手的周期数。
    :param X: 数组。被累计的源数据。 源数组中不能有小于0的元素。
    :param A: 数组（一组）或者浮点数（一个）或者整数（一个），累加截止的界限数
    :return:  数组。各K线分别对应的周期数
    """
    if any(X<=0):   raise ValueError('数组X的每个元素都必须大于0！')
    
    X = np.flipud(X)  # 倒转
    length = len(X)

    if isinstance(A * 1.0, float):  A = np.repeat(A, length)  # 是单值则转化为数组
    A = np.flipud(A)  # 倒转
    sumbars = np.zeros(length)  # 初始化sumbars为0
    Sigma = np.insert(np.cumsum(X), 0, 0.0)  # 在累加值前面插入一个0.0（元素变多1个，便于引用）

    for i in range(length):
        k = np.searchsorted(Sigma[i + 1:], A[i] + Sigma[i])
        if k < length - i:  # 找到
            sumbars[length - i - 1] = k + 1
    return sumbars.astype(int)  
  
  


#------------------------指标函数---------------------------------------------

def SAR(HIGH, LOW, N=10, S=2, M=20):             
    """
    求抛物转向。 例如SAR(10,2,20)表示计算10日抛物转向，步长为2%，步长极限为20%
    Created by: jqz1226, 2021-11-24首次发表于聚宽(www.joinquant.com)
    
    :param HIGH: high序列
    :param LOW: low序列
    :param N: 计算周期
    :param S: 步长
    :param M: 步长极限
    :return: 抛物转向
    """
    f_step = S / 100;    f_max = M / 100;    af = 0.0
    is_long = HIGH[N - 1] > HIGH[N - 2]
    b_first = True
    length = len(HIGH)

    s_hhv = REF(HHV(HIGH, N), 1)  # type: np.ndarray
    s_llv = REF(LLV(LOW, N), 1)  # type: np.ndarray
    sar_x = np.repeat(np.nan, length)  # type: np.ndarray
    for i in range(N, length):
        if b_first:  # 第一步
            af = f_step
            sar_x[i] = s_llv[i] if is_long else s_hhv[i]
            b_first = False
        else:  # 继续多 或者 空
            ep = s_hhv[i] if is_long else s_llv[i]  # 极值
            if (is_long and HIGH[i] > ep) or ((not is_long) and LOW[i] < ep):  # 顺势：多创新高 或者 空创新低
                af = min(af + f_step, f_max)
            #
            sar_x[i] = sar_x[i - 1] + af * (ep - sar_x[i - 1])

        if (is_long and LOW[i] < sar_x[i]) or ((not is_long) and HIGH[i] > sar_x[i]):  # 反空 或者 反多
            is_long = not is_long
            b_first = True
    return sar_x


def TDX_SAR(High, Low, iAFStep=2, iAFLimit=20):    # type: (np.ndarray, np.ndarray, int, int) -> np.ndarray
    """  通达信SAR算法,和通达信SAR对比完全一致   by: jqz1226, 2021-12-18
    :param High: 最高价序列
    :param Low: 最低价序列
    :param iAFStep: AF步长
    :param iAFLimit: AF极限值
    :return: SAR序列
    """
    af_step = iAFStep / 100;     af_limit = iAFLimit / 100
    SarX = np.zeros(len(High))   # 初始化返回数组

    # 第一个bar
    bull = True 
    af = af_step
    ep = High[0]
    SarX[0] = Low[0]
    # 第2个bar及其以后
    for i in range(1, len(High)):
        # 1.更新：hv, lv, af, ep
        if bull:  # 多
            if High[i] > ep:  # 创新高
                ep = High[i]
                af = min(af + af_step, af_limit)
        else:  # 空
            if Low[i] < ep:  # 创新低
                ep = Low[i]
                af = min(af + af_step, af_limit)
        # 2.计算SarX
        SarX[i] = SarX[i - 1] + af * (ep - SarX[i - 1])

        # 3.修正SarX
        if bull:
            SarX[i] = max(SarX[i - 1], min(SarX[i], Low[i], Low[i - 1]))
        else:
            SarX[i] = min(SarX[i - 1], max(SarX[i], High[i], High[i - 1]))

        # 4. 判断是否：向下跌破，向上突破
        if bull:  # 多
            if Low[i] < SarX[i]:  # 向下跌破，转空
                bull = False
                tmp_SarX = ep  # 上阶段的最高点
                ep = Low[i]
                af = af_step
                if High[i - 1] == tmp_SarX:  # 紧邻即最高点
                    SarX[i] = tmp_SarX
                else:
                    SarX[i] = tmp_SarX + af * (ep - tmp_SarX)
        else:  # 空
            if High[i] > SarX[i]:  # 向上突破, 转多
                bull = True
                ep = High[i]
                af = af_step
                SarX[i] = min(Low[i], Low[i - 1])
    # end for
    return SarX





