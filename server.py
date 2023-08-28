import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers

fileName = 'c:\Users\tmcna\Downloads\SPY.csv'
df = pd.read_csv(fileName)
df