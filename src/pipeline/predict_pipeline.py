import os
import sys
import pandas as pd
import numpy
from src.exception import CustomException
from  src.utils import load_object
from src.logger import logging


##20 
class PredictPipeline:
    def __init__(self):
        pass
    ## 23 go to utils.py
    def predict(self,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path= 'artifacts\preprocessor.pkl' # preprocess the input data
            logging.info("before loading")
            model=load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print(preprocessor)
            print(features)
            logging.info(features)
            logging.info("after loading")
            indata_scaled = preprocessor.transform(features)
            logging.info("prepeocessing done")
            preds = model.predict(indata_scaled)
            return preds
        ## 25 go to application.py
        except Exception as e:
            raise logging.info(CustomException(e,sys))
##21
class CustomData:
    def __init__(self,
         age:float, bp:float, sg:float,al:float,
         su:float, bgr:float, bu:float, sc:float, sod:float,
         pot:float, hemo:float,pcv:float,wc:float,rc:float,
         rbc:str,pc:str,pcc:str,ba:str,htn:str,dm:str,cad:str,appet:str,pe:str,ane:str):
        ## check carefully theseinput variable name in html page , datatype

         self.age = age
         self.bp = bp
         self.sg = sg
         self.al = al
         self.su = su
         self.bgr = bgr
         self.bu = bu
         self.sc = sc
         self.sod=sod
         self.pot = pot
         self.hemo = hemo
         self.pcv = pcv
         self.wc = wc
         self.rc=rc
         self.rbc = rbc
         self.pc = pc
         self.pcc = pcc
         self.ba = ba
         self.htn = htn
         self.dm = dm
         self.cad = cad
         self.appet = appet
         self.pe = pe
         self.ane = ane
##22
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict ={
                'age':[self.age], 'bp':[self.bp], 'sg':[self.sg], 'al':[self.al], 'su':[self.su],
                'bgr':[self.bgr], 'bu':[self.bu], 'sc':[self.sc], 'sod':[self.sod], 'pot':[self.pot],
                'hemo':[self.hemo],'pcv':[self.pcv],'wc':[self.wc],'rc':[self.rc],
                'rbc':[self.rbc],'pc':[self.pc],'pcc':[self.pcc],'ba':[self.ba],'htn':[self.htn],
                'dm':[self.dm],'cad':[self.cad],'appet':[self.appet],'pe':[self.pe],'ane':[self.ane]

            }
            ### rearange the columns like raw data
            df = pd.DataFrame(custom_data_input_dict)
            # return df.to_numpy()
            return df

        except Exception as e:
            raise logging.info(CustomException(e,sys))
            