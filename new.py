import random
from datetime import datetime, timedelta

# Initialize the payment methods
payment_methods = [
    {
        "payment_method_id": 1,
        "payment_method_name": "SBI Credit Card",
        "description": "Issued by State Bank of India"
    },
    {
        "payment_method_id": 2,
        "payment_method_name": "Amazon Pay ICICI Credit Card",
        "description": "Issued by ICICI Bank"
    },
    {
        "payment_method_id": 3,
        "payment_method_name": "HDFC Debit Card",
        "description": "Issued by HDFC Bank"
    }
]

# Define eligible categories
categories = ["Electronics", "Home Appliances", "Fashion", "Groceries", "Travel", "Dining"]

# Generate random offers
def generate_random_offers(n):
    offers = []
    for i in range(n):
        payment_method = random.choices(payment_methods, weights=[29, 43, 28], k=1)[0]  # 43% Amazon Pay ICICI Credit Card
        cashback_percentage = random.uniform(2, 10)
        min_spend = random.randint(500, 10000)
        max_cashback = random.randint(500, 3000)
        eligible_categories = random.sample(categories, k=random.randint(1, len(categories)))
        valid_from = datetime.strptime("2024-01-01", "%Y-%m-%d")
        valid_to = valid_from + timedelta(days=random.randint(30, 365))

        offer = {
            "payment_method_id": payment_method['payment_method_id'],
            "payment_method_name": payment_method['payment_method_name'],
            "description": payment_method['description'],
            "offer_id": i + 1,
            "cashback_percentage": round(cashback_percentage, 2),
            "max_cashback": max_cashback,
            "min_spend": min_spend,
            "valid_from": valid_from.strftime("%Y-%m-%d"),
            "valid_to": valid_to.strftime("%Y-%m-%d"),
            "eligible_categories": eligible_categories
        }
        offers.append(offer)
    return offers

# Generate 300 random offers
random_offers = generate_random_offers(300)
# Print a few entries to verify
print(random_offers[0]);