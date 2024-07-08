import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from numpy import mean
from numpy import std
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from matplotlib import pyplot
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import os
from rnn_lstm import make_predictions
from db import connect_to_mongodb

f_path = '/mnt/d/CollegeProject/UPNepse/data_load/data/'
all_files = os.listdir(f_path)


def write_predictions_data_todb(sym,latest_date,predic_df):
    client = connect_to_mongodb()
    db = client['prediction_db']
    prediction_data = {
        "symbol" :sym, 
        "last_date": latest_date ,
        "prediction_values" : predic_df.to_dict(orient='records')


    }

    collection.insert_one(prediction_data)
def write_history_to_db(sym,last_date,history_df):
    client = connect_to_mongodb()
    db = client['prediction_db']
    if 'history' in db.list_collection_names(): 
        db['history']
    collection = db['history']
    history_data = {
        "symbol" : sym,
        "last_date": last_date,
        "history_values": history_df.to_dict(orient='records')


    }
    collection.insert_one(history_data)


for file_n in all_files:
    df = pd.read_parquet(f'/mnt/d/CollegeProject/UPNepse/data_load/data/{file_n}')
    print("df head ------------------->")
    print(df.tail())
    df_with_date = pd.read_parquet(f'/mnt/d/CollegeProject/UPNepse/data_load/data/{file_n}')
    if df_with_date.empty:
        continue
    symbol = df['symbol'].iloc[0]
    latest_date = df_with_date['date'].max()
    features_to_ = ['date','Close','symbol','bonus_dividend', 'cash_dividend', 'book_closure_flag', 'news_flag',
           'year', 'month', 'day_of_week','Open', 'High', 'Low', 'Volume', 'SMA_20', 'SMA_100', 'EMA_20',
           'EMA_100', 'RSI_14', 'ROC_12', 'ATR_14', 'SD_20', 'OBV', 'ADX_14',
           'gap_up', 'gap_down', 'price_change']
    column_to_drop= []

    history_df = df_with_date[['date','Close']]
    write_history_to_db(symbol,latest_date,history_df)
    for col in df.columns:
        if col not in features_to_:
            column_to_drop.append(col)


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df.drop(['date','symbol'],axis=1,inplace=True)
    if 'gap_down' in df.columns:
        df.drop('gap_down',axis=1,inplace=True)
    df.rename(columns={'gap_up':'gap'},inplace=True) 
    df.drop(columns=column_to_drop,axis=1,inplace=True)

    X = df.drop(columns=['Close'])
    y = df['Close']
    X_train , X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

    def get_models():
        models = dict()
        for i in range(2,23,1):

            rfe = RFE(estimator=DecisionTreeRegressor(), n_features_to_select=i)
            model = DecisionTreeRegressor()
            models[str(i)] = Pipeline(steps=[('s',rfe),('m',model)])
        return models,rfe

    def evaluate_model(model,X,y):
        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        scores = cross_val_score(model, X, y, scoring='r2', cv=cv, n_jobs=-1, error_score='raise')

    def get_eval_results():
        models,rfe = get_models()
        # evaluate the models and store results
        results, names = list(), list()
        for name, model in models.items():
            model.fit(X_train,y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_r2 = r2_score(y_train,y_train_pred)
            test_r2 = r2_score(y_test,y_test_pred)

            print(f"Model: {model}")
            print(f"Training R-squared: {train_r2}")
            print(f"Test R-squared: {test_r2}")
            print("="*50)

            for i in range(X.shape[1]):
                print('Column: %d, Selected %s, Rank: %.3f' % (i, model.support_[i], model.ranking_[i]))




            scores = evaluate_model(model, X, y)
            results.append(scores)
            names.append(name)
        print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))
        # plot model performance for comparison
        pyplot.boxplot(results, labels=names, showmeans=True)
        pyplot.show()



    rfe = RFE(estimator=DecisionTreeRegressor(), n_features_to_select=1)
    rfe.fit(X,y)


    selected_features = X.columns[rfe.support_]
    X_selected = X[selected_features]

    df_selected = pd.concat([X_selected,y],axis=1)
    df_selected = pd.concat([df_selected,df_with_date['date']],axis=1)
    df_predicted = make_predictions(df_selected,symbol)

    write_predictions_data_todb(symbol,latest_date,df_predicted)





