import argparse
import os

import pandas as pd
import pyarrow

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def load_dataset():
    trainx_dataset = pd.read_parquet(
        os.path.join(os.environ["SM_CHANNEL_TRAINX"], "trainX.parquet"))
    
    trainy_dataset = pd.read_parquet(
        os.path.join(os.environ["SM_CHANNEL_TRAINY"], "trainY.parquet"))
    
    testx_dataset = pd.read_parquet(
        os.path.join(os.environ["SM_CHANNEL_TESTX"], "testX.parquet"))
    
    testy_dataset = pd.read_parquet(
        os.path.join(os.environ["SM_CHANNEL_TESTY"], "testY.parquet"))
    
    trainx = trainx_dataset.to_numpy().reshape(22500, 40)
    trainy = trainy_dataset['label'].astype(int).to_numpy()
    testx = testx_dataset.to_numpy().reshape(7500, 40)
    testy = testy_dataset['label'].astype(int).to_numpy()
    
    return trainx, trainy, testx, testy

def train(args):
    trainX, trainY, testX, testY = load_dataset()
    print(trainX.shape, trainY.shape)
    print(testX.shape, testY.shape)
    print(trainX.dtype, testX.dtype) 
    print(trainY.dtype, testY.dtype) 
    
    model = Sequential()
    model.add(Dense(100,input_shape=(40,),activation='relu'))
    model.add(Dense(100,activation='relu'))
    model.add(Dense(100,activation='relu'))
    model.add(Dense(10,activation='softmax'))\
    
    model.summary()
    
    model.compile(loss='sparse_categorical_crossentropy',
              metrics=['accuracy'],
              optimizer='adam')
    
    model.fit(trainX,trainY,validation_data=(testX,testY),epochs=args.epochs,batch_size=args.per_device_train_batch_size,verbose=1)
    
    model.save(os.path.join(args.model_dir, '1'), save_format='tf')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--per-device-train-batch-size", type=int, default=32)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=10)
    parser.add_argument("--learning-rate", type=float, default=0.0001)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    
    
    args, _ = parser.parse_known_args()
    
    train(args)
    
    
    
    
    
    
 
    

    
    
    
    





    

    


    
