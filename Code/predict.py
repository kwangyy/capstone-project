import pickle
import pandas as pd

from flask import Flask
from flask import request
from flask import jsonify

model_file = 'xgbclassifier.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('bank_prediction')
def preprocess(customer):
    customer_data = pd.DataFrame()
    customer_data = customer_data.append(customer, ignore_index=True)
    del customer_data['duration']
    if customer_data['y'].dtype == object:
        customer_data['target'] = (customer_data.y == 'yes').astype(int)
        del customer_data['y']
    else:
        customer_data['target'] = customer_data['y']
        del customer_data['y']
    customer_data_dict = customer_data.to_dict(orient='records')
    return customer_data_dict


@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    customer_preprocessed = preprocess(customer)
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    bank_pred = y_pred >= 0.29

    result = {
        'pred_probability': float(y_pred),
        'pred': bool(bank_pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
