#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import csv
import pandas as pd



app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method =='GET':
        return render_template('index.html')
    elif request.method=='POST':
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(prediction[0], 2)

        return render_template('index.html',eng_size=int_features[0], cylinders=int_features[1], fuel=int_features[2], emission=output, scroll="prediction")

@app.route('/suggest',methods=['POST'])
def suggest():
    filters = [x for x in request.form.values()]
    print(filters)
    
    data = pd.read_csv("FuelConsumption.csv")

    if (filters[0]=='' and filters[1]=='' and filters[2]==''):
        filt=data.head(8)
    elif filters[0]=='' and filters[1]=='':
        filt=data[(data['MAKE']==filters[2])]
    elif filters[0]=='' and filters[2]=='':
        filt=data[(data['VEHICLE CLASS']==filters[1])]
    elif filters[1]=='' and filters[2]=='':
        filt=data[(data['FUELTYPE']==filters[0])]
    elif filters[2]=='':
        filt=data[(data['FUELTYPE']==filters[0])&(data['VEHICLE CLASS']==filters[1])]
    elif filters[1]=='':
        filt=data[(data['FUELTYPE']==filters[0])&(data['MAKE']==filters[2])]
    elif filters[0]=='':
        filt=data[(data['VEHICLE CLASS']==filters[1])&(data['MAKE']==filters[2])]
    elif (filters[0]!='' and filters[1]!='' and filters[2]!=''):
        filt=data[(data['FUELTYPE']==filters[0])&(data['VEHICLE CLASS']==filters[1])&(data['MAKE']==filters[2])]
        

    dataset=filt.loc[:,['FUELTYPE','VEHICLE CLASS','MAKE','MODEL','CO2EMISSIONS']]

    if len(dataset)==0:
        return render_template('index.html', scroll="suggestion",fuel_type=filters[0], vehicle_class=filters[1], make=filters[2] ,results=True, not_found=True)
    
    return render_template('index.html', scroll="suggestion",fuel_type=filters[0], vehicle_class=filters[1], make=filters[2] ,results=True, data=dataset.head(8).to_html(index=False,classes = "list"))


if __name__ == "__main__":
    app.run(debug=True)