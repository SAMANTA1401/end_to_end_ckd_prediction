import sys
import os

from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder, OrdinalEncoder, MinMaxScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# 10. after data ingestion
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")
# 11.
class DataTransformation:
    # 11.1
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    # 11.2
    def get_data_transformer_object(self):
        ''' this function is responsible for data transformation '''
        try:
            numerical_columns = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo','pcv','wc','rc']
            categorical_columns = ['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane'] #,'classification'

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                    # ('scaler',MinMaxScaler())
                    ]

                )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    # ('imputer1',SimpleImputer(missing_values='\t?', strategy='constant', fill_value='most_frequent')),
                    # ('imputer2',SimpleImputer(missing_values='\tno', strategy='constant', fill_value='no')),
                    # ('imputer3',SimpleImputer(missing_values='\tyes', strategy='constant', fill_value='yes')),
                    # ('imputer4',SimpleImputer(missing_values=' yes', strategy='constant', fill_value='yes')),
                    # ('imputer5',SimpleImputer(missing_values='\t43', strategy='constant', fill_value='43')),
                    # ('imputer6',SimpleImputer(missing_values='\t6200', strategy='constant', fill_value='6200')),
                    # ('imputer7',SimpleImputer(missing_values='\t8400', strategy='constant', fill_value='8400')),
                    # ('imputer',SimpleImputer(missing_values='ckd\t', strategy='constant', fill_value='ckd')),
                    # ('ordinal_encoder',OrdinalEncoder()),
                    ('one_hot_encoder',OneHotEncoder()),

                    ("scaler",StandardScaler(with_mean=False))
                    # ('scaler',MinMaxScaler())


                ]
            )
            logging.info("categorical columns encoding completed")
            logging.info("Numerical columns standard scalling completed")

            # 11.2.1
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipelines",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise logging.info(CustomException(e,sys))
            
    #11.3
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name="classification"
            numerical_columns = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo','pcv','wc','rc']

            input_feature_train__df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test__df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]



            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train__df)
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test__df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr =  np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("saved preprocessing object. ")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )



            # before utils
        except Exception as e:
            raise logging.info(CustomException(e,sys))
        