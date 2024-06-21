from flask import Flask, request, render_template, jsonify
from sklearn.neighbors import NearestNeighbors
import numpy as np

app = Flask(__name__)

offers = [
    {
        "payment_method_name": "SBI Credit Card",
        "offers": [
            {
                "cashback_percentage": 10,
                "max_cashback": 1500,
                "min_spend": 5000,
                "eligible_categories": ["Electronics", "Home Appliances"]
            },
            {
                "cashback_percentage": 5,
                "max_cashback": 500,
                "min_spend": 2000,
                "eligible_categories": ["Fashion", "Groceries"]
            }
        ]
    },
    {
        "payment_method_name": "Amazon Pay ICICI Credit Card",
        "offers": [
            {
                "cashback_percentage": 5,
                "max_cashback": 750,
                "min_spend": 3000,
                "eligible_categories": ["All"]
            }
        ]
    },

]

# Flatten the offers into a list of dictionaries
flattened_offers = []
for payment_method in offers:
    for offer in payment_method['offers']:
        offer_details = {
            "payment_method_name": payment_method['payment_method_name'],
            "cashback_percentage": offer['cashback_percentage'],
            "max_cashback": offer['max_cashback'],
            "min_spend": offer['min_spend'],
            "eligible_categories": offer['eligible_categories']
        }
        flattened_offers.append(offer_details)

# Create a list of unique categories
all_categories = sorted(list(
    set(cat for offer in flattened_offers for cat in offer['eligible_categories'])))

# Prepare the feature matrix and labels
X = []
y = []

for offer in flattened_offers:
    category_vector = [1 if cat in offer['eligible_categories']
                       else 0 for cat in all_categories]
    feature_vector = [offer['min_spend']] + category_vector
    X.append(feature_vector)
    y.append(offer['cashback_percentage'])

X = np.array(X)
y = np.array(y)

# Fit k-NN model
knn = NearestNeighbors(n_neighbors=1)
knn.fit(X)

# Suggestion function


def suggest_max_cashback(spend, category):
    if category not in all_categories:
        return "Category not found."

    category_vector = [1 if cat == category else 0 for cat in all_categories]
    input_vector = [spend] + category_vector

    distances, indices = knn.kneighbors([input_vector])
    best_offer_index = indices[0][0]

    best_offer = flattened_offers[best_offer_index]
    best_price = spend - (spend*0.01*best_offer['cashback_percentage'])
    savings = spend - best_price
    return {
        "payment_method_name": best_offer['payment_method_name'],
        "cashback_percentage": best_offer['cashback_percentage'],
        "best_price": best_price,
        "savings": savings
    }


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', offer=None)


@app.route('/cashback', methods=['POST'])
def cashback():
    data = request.get_json()
    spend = float(data['spend'])
    category = data['category']
    if spend <= 500:
        return jsonify({"offer": "no"})
    best_offer = suggest_max_cashback(spend, category)
    return jsonify(best_offer)


if __name__ == '__main__':
    app.run(debug=True)
