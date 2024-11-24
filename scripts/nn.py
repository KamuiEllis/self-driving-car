import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

class nn:
    def __init__(self, dataset):
        self.dataset = pd.DataFrame(dataset)
        x = self.dataset.iloc[:, :4].values
        y = tf.keras.utils.to_categorical(self.dataset.iloc[:, -1].values, num_classes=4)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x,y, test_size=0.2, random_state=0)

    async def train(self):
        try:
            ann = tf.keras.models.load_model('car.keras')
        except:    
            ann = tf.keras.models.Sequential()
            ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
            ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
            ann.add(tf.keras.layers.Dense(units=4, activation='softmax'))  
            ann.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss = 'categorical_crossentropy' , metrics = ['accuracy'])
        ann.fit(self.x_train, self.y_train, batch_size = 32, epochs = 1500)
        self.saveModel(ann)
      

    def saveModel(self, ann):
        ann.save('car.keras')

    def predictDirection(self, value):
        ann = tf.keras.models.load_model('car.keras')
        result = ann.predict(np.array([value]))   
        return result 