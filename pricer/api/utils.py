import requests
from pricer.analytics.optionDelta import option_delta
from pricer.analytics.optionGamma import option_gamma
from pricer.analytics.optionVega import option_vega
from pricer.analytics.optionTheta import option_theta
from pricer.analytics.optionPrice import option_price
from datetime import datetime, timezone

def get_option_data():
    """
    Fetch option data from the API and extract necessary fields for pricing.
    
    Returns:
    list: List of dictionaries, each containing the extracted fields for an option.
    """
    url = 'http://localhost:5000/getClass/FXOption'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Assuming the API returns a JSON array with the necessary fields for each option
        data = response.json()
        print(data)
        # Extracting fields for each option in the response
        option_list = []
        for option in data:
            strike = option.get('strike')
            expiry_time = option.get('expiry_time')  # This is a string in the format "YYYY-MM-DDTHH:MM:SS"
            notional = option.get('notional')
            option_type = option.get('type')  # 'CALL' or 'PUT'
            
            # Validate if all the required fields are present and not None
            if None in (strike, expiry_time, notional, option_type):
                continue  # Skip invalid option data
            
            # Convert expiry_time to a datetime object
            expiry_datetime = datetime.strptime(expiry_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
            
            # Calculate the time to expiry in years
            current_time = datetime.now(timezone.utc)
            time_to_expiry = (expiry_datetime - current_time).days / 365.0
            
            # Skip expired options
            if time_to_expiry < 0:
                continue
            
            option_data = {
                'strike': strike,
                'expiry': time_to_expiry,  # Time to expiry in years
                'notional': notional,
                'option_type': option_type  # 'CALL' or 'PUT'
            }
            option_list.append(option_data)
        
        return option_list
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")

def calculate_option_greeks(volatility, rate, spot):
    """
    Calculate the sum of greeks of all options by fetching data from the API and using the option_delta function.
    
    Parameters:
    volatility (float): Volatility of the underlying asset (annualized).
    rate (float): Risk-free interest rate (annualized).
    spot (float): Current spot price of the underlying asset.
    
    Returns:
    float: Sum of deltas of all options.
    """
    # Step 1: Get option data from the API
    options = get_option_data()
    
    # Step 2: Initialize the total delta sum
    total_delta = 0.0
    total_gamma = 0.0
    total_theta = 0.0
    total_vega = 0.0
    
    # Step 3: Loop through each option and calculate the delta
    for option_data in options:
        strike = option_data['strike']
        expiry = option_data['expiry']  # Now this is a float representing time to expiry in years
        notional = option_data['notional']
        option_type = option_data['option_type']
        
        # Calculate delta using option_delta function from optionDelta.py
        delta = option_delta(strike, expiry, rate, volatility, notional, spot, option_type)
        gamma = option_gamma(strike, expiry, rate, volatility, notional, spot, option_type)
        theta = option_theta(strike, expiry, rate, volatility, notional, spot, option_type)
        vega = option_vega(strike, expiry, rate, volatility, notional, spot, option_type)
        
        # Add the delta to the total
        total_delta += delta
        total_gamma += gamma
        total_theta += theta
        total_vega += vega
    
    # Step 4: Return the total sum of deltas
    return total_delta, total_gamma, total_theta, total_vega


def calculate_option_price(volatility, rate, spot):
    """
    Calculate the sum of option prices by fetching data from the API and using the option_price function.
    
    Parameters:
    volatility (float): Volatility of the underlying asset (annualized).
    rate (float): Risk-free interest rate (annualized).
    spot (float): Current spot price of the underlying asset.
    
    Returns:
    float: Sum of prices of all options.
    """
    # Step 1: Get option data from the API
    options = get_option_data()
    
    # Step 2: Initialize the total price sum
    total_price = 0.0
    
    # Step 3: Loop through each option and calculate the price
    for option_data in options:
        strike = option_data['strike']
        expiry = option_data['expiry']  # Now this is a float representing time to expiry in years
        notional = option_data['notional']
        option_type = option_data['option_type']
        
        # Calculate price using option_price function from optionPrice.py
        price = option_price(strike, expiry, rate, volatility, notional, spot, option_type)
        
        # Add the price to the total
        total_price += price
    
    # Step 4: Return the total sum of prices
    return total_price
