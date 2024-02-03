import pandas as pd
import talib
from ta.trend import macd
import ta
import os
import yfinance

def calculatestock(stock,start,end):
    global df
    df = pd.DataFrame()
    df=yfinance.download(stock,start,end)

def macdfram():    
    global df
    df['funds']=0
    df['coins']=0
    df['profit']=0
    df['perc']=0
    df['loss']=0
    df['crossover']=0
    convert = {'funds': float,
                'coins': float,
           'profit': float,
           'perc': float,
            'loss': float,
            'crossover':float
               }
    df = df.astype(convert)

def macdd(a):
    exp1 = df.Close.ewm(span=a[0], adjust=False).mean()
    exp2 = df.Close.ewm(span=a[1], adjust=False).mean()
    df['macd'] = exp1-exp2
    df['signal'] = df['macd'].ewm(span=a[2], adjust=False).mean()
    df['funds'][0]=100.0
    mcdlist=[0]*11
    initalfund=100.0
    lastfund=100.0
    profitloss=0.0
    buysignal=0.0
    sellsignal=0.0
    buytrades=0.0
    selltrades=0.0
    maxprofit=0.0
    maxloss=0.0
    minloss=0.0
    minprofit=0.0
    pattern=''

    
    
    
    for i in range(1,(len(df)-1)):
        if df['macd'][i]>=df['signal'][i] and df['macd'][i-1]<=df['signal'][i-1]:
            df['crossover'][i]=1
            buysignal=buysignal+1
        elif df['macd'][i]<=df['signal'][i] and df['macd'][i-1]>=df['signal'][i-1]:
            df['crossover'][i]= -1
            sellsignal=sellsignal+1
        else:
            df['crossover'][i]=0
        
    
    for i in range((len(df)-1)):
        if df['crossover'][i]== 1:
            if df['funds'][i]==0:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])
            else:
                df['coins'][i+1]=float(df.iloc[i]['funds']/df.iloc[i+1]['Open'])
                df['funds'][i+1]=0
                lastfund=df['funds'][i]
                buytrades=buytrades+1
        elif df['crossover'][i]== -1:
            if df['coins'][i]==0:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])
            else:
                df['funds'][i+1] = float(df.iloc[i]['coins'])* float(df.iloc[i+1]['Open'])
                df['coins'][i+1]=0
                selltrades=selltrades+1
                profitloss= float(df.iloc[i+1]['funds'] - lastfund)
                
                if profitloss<=0:
                    df['loss'][i+1]=profitloss
                else:
                    df['profit'][i+1]=profitloss

        else:
            df['funds'][i+1]=float(df.iloc[i]['funds'])
            df['coins'][i+1]=float(df.iloc[i]['coins'])

    if df['funds'][(len(df)-1)]==0:
        df['profit'][(len(df)-1)]=float(df.iloc[(len(df)-1)]['coins'])* float(df.iloc[(len(df)-1)]['Close'])
    else:
        df['profit'][(len(df)-1)]=df['funds'][(len(df)-1)]

    if buytrades>selltrades:
        pattern='Bullish'
    else:
        pattern='Bearish'
    maxprofit=df['profit'].max()
    minprofit=df['profit'].min()
    maxloss=df['loss'].min()
    minloss=df['loss'].max()
    print(df['profit'][(len(df)-1)])
    
    mcdlist[0]=initalfund
    mcdlist[1]=buysignal
    mcdlist[2]=sellsignal
    mcdlist[3]=df['profit'][(len(df)-1)]
    mcdlist[4]=buytrades
    mcdlist[5]=selltrades
    mcdlist[6]=maxprofit
    mcdlist[7]=minprofit
    mcdlist[8]=minloss
    mcdlist[9]=pattern
    mcdlist[10]='Macd Indicator'
    return mcdlist

def engpatternfram():
    global df
    df['funds']=0
    df['coins']=0
    df['profit']=0
    df['perc']=0
    df['loss']=0
    df['Engulling_signal']=0
    convert = {'funds': float,
                'coins': float,
           'profit': float,
           'perc': float,
            'loss': float,
            'Engulling_signal': float
               
               }
    df = df.astype(convert)

