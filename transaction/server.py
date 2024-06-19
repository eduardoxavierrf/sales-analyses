from flask import Flask, jsonify, request
import pandas as pd
from joblib import load

app = Flask(__name__)

# Load the pre-trained model
model = load('monitoring/iso_forest.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    status = ['approved', 'denied', 'refunded', 'reversed', 'backend_reversed', 'failed', 'processing']

    transactions = pd.DataFrame.from_dict(data)
    transactions['total_count'] = transactions.groupby(['time'])['count'].transform('sum')
    transactions['percentage'] = (transactions['count'] / transactions['total_count']) * 100

    transactions_pivot = transactions.pivot_table(index=['time'], columns='status', values='percentage', aggfunc='sum', fill_value=0).reset_index()
    transactions_pivot = transactions_pivot.reindex(columns=status, fill_value=0)
    
    prediction = model.predict(transactions_pivot[status])
    
    return jsonify({'prediction': prediction.tolist()[0]})

if __name__ == '__main__':
    app.run(debug=True)
