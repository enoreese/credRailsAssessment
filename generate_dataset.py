import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, date

if __name__ == '__main__':
    fake = Faker()
    # Set random seed for reproducibility
    np.random.seed(42)
    # Generate data
    num_records = 10000

    dates = [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_records)]
    customer_ids = [f'C{random.randint(1000, 9876)}' for _ in range(num_records)]
    product_ids = [f'P{random.randint(1, 100)}' for _ in range(num_records)]
    merchant_ids = [f'M{random.randint(1, 50)}' for _ in range(num_records)]
    countries = np.random.choice(['USA', 'UK', 'Canada', 'Australia'], num_records, p=[0.4, 0.3, 0.2, 0.1])

    # Simulate dependency and pattern between status, country, payment_type, time and amount
    amounts = []
    statuses = []
    payment_types = []
    times = []

    for idx, country in enumerate(countries):
        if np.random.random() < 0.15:  # 15% chance of fraud
            statuses.append('Chargeback')
            if country == 'USA':
                amounts.append(np.random.uniform(600, 1400))
            else:
                amounts.append(np.random.uniform(500, 1400))

            payment_types.append(np.random.choice(['Credit Card', 'Debit Card', 'PayPal'], p=[0.5, 0.35, 0.15]))
            risky_hour = np.random.choice([2, 3, 4, 23, 0, 1])
            now_time = (datetime.combine(date(1, 1, 1), fake.time_object()) + timedelta(hours=int(risky_hour))).time()
            times.append(str(now_time).split('.')[0])

            date_split = str(dates[idx]).split('-')
            if date_split[1] in ['11', '12', '01']:
                date_split[1] = np.random.choice(['24', '25', '26', '28', '02', '01'])
                dates[idx] = '-'.join(date_split)

            times_split = times[idx].split(':')
            if date_split[2] in ['30', '28', '01', '02']:
                times_split[-1] = np.random.choice(['18', '22', '19'])
                times[idx] = ':'.join(times_split)

        elif (np.random.random() > 0.15) and (np.random.random() < 0.20):
            statuses.append('Refunded')
            payment_types.append(np.random.choice(['Credit Card', 'Debit Card', 'PayPal'], p=[0.35, 0.5, 0.15]))
            times.append(str(fake.time()))
            amounts.append(np.random.uniform(50, 1000))
        else:
            statuses.append(np.random.choice(['Completed', 'Pending', 'Cancelled'], p=[0.4, 0.35, 0.25]))
            payment_types.append(np.random.choice(['Credit Card', 'Debit Card', 'PayPal'], p=[0.3, 0.3, 0.4]))
            times.append(str(fake.time()))
            amounts.append(np.random.uniform(50, 1400))

    amounts = np.array(amounts).round(2)

    # simulate missing values
    def sim_missing(lst, prop=0.1):
        indices_to_remove = random.sample(range(len(lst)), int(len(lst) * prop))
        return [x if i not in indices_to_remove else None for i, x in enumerate(lst)]

    countries = sim_missing(countries, prop=0.05)
    payment_types = sim_missing(payment_types, prop=0.1)
    amounts = sim_missing(amounts, prop=0.05)

    # Create DataFrame
    df = pd.DataFrame({
        'Transaction_ID': [f'TX{10000 + i}' for i in range(num_records)],
        'Date': dates,
        'Time': times,
        'Customer_ID': customer_ids,
        'Product_ID': product_ids,
        'Amount': amounts,
        'Payment_Type': payment_types,
        'Country': countries,
        'Merchant_ID': merchant_ids,
        'Status': statuses
    })

    # Save to CSV
    df.to_csv('data/financial_transactions_100k.csv', index=False)
    print("Dataset generated and saved to 'financial_transactions_10k.csv'")
