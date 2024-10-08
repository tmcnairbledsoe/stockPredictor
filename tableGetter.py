

import numpy as np
import pandas as pd

def SpyHistory():
    df = pd.read_csv('C:\\src\\stockPredictor\\SPYHist.csv', index_col=0)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = [d.date() for d in df['DateTime']]
    df['time'] = [d.time() for d in df['DateTime']]
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)
    df['Difference'] = df['Close'] - df['Open']
    df = df.dropna()

    for currentDate in df.date.unique():
        if len(df.time.unique()) > len(df.loc[df['date'] == currentDate]):
            df = df.loc[df['date'] != currentDate]
    
    return df
    
def SpyHistoryWithSma():
    df = pd.read_csv('C:\\src\\stockPredictor\\SPYHist.csv', index_col=0)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = [d.date() for d in df['DateTime']]
    df['time'] = [d.time() for d in df['DateTime']]
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)
    df['slowsma'] = df['Close'].rolling(21).mean()
    df['fastsma'] = df['Close'].rolling(9).mean()
    df['Difference'] = df['Close'] - df['Open']
    df = df.dropna()

    for currentDate in df.date.unique():
        if len(df.time.unique()) > len(df.loc[df['date'] == currentDate]):
            df = df.loc[df['date'] != currentDate]
    
    return df

def QqqHistory():
    df = pd.read_csv('C:\\src\\stockPredictor\\QQQHist.csv', index_col=0)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = [d.date() for d in df['DateTime']]
    df['time'] = [d.time() for d in df['DateTime']]
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)
    df['Difference'] = df['Close'] - df['Open']
    df = df.dropna()

    for currentDate in df.date.unique():
        if len(df.time.unique()) > len(df.loc[df['date'] == currentDate]):
            df = df.loc[df['date'] != currentDate]
    
    return df
    
def QqqHistoryWithSma():
    df = pd.read_csv('C:\\src\\stockPredictor\\QQQHist.csv', index_col=0)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = [d.date() for d in df['DateTime']]
    df['time'] = [d.time() for d in df['DateTime']]
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)
    df['slowsma'] = df['Close'].rolling(21).mean()
    df['fastsma'] = df['Close'].rolling(9).mean()
    df['Difference'] = df['Close'] - df['Open']
    df = df.dropna()

    for currentDate in df.date.unique():
        if len(df.time.unique()) > len(df.loc[df['date'] == currentDate]):
            df = df.loc[df['date'] != currentDate]
    
    return df

def TradeData():
    df = pd.read_csv('C:\\src\\stockPredictor\\tradeData.csv', index_col=0)
    df['Price'] = df['Price'].astype(float)
    return df

    
def AverageWinning():
    df = pd.read_csv('C:\\src\\stockPredictor\\averageWin.csv', index_col=0)
    df['AverageWin'] = df['AverageWin'].astype(float)
    return df