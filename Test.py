import pandas as pd
import math, datetime
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = pd.read_csv('C:/USERS/Stephen/Desktop/UNI/Python/Corona.csv', skiprows=1)
df.columns = ['Day','Cases','NewCases','Deaths','NewDeaths']
df = df[['Cases','NewCases','Deaths','NewDeaths']]

#FORCAST WHAT...
forecast_col = 'Deaths'
#Fill in missing data
df.fillna(-99999, inplace=True)

#0.1 10 percent before to get next / can change this will likely change accuracy
forecast_out = int(math.ceil(0.05* len(df)))
#how many days we are forecasting
print(forecast_out)
#shift columns negatively 10 days in future
df['label'] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out:]

df.dropna(inplace=True)#Drop missing data
y = np.array(df['label'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

#algorithm / could comment out as we are loading the file i.e pickle_in
clf = LinearRegression(n_jobs=-1) # Default 1 thread -1 for max
#clf = LinearRegression(n_jobs = 10) # 10 threads
#clf = svm.SVR() # Horrid support vector machine
#clf = svm.SVR(kernel='poly') # Also horrid polynomial support vector machine
#train
clf.fit(X_train, y_train)
#Save the model here
with open('linearregression.pickle','wb') as f:
    pickle.dump(clf,f)
#open model here
pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)
    
#test / accuracy is the mean squared error
accuracy = clf.score(X_test, y_test)
#print(accuracy)
#Predict
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)

#Unfortunetly the graph doesnt work so well
#cant get it to show the forecast
df['Forecast'] = np.nan
plt.xlim([0, 150])
plt.ylim([0, 500000])

print(df.tail())

df['Deaths'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Day')
plt.ylabel('Deaths')
plt.show()
