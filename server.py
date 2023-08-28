import pandas as pd
import datetime
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from copy import deepcopy

fileName = 'C:\\src\\stockPredictor\\SPY.csv'
df = pd.read_csv(fileName)
df = df[['Date', 'Close']]

df['Change'] = 0
df['Change'] = df['Change'].astype(int)
##putting the first value as 0
df['Change'].loc[0] = 0

for index in range(1,df.shape[0]):  
    difference = df['Close'].iloc[index] - df['Close'].iloc[index-1]
    if(difference == 0):
        df['Change'].iloc[index]=0
    elif(difference > 0):
        percentChange = (1-df['Close'].iloc[index-1]/df['Close'].iloc[index])*100
        if(percentChange > 1):
            df['Change'].iloc[index]=3
        elif(percentChange > .5):
            df['Change'].iloc[index]=2
        elif(percentChange > .25):
            df['Change'].iloc[index]=1
        elif(percentChange > 0):
            df['Change'].iloc[index]=0
    elif(difference < 0):
        percentChange = (1-df['Close'].iloc[index]/df['Close'].iloc[index-1])*100
        if(percentChange > 1):
            df['Change'].iloc[index]=-3
        elif(percentChange > .5):
            df['Change'].iloc[index]=-2
        elif(percentChange > .25):
            df['Change'].iloc[index]=-1
        elif(percentChange > 0):
            df['Change'].iloc[index]=0

def str_to_datetime(s):
  split = s.split('-')
  year, month, day = int(split[0]), int(split[1]), int(split[2])
  return datetime.datetime(year=year, month=month, day=day)

datetime_object = str_to_datetime('1986-03-19')
df['Date'] = df['Date'].apply(str_to_datetime)
df.index = df.pop('Date')

def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
  first_date = str_to_datetime(first_date_str)
  last_date  = str_to_datetime(last_date_str)

  target_date = first_date
  
  dates = []
  X, Y = [], []

  last_time = False
  while True:
    df_subset = dataframe.loc[:target_date].tail(n+1)
    
    if len(df_subset) != n+1:
      print(f'Error: Window of size {n} is too large for date {target_date}')
      return

    values = df_subset['Change'].to_numpy()
    x, y = values[:-1], values[-1]

    dates.append(target_date)
    X.append(x)
    Y.append(y)

    next_week = dataframe.loc[target_date:target_date+datetime.timedelta(days=7)]
    next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
    next_date_str = next_datetime_str.split('T')[0]
    year_month_day = next_date_str.split('-')
    year, month, day = year_month_day
    next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))
    
    if last_time:
      break
    
    target_date = next_date

    if target_date == last_date:
      last_time = True
    
  ret_df = pd.DataFrame({})
  ret_df['Target Date'] = dates
  
  X = np.array(X)
  for i in range(0, n):
    X[:, i]
    ret_df[f'Target-{n-i}'] = X[:, i]
  
  ret_df['Target'] = Y

  return ret_df

windowed_df = df_to_windowed_df(df, 
                                '2000-08-25', 
                                '2023-08-25', 
                                n=3)

def windowed_df_to_date_X_y(windowed_dataframe):
  df_as_np = windowed_dataframe.to_numpy()

  dates = df_as_np[:, 0]

  middle_matrix = df_as_np[:, 1:-1]
  X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

  Y = df_as_np[:, -1]

  return dates, X.astype(np.int32), Y.astype(np.int32)

dates, X, y = windowed_df_to_date_X_y(windowed_df)

q_80 = int(len(dates) * .8)
q_90 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

model = Sequential([layers.Input((3, 1)),
                    layers.LSTM(7),
                    layers.Dense(7, activation='relu'),
                    layers.Dense(7, activation='relu'),
                    layers.Dense(1)])

model.compile(loss='mse', 
              optimizer=Adam(learning_rate=0.001))

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20)
train_predictions = model.predict(X_train).flatten()
val_predictions = model.predict(X_val).flatten()
test_predictions = model.predict(X_test).flatten()

count = 0
for index in range(1,test_predictions.shape[0]):  
   if((y_test[index]>0 and test_predictions[index]>0) or (y_test[index]<0 and test_predictions[index]<0)):
      count = count + 1
      
print((1-count/test_predictions.shape[0])*100)

# recursive_predictions = []
# recursive_dates = np.concatenate([dates_val, dates_test])

# for target_date in recursive_dates:
#   last_window = deepcopy(X_train[-1])
#   next_prediction = model.predict(np.array([last_window])).flatten()
#   recursive_predictions.append(next_prediction)
#   last_window[-1] = next_prediction

