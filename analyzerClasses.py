from abc import ABC, abstractmethod
import numpy as np

class Analyzer(ABC):
    def __init__(self):
        self.long = False
        self.short = False
        self.lastPrice = 0
        self.totalWin = 0
        self.name = ''
        self.tradeNum = 0
        self.profit = 0
 
    def action(self):
        pass

class BasicAnalyzer(Analyzer):
    def __init__(self):
        self.long = False
        self.short = False
        self.closed = False
        self.lastPrice = 0
        self.totalWin = 0
        self.name = 'Basic'
        self.tradeNum = 0
        self.profit = 0
 
    def action(self, predicted_sequence, todaysData):
        self.closed = False
        total = 0
        highest = 0
        positive = predicted_sequence[0] > 0
        
        for i in range(0,len(predicted_sequence)):
            total = total + predicted_sequence[i]
            if positive:
                if total < 0:
                    break
                if highest < total:
                    highest = total
            else:
                if total > 0:
                    break
                if highest > total:
                    highest = total
        
        highest = abs(highest)
        percentChange = highest / todaysData.iloc[-1]['Close'] * 100

        if self.long == False and self.short == False:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = True
                return 'GOLONG'
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = True
                return 'GOSHORT'
            else:
                return ''
        elif self.long == True:
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                self.short = True
                return 'GOSHORT'
            elif not positive:
                print('SELL')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                return 'SELL'
            else:
                return ''
        elif self.short == True:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.profit = self.lastPrice  - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice  - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                self.long = True
                return 'GOLONG'
            elif positive:
                print('BUY')
                self.profit = self.lastPrice  - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice  - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                return 'BUY'
            else:
                return ''


class CrossoverAnalyzer(Analyzer):
    def __init__(self):
        self.long = False
        self.short = False
        self.closed = False
        self.lastPrice = 0
        self.totalWin = 0
        self.name = 'Crossover'
        self.tradeNum = 0
        self.profit = 0
 
    def action(self, predicted_sequence, todaysData):
        self.closed = False
        total = 0
        highest = 0
        crossoverHighest = 0
        positive = predicted_sequence[0] > 0
        
        for i in range(0,len(predicted_sequence)):
            total = total + predicted_sequence[i]
            if positive:
                if total < 0:
                    crossoverHighest = total
                    for j in range(i+1,len(predicted_sequence)):
                        total = total + predicted_sequence[j]
                        if total > 0:
                            break
                        if crossoverHighest > total:
                            crossoverHighest = total
                    break
                if highest < total:
                    highest = total
            else:
                if total > 0:
                    crossoverHighest = total
                    for j in range(i+1,len(predicted_sequence)):
                        total = total + predicted_sequence[j]
                        if total < 0:
                            break
                        if crossoverHighest < total:
                            crossoverHighest = total
                    break
                if highest > total:
                    highest = total
        
        highest = abs(highest)
        crossoverHighest = abs(crossoverHighest)
        percentChange = highest / todaysData.iloc[-1]['Close'] * 100
        crossoverPercentChange = crossoverHighest / todaysData.iloc[-1]['Close'] * 100

        if self.long == False and self.short == False:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = True
                return 'GOLONG'
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = True
                return 'GOSHORT'
            else:
                return ''
        elif self.long == True:
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                self.short = True
                return 'GOSHORT'
            elif not positive and crossoverPercentChange > percentChange:
                print('SELL')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                return 'SELL'
            else:
                return ''
        elif self.short == True:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.profit = self.lastPrice - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                self.long = True
                return 'GOLONG'
            elif positive and crossoverPercentChange > percentChange:
                print('BUY')
                self.profit = self.lastPrice - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                return 'BUY'
            else:
                return ''



class CrossoverAnalyzerUpdated(Analyzer):
    def __init__(self):
        self.long = False
        self.short = False
        self.closed = False
        self.lastPrice = 0
        self.totalWin = 0
        self.name = 'CrossoverUpdated'
        self.tradeNum = 0
        self.profit = 0
 
    def action(self, predicted_sequence, todaysData):
        self.closed = False
        total = 0
        highest = 0
        crossoverHighest = 0
        positive = predicted_sequence[0] > 0
        
        for i in range(0,len(predicted_sequence)):
            total = total + predicted_sequence[i]
            if positive:
                if total < 0:
                    crossoverHighest = total
                    for j in range(i+1,len(predicted_sequence)):
                        total = total + predicted_sequence[j]
                        if total > 0:
                            break
                        if crossoverHighest > total:
                            crossoverHighest = total
                    break
                if highest < total:
                    highest = total
            else:
                if total > 0:
                    crossoverHighest = total
                    for j in range(i+1,len(predicted_sequence)):
                        total = total + predicted_sequence[j]
                        if total < 0:
                            break
                        if crossoverHighest < total:
                            crossoverHighest = total
                    break
                if highest > total:
                    highest = total
        
        highest = abs(highest)
        crossoverHighest = abs(crossoverHighest)
        percentChange = highest / todaysData.iloc[-1]['Close'] * 100
        crossoverPercentChange = crossoverHighest / todaysData.iloc[-1]['Close'] * 100

        if self.long == False and self.short == False:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = True
                return 'GOLONG'
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = True
                return 'GOSHORT'
            else:
                return ''
        elif self.long == True:
            if not positive and percentChange > 0.05:
                print('GOSHORT')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                self.short = True
                return 'GOSHORT'
            elif not positive and crossoverPercentChange > percentChange:
                print('SELL')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                return 'SELL'
            elif positive and crossoverPercentChange > percentChange:
                print('SELL')
                self.profit = todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.closed = True
                self.totalWin = self.totalWin + todaysData.iloc[-1]['Close'] - self.lastPrice 
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.long = False
                return 'SELL'
            else:
                return ''
        elif self.short == True:
            if positive and percentChange > 0.05:
                print('GOLONG')
                self.profit = self.lastPrice - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                self.long = True
                return 'GOLONG'
            elif positive and crossoverPercentChange > percentChange:
                print('BUY')
                self.profit = self.lastPrice - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                return 'BUY'
            elif not positive and crossoverPercentChange > percentChange:
                print('BUY')
                self.profit = self.lastPrice - todaysData.iloc[-1]['Close']
                self.closed = True
                self.totalWin =  self.totalWin + self.lastPrice - todaysData.iloc[-1]['Close']
                self.lastPrice = todaysData.iloc[-1]['Close']
                self.short = False
                return 'BUY'
            else:
                return ''