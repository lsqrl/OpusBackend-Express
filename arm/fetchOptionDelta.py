# fetchOptionDelta.py

import psycopg2
from optionDelta import calculate_delta

def fetch_option_data(option_id, connection):
    cursor = connection.cursor()
    query = "SELECT strike_price, underlying_price, time_to_maturity, volatility, interest_rate FROM options WHERE id = %s"
    cursor.execute(query, (option_id,))
    option_data = cursor.fetchone()
    cursor.close()
    
    if option_data:
        strike_price, underlying_price, time_to_maturity, volatility, interest_rate = option_data
        delta = calculate_delta(strike_price, underlying_price, time_to_maturity, volatility, interest_rate)
        return delta
    else:
        raise ValueError("Option ID not found")

# Example usage:
# connection = psycopg2.connect(database="your_db", user="your_user", password="your_password", host="your_host", port="your_port")
# delta = fetch_option_data(1, connection)
# print(delta)
