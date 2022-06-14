import os
import pickle
import pandas as pd
from flask import Flask, request, Response
import os

from rossmann.rossmann import Rossmann



# load model
# model = pickle.load(open('./model/model_xgb.file', 'rb'))
with open("./model/model_xgb.file", "rb") as file:
    model_xgb_tuned = pickle.load(file)

# start API
app = Flask(__name__)


@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        # start Rossmann class
        pipeline = Rossmann()

        # cleaning data
        df1 = pipeline.data_cleaning(test_raw)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model_xgb_tuned, test_raw, df3)

        return df_response

    else:
        return Response('{}', status=200, mimetype='application/json')


if __name__ == '__main__':
    os.environ.get('PORT', 5000)
    app.run('0.0.0.0')