def engpfun():
    global df
    df['Engulling_signal']= talib.CDLENGULFING(df['Open'],df['High'],df['Low'],df['Close'])
    df['funds'][0]=100.0
    mcdlist=[0]*11
    initalfund=100.0
    lastfund=100.0
    profitloss=0.0
    buysignal=0.0
    sellsignal=0.0
    buytrades=0.0
    selltrades=0.0
    maxprofit=0.0
    maxloss=0.0
    minloss=0.0
    minprofit=0.0
    pattern=''
    
    
    for i in range(len(df)-1):
        if df['Engulling_signal'][i]== 100:
            buysignal=buysignal+1
        elif df['Engulling_signal'][i]== -100:
             sellsignal=sellsignal+1
        else:
            pass
    
    for i in range((len(df)-1)):
            if df['Engulling_signal'][i]== 100:
                if df['funds'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['coins'][i+1]=float(df.iloc[i]['funds']/df.iloc[i+1]['Open'])
                    df['funds'][i+1]=0
                    lastfund=df['funds'][i]
                    buytrades=buytrades+1
            elif df['Engulling_signal'][i]== -100:
                if df['coins'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['funds'][i+1] = float(df.iloc[i]['coins'])* float(df.iloc[i+1]['Open'])
                    df['coins'][i]=0
                    selltrades=selltrades+1
                    profitloss= float(df.iloc[i+1]['funds'] - lastfund)
                    if profitloss<=0:
                        df['loss'][i+1]=profitloss
                    else:
                        df['profit'][i+1]=profitloss
            else:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])

    
    if df['funds'][(len(df)-1)]==0:
        df['profit'][(len(df)-1)]=float(df.iloc[(len(df)-1)]['coins'])* float(df.iloc[(len(df)-1)]['Close'])
    else:
        df['profit'][(len(df)-1)]=df['funds'][(len(df)-1)]
    
    if buytrades>selltrades:
        pattern='Bullish'
    else:
        pattern='Bearish'

    maxprofit=df['profit'].max()
    minprofit=df['profit'].min()
    maxloss=df['loss'].min()
    minloss=df['loss'].max()
    print(df['profit'][(len(df)-1)])
    
    mcdlist[0]=initalfund
    mcdlist[1]=buysignal
    mcdlist[2]=sellsignal
    mcdlist[3]=df['profit'][(len(df)-1)]
    mcdlist[4]=buytrades
    mcdlist[5]=selltrades
    mcdlist[6]=maxprofit
    mcdlist[7]=minprofit
    mcdlist[8]=minloss
    mcdlist[9]=pattern
    mcdlist[10]='Engulling Pattern'
    return mcdlist

def rsiframe():
    global df
    df['funds']=0
    df['coins']=0
    df['profit']=0
    df['perc']=0
    df['loss']=0
    df['rsivalue']=0
    df['rsi']=0
    convert = {'funds': float,
                'coins': float,
           'profit': float,
           'perc': float,
            'loss': float,
            'rsivalue': float,
            'rsi': float
               
               }
    df = df.astype(convert)

def rsifun(a):
    global df
    df['rsivalue'] = talib.RSI(df["Close"],a)
    df['funds'][0]=100.0
    mcdlist=[0]*11
    initalfund=100.0
    lastfund=100.0
    profitloss=0.0
    buysignal=0.0
    sellsignal=0.0
    buytrades=0.0
    selltrades=0.0
    maxprofit=0.0
    maxloss=0.0
    minloss=0.0
    minprofit=0.0
    pattern=''
    
    
    for i in range(len(df)-1):
        if df['rsivalue'][i]<=30:
            df['rsi'][i]=1
            buysignal=buysignal+1
        elif df['rsivalue'][i]>=70:
             df['rsi'][i]= -1
             sellsignal=sellsignal+1
        else:
            df['rsi'][i]=0
    
    for i in range((len(df)-1)):
            if df['rsi'][i]== 1:
                if df['funds'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['coins'][i+1]=float(df.iloc[i]['funds']/df.iloc[i+1]['Open'])
                    df['funds'][i+1]=0
                    lastfund=df['funds'][i]
                    buytrades=buytrades+1
            elif df['rsi'][i]== -1:
                if df['coins'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['funds'][i+1] = float(df.iloc[i]['coins'])* float(df.iloc[i+1]['Open'])
                    df['coins'][i]=0
                    selltrades=selltrades+1
                    profitloss= float(df.iloc[i+1]['funds'] - lastfund)
                    if profitloss<=0:
                        df['loss'][i+1]=profitloss
                    else:
                        df['profit'][i+1]=profitloss
            else:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])

    
    if df['funds'][(len(df)-1)]==0:
        df['profit'][(len(df)-1)]=float(df.iloc[(len(df)-1)]['coins'])* float(df.iloc[(len(df)-1)]['Close'])
    else:
        df['profit'][(len(df)-1)]=df['funds'][(len(df)-1)]
    
    if buytrades>selltrades:
        pattern='Bullish'
    else:
        pattern='Bearish'
    
    maxprofit=df['profit'].max()
    minprofit=df['profit'].min()
    maxloss=df['loss'].min()
    minloss=df['loss'].max()
    print(df['profit'][(len(df)-1)])
    
    mcdlist[0]=initalfund
    mcdlist[1]=buysignal
    mcdlist[2]=sellsignal
    mcdlist[3]=df['profit'][(len(df)-1)]
    mcdlist[4]=buytrades
    mcdlist[5]=selltrades
    mcdlist[6]=maxprofit
    mcdlist[7]=minprofit
    mcdlist[8]=minloss
    mcdlist[9]=pattern
    mcdlist[10]='RSI Indicator'
    return mcdlist

