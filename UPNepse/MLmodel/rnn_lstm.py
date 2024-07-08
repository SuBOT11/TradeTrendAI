import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd
import random 



# Function to preprocess data
def preprocess_data(df, sequence_length):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['Close']])

    X, y = [], []
    for i in range(len(df_scaled) - sequence_length):
        X.append(df_scaled[i:i + sequence_length])
        y.append(df_scaled[i + sequence_length])
    X, y = np.array(X), np.array(y)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return scaler, X_train, X_test, y_train, y_test

# Function to train LSTM model
def train_lstm_model(X_train, y_train):
    model = Sequential()
    model.add(LSTM(50, activation='sigmoid', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(50, activation='tanh'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss=MeanSquaredError())
    model.fit(X_train, y_train, epochs=64, batch_size=4, verbose=2)
    return model

# Function to save model to HDF5 file
def save_model_to_h5(model, filename):
    model.save(filename)


# Function to load model from HDF5 file
def load_model_from_h5(filename):
    return load_model(filename)

def make_predictions(df_selected,symbol):
# Sample usage
    sequence_length = 100# Example sequence length
    try:
        model = load_model('/mnt/d/CollegeProject/UPNepse/MLmodel/trained_model.keras')
    except Exception as e:
        model = Sequential()
        print("model file not found ")
    df = df_selected 
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df.dropna()

    scaler, X_train, _, y_train, _ = preprocess_data(df, sequence_length)
    if not model.layers:
        model = train_lstm_model(X_train, y_train)
        save_model_to_h5(model,'/mnt/d/CollegeProject/UPNepse/MLmodel/trained_model.keras')
    # predict tomorrow's price

    dates = []
    predictions = []

    last_date = df.index[-1]
    last_50_days = df.tail(sequence_length)
    last_50_days_scaled = scaler.transform(last_50_days[['Close']])
    last_50_days_scaled = np.array(last_50_days_scaled).reshape((1, sequence_length, 1))

    for _ in range(7):
        # Predict the next day's value
        next_day_prediction = model.predict(last_50_days_scaled)[0, 0]
        next_date = last_date + pd.DateOffset(days=1)
        random_int  = random.randint(1,20)
        rand_dec = random.randint(0,5)
        if (rand_dec > rand_dec):
            rand_dec = 0
        else:
            rand_dec = 1
        if rand_dec == 0:
            next_day_prediction = next_day_prediction - random_int
        else:
            next_day_prediction = next_day_prediction + random_int

        # Store the prediction
        predictions.append(next_day_prediction)
        dates.append(next_date)

        # Update last_50_days_scaled to include the new prediction
        last_50_days_scaled = np.roll(last_50_days_scaled, -1)
        last_50_days_scaled[-1, -1] = next_day_prediction
        last_date = next_date

    # Inverse transform the predictions
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    predicted_df = pd.DataFrame({"Date":dates, 'Prediction':predictions.flatten(),'Symbol': symbol})
    print(predictions.flatten()) 
    print(predicted_df)
    return predicted_df
