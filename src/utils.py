import os 
import sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import f1_score , accuracy_score, precision_recall_curve
from sklearn.preprocessing import OrdinalEncoder 


# 12 after data transformation then go data ingestion
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    
    except Exception as e:
        raise logging.info(CustomException(e,sys))

## 16 after 
def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report = {}

        for i in range(len(list(models))-1):
            model = list(models.values())[i]

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_f1_score =f1_score(y_train, y_train_pred,pos_label="ckd")

            test_model_f1_score = f1_score(y_test,y_test_pred,pos_label="ckd")
            test_model_accuracy_score = accuracy_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_f1_score

            logging.info(f"Model {list(models.keys())[i]} Test F1 Score :{test_model_f1_score} Accuracy :{test_model_accuracy_score}")


        ## for neural network 
        X_train = np.asarray(X_train).astype(np.float32)
        X_test = np.asarray(X_test).astype(np.float32)
    
        y_test = y_test.reshape(-1,1)
        y_train = y_train.reshape(-1,1)

        enco=OrdinalEncoder()
        y_test = enco.fit_transform(y_test)
        y_train = enco.fit_transform(y_train)

        modelNN = list(models.values())[-1]
        modelNN.fit(X_train, y_train,validation_data=(X_test, y_test),epochs=5, verbose=1) #

        y_test_pred = model.predict(X_test)

        y_test_pred = y_test_pred.reshape(-1,1)
        y_test_pred = enco.fit_transform(y_test_pred)
        #evauate model
        loss,test_model_accuracy_score = modelNN.evaluate(X_test, y_test,verbose=0)
        def calc_f1(prec, recall):
            return 2*(prec*recall)/(prec+recall) if prec or recall else 0
        precision,recall,thresholds = precision_recall_curve(y_test,y_test_pred)
        f1_sco = [calc_f1(precision[i],recall[i]) for i in range(len(thresholds))]
        fi_max = np.argmax(f1_sco)
        test_model_f1_score = f1_sco[fi_max]

        report[list(models.keys())[-1]] = test_model_f1_score
        logging.info(f"Model {list(models.keys())[-1]} Test F1 Score :{test_model_f1_score} Accuracy :{test_model_accuracy_score}")

        return report

    except Exception as e:
        raise logging.info(CustomException(e,sys))