def arronframe():
    global df
    df['funds']=0
    df['coins']=0
    df['profit']=0
    df['perc']=0
    df['loss']=0
    df['Arron_Signal']=0
    df['Arron_value']=0
    convert = {'funds': float,
                'coins': float,
           'profit': float,
           'perc': float,
            'loss': float,
            'Arron_Signal': float,
            'Arron_value': float
               
               }
    df = df.astype(convert)

def arronfun(a):
    global df
    df['Arron_value']= talib.AROONOSC(df['High'],df['Low'],a)
    df['funds'][0]=100.0
    mcdlist=[0]*11
    initalfund=100.0
    lastfund=100.0
    profitloss=0.0
    buysignal=0.0
    sellsignal=0.0
    buytrades=0.0
    selltrades=0.0
    maxprofit=0.0
    maxloss=0.0
    minloss=0.0
    minprofit=0.0
    pattern=''
    
    
   
    for i in range(len(df)-1):
        if df['Arron_value'][i]>=70 and df['Arron_value'][i]<=100 :
            df['Arron_Signal'][i]=1
            buysignal=buysignal+1
        elif df['Arron_value'][i]>=-100 and df['Arron_value'][i]<=-70:
            df['Arron_Signal'][i]= -1
            sellsignal=sellsignal+1
        else:
            df['Arron_Signal'][i]=0
    
    for i in range((len(df)-1)):
            if df['Arron_Signal'][i]== 1:
                if df['funds'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['coins'][i+1]=float(df.iloc[i]['funds']/df.iloc[i+1]['Open'])
                    df['funds'][i+1]=0
                    lastfund=df['funds'][i]
                    buytrades=buytrades+1
            elif df['Arron_Signal'][i]== -1:
                if df['coins'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['funds'][i+1] = float(df.iloc[i]['coins'])* float(df.iloc[i+1]['Open'])
                    df['coins'][i]=0
                    selltrades=selltrades+1
                    profitloss= float(df.iloc[i+1]['funds'] - lastfund)
                    if profitloss<=0:
                        df['loss'][i+1]=profitloss
                    else:
                        df['profit'][i+1]=profitloss
            else:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])

    
    if df['funds'][(len(df)-1)]==0:
        df['profit'][(len(df)-1)]=float(df.iloc[(len(df)-1)]['coins'])* float(df.iloc[(len(df)-1)]['Close'])
    else:
        df['profit'][(len(df)-1)]=df['funds'][(len(df)-1)]
    
    if buytrades>selltrades:
        pattern='Bullish'
    else:
        pattern='Bearish'

    maxprofit=df['profit'].max()
    minprofit=df['profit'].min()
    maxloss=df['loss'].min()
    minloss=df['loss'].max()
    print(df['profit'][(len(df)-1)])
    
    mcdlist[0]=initalfund
    mcdlist[1]=buysignal
    mcdlist[2]=sellsignal
    mcdlist[3]=df['profit'][(len(df)-1)]
    mcdlist[4]=buytrades
    mcdlist[5]=selltrades
    mcdlist[6]=maxprofit
    mcdlist[7]=minprofit
    mcdlist[8]=minloss
    mcdlist[9]=pattern
    mcdlist[10]='Arron Indicator'
    return mcdlist

