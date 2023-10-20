from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed, BatchNormalization
from tensorflow.keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler, EarlyStopping
import tensorflow as tf
from abc import ABC, abstractmethod
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Model(ABC):
    def __init__(self, df):
        self.name = 'abstract'
        self.numInput = 1
        self.numOutput = 1
        self.inputs = []
        self.outputs = []
        self.inputScalar = MinMaxScaler()
        self.outputScalar = MinMaxScaler()
        self.df = df
 
    def build(self):
        pass

class BasicModel(Model):
    def __init__(self, df):
        self.name = 'basic'
        self.numInput = 1
        self.numOutput = 1
        self.inputs = ['Difference']
        self.outputs = ['Difference']
        self.outputScalar = MinMaxScaler()
        df[self.outputs] = self.outputScalar.fit_transform(df[self.outputs])
        self.df = df
 
    def build(self):
        maxSteps = len(self.df.time.unique())
        for i in range(1, maxSteps):
            # Create sequences of past and future data
            X = []
            y = []

            for currentDate in self.df.date.unique():
                past_sequence = self.df[self.inputs].loc[self.df['date']==currentDate][0:i]
                future_sequence = self.df[self.outputs][self.df['date']==currentDate][i:maxSteps]
                X.append(past_sequence)
                y.append(future_sequence)

            X = np.array(X)
            y = np.array(y)
        
            # Define the model
            model = Sequential()
            model.add(LSTM(50, activation='relu', input_shape=(i, self.numInput)))
            model.add(Dense(maxSteps - i))
            model.compile(optimizer='adam', loss='mean_squared_error')

            # Train the model (you can adjust the number of epochs and batch size)
            model.fit(X, y, epochs=20, batch_size=32)

            modelName = 'model_'+str(self.df.time.unique()[i-1]).replace(':','_')+'.keras'
            print(modelName)
            model.save(modelName)

class BatchClipEarlyStopDSFV(Model):
    def __init__(self, df):
        self.name = 'basic'
        self.numInput = 4
        self.numOutput = 1
        self.inputs = ['Difference','slowsma','fastsma','Volume']
        self.outputs = ['Difference']
        self.inputScalar = MinMaxScaler()
        self.outputScalar = MinMaxScaler()
        df[self.inputs] = self.inputScalar.fit_transform(df[self.inputs.remove('Difference')])
        df[self.outputs] = self.outputScalar.fit_transform(df[self.outputs])
        self.df = df
 
    def build(self):
        maxSteps = len(self.df.time.unique())
        for i in range(1, maxSteps):
            # Create sequences of past and future data
            X = []
            y = []

            for currentDate in self.df.date.unique():
                past_sequence = self.df[self.inputs].loc[self.df['date']==currentDate][0:i]
                future_sequence = self.df[self.outputs][self.df['date']==currentDate][i:maxSteps]
                X.append(past_sequence)
                y.append(future_sequence)

            X = np.array(X)
            y = np.array(y)
        
            # Define the model
            model = Sequential()
            model.add(LSTM(50, activation='relu', input_shape=(i, self.numInput)))
            model.add(BatchNormalization())
            model.add(Dense(maxSteps - i))
            optimizer = Adam(clipnorm=0.001)
            model.compile(optimizer=optimizer, loss='mean_squared_error')
            
            early_stopping = EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)
            # Train the model (you can adjust the number of epochs and batch size)
            model.fit(X, y, epochs=100, callbacks=[early_stopping])

            modelName = 'model_'+str(self.df.time.unique()[i-1]).replace(':','_')+'.keras'
            print(modelName)
            model.save(modelName)