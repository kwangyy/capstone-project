import requests

url = 'http://localhost:9696/predict'

customer_id = 'xyz-123'
customer = {'age': 37,
            'job': 'technician',
            'marital': 'single',
            'education': 'university.degree',
            'default': 'no',
            'housing': 'yes',
            'loan': 'no',
            'contact': 'telephone',
            'month': 'may',
            'day_of_week': 'thu',
            'duration': 30,
            'campaign': 1,
            'pdays': 999,
            'previous': 0,
            'poutcome': 'nonexistent',
            'emp.var.rate': 1.1,
            'cons.price.idx': 93.994,
            'cons.conf.idx': -36.4,
            'euribor3m': 4.86,
            'nr.employed': 5191.0,
            'y': 'no'}

response = requests.post(url, json=customer).json()
decision = response['pred']
probability = response['pred_probability']

if decision == True:
    print('Sending email to %s, probability is %.9f' % (customer_id, probability))
else:
    print('Not sending email to %s, probability is %.9f' % (customer_id, probability))