def adxframe():
    global df
    df['funds']=0
    df['coins']=0
    df['profit']=0
    df['perc']=0
    df['loss']=0
    df['ADX']=0
    df['ADX_Signal']=0
    convert = {'funds': float,
                'coins': float,
           'profit': float,
           'perc': float,
            'loss': float,
            'ADX': float,
            'ADX_Signal': float
               
               }
    df = df.astype(convert)

def adxfun(a):
    global df
    df['ADX']=talib.ADX(df['High'],df['Low'],df['Close'],a)
    df['funds'][0]=100.0
    mcdlist=[0]*11
    initalfund=100.0
    lastfund=100.0
    profitloss=0.0
    buysignal=0.0
    sellsignal=0.0
    buytrades=0.0
    selltrades=0.0
    maxprofit=0.0
    maxloss=0.0
    minloss=0.0
    minprofit=0.0
    pattern=''
    
    
    for i in range(len(df)-1):
        if df['ADX'][i]>=25: 
            df['ADX_Signal'][i]=1
            buysignal=buysignal+1
        elif df['ADX'][i]>=1 and df['ADX'][i]<=25:
            df['ADX_Signal'][i]= -1
            sellsignal=sellsignal+1
        else:
            df['ADX_Signal'][i]=0
    
    for i in range((len(df)-1)):
            if df['ADX_Signal'][i]== 1:
                if df['funds'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['coins'][i+1]=float(df.iloc[i]['funds']/df.iloc[i+1]['Open'])
                    df['funds'][i+1]=0
                    lastfund=df['funds'][i]
                    buytrades=buytrades+1
            elif df['ADX_Signal'][i]== -1:
                if df['coins'][i]==0:
                    df['funds'][i+1]=float(df.iloc[i]['funds'])
                    df['coins'][i+1]=float(df.iloc[i]['coins'])
                else:
                    df['funds'][i+1] = float(df.iloc[i]['coins'])* float(df.iloc[i+1]['Open'])
                    df['coins'][i]=0
                    selltrades=selltrades+1
                    profitloss= float(df.iloc[i+1]['funds'] - lastfund)
                    if profitloss<=0:
                        df['loss'][i+1]=profitloss
                    else:
                        df['profit'][i+1]=profitloss
            else:
                df['funds'][i+1]=float(df.iloc[i]['funds'])
                df['coins'][i+1]=float(df.iloc[i]['coins'])

    
    if df['funds'][(len(df)-1)]==0:
        df['profit'][(len(df)-1)]=float(df.iloc[(len(df)-1)]['coins'])* float(df.iloc[(len(df)-1)]['Close'])
    else:
        df['profit'][(len(df)-1)]=df['funds'][(len(df)-1)]
    
    if buytrades>selltrades:
        pattern='Bullish'
    else:
        pattern='Bearish'

    maxprofit=df['profit'].max()
    minprofit=df['profit'].min()
    maxloss=df['loss'].min()
    minloss=df['loss'].max()
    print(df['profit'][(len(df)-1)])
    
    mcdlist[0]=initalfund
    mcdlist[1]=buysignal
    mcdlist[2]=sellsignal
    mcdlist[3]=df['profit'][(len(df)-1)]
    mcdlist[4]=buytrades
    mcdlist[5]=selltrades
    mcdlist[6]=maxprofit
    mcdlist[7]=minprofit
    mcdlist[8]=minloss
    mcdlist[9]=pattern
    mcdlist[10]='ADX Indicator'
    return mcdlist

def outframersi():
    newframe=pd.DataFrame()
    newframe=df
    newframe.drop(newframe[newframe['rsi'] ==0].index, inplace = True)
    return newframe

def outframemacd():
    newframe=pd.DataFrame()
    newframe=df
    newframe.drop(newframe[newframe['crossover'] ==0].index, inplace = True)
    return newframe

def outframeengf():
    newframe=pd.DataFrame()
    newframe=df
    newframe.drop(newframe[newframe['Engulling_signal'] ==0].index, inplace = True)
    return newframe

def outframearron():
    newframe=pd.DataFrame()
    newframe=df
    newframe.drop(newframe[newframe['Arron_Signal'] ==0].index, inplace = True)
    return newframe

def outframeadx():
    newframe=pd.DataFrame()
    newframe=df
    newframe.drop(newframe[newframe['ADX_Signal'] ==0].index, inplace = True)
    return newframe