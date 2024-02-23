from flask import Flask, request, render_template, url_for,redirect
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

## 19  then go predict pipeline
application=Flask( __name__)

app=application
#route for home page
@app.route('/')
def index():
    return render_template( 'index.html' )
 
@app.route('/predictdata', methods=['GET','POST'])
def predict_data(): 
    if request.method == "GET":
        return render_template('home.html')
    else:
## 21 after predict pipeline
## 26 
        data = CustomData(
            age =float(request.form.get('age')),
            bp =float(request.form.get('bp')),
            sg =float(request.form.get('sg')),
            al =float(request.form.get('al')),
            su =float(request.form.get('su')),
            bgr =float(request.form.get('bgr')),
            bu =float(request.form.get('bu')),
            sc =float(request.form.get('sc' )),
            sod=float(request.form.get('sod')),
            pot =float(request.form.get('pot')),
            hemo =float(request.form.get('hemo')),
            pcv =float(request.form.get('pcv')),
            wc =float(request.form.get('wc')),
            rc=float(request.form.get('rc')),
            rbc=request.form.get('rb'),
            pc =request.form.get('pc'),
            pcc=request.form.get('pcc'),
            ba =request.form.get('ba'),
            htn =request.form.get('htn'),
            dm =request.form.get('dm'),
            cad = request.form.get('cad'),
            appet = request.form.get('appet'),
            pe =request.form.get('pe'),
            ane =request.form.get('ane')
        )
        pred_df = data.get_data_as_data_frame()
        print(pred_df) ## input data frame

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df) 

        return render_template('home.html',results=results[0])



if __name__=='__main__':
    app.run(debug=True)
        