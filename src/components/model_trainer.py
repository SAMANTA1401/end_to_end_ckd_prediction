import os
import sys
from dataclasses import dataclass
from imblearn.over_sampling import RandomOverSampler

from sklearn.ensemble import  RandomForestClassifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

# import tensorflow as tf
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.optimizers import Adam

from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import f1_score , accuracy_score

from src.utils import save_object, evaluate_models

##14. 
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")
## 15
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    ## 15.2
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("split training and test input data")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], 
                train_array[:,-1],  
                test_array[:, :-1],  
                test_array[:, -1]

            )
            ## label balancing
            ros = RandomOverSampler()
            X_ros, y_ros = ros.fit_resample(X_train,y_train)

            # create neural network
            def NNModel():
                Classifier = Sequential()
                Classifier.add(Dense(15,input_shape=(X_ros.shape[1],),activation = 'relu'))
                Classifier.add(Dropout(0.2))
                Classifier.add(Dense(15, activation='relu'))
                Classifier.add(Dropout(0.4))
                Classifier.add(Dense(1, activation='sigmoid'))
                Classifier.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
                return Classifier
    

            models = {
                "Random Forest Classifier": RandomForestClassifier(),
                "Decision Tree Classifier": DecisionTreeClassifier(random_state=42),
                "Support Vector Machine": SVC(),
                "Naive Bays Classifier" : GaussianNB(),
                "Neural Network" :  NNModel()
            }
            ##15.3 go to utils.py ## 16
            model_report:dict=evaluate_models(X_train=X_ros,y_train=y_ros,X_test=X_test,y_test=y_test, models=models)
          ### 17 after evaluate model
            ## to get the best model
            best_model_f1_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_f1_score)
            ]  

            best_model = models[best_model_name]

            if best_model_f1_score<0.7:
                raise logging.info(CustomException("No best model found"))

            logging.info(f"The Best Model for this dataset is {best_model_name}:{best_model}  with a f1-Score of {best_model_f1_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(X_test)
            f1_sco = f1_score(y_test,predicted,pos_label="ckd")
            accuracy = accuracy_score(y_test,predicted)

            return best_model_name,f1_sco, accuracy

        except Exception as e:
            raise logging.info(CustomException(e,sys))
            
