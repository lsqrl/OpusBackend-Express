import requests
import pricer  # Assuming pricer.optionDelta is defined in a file called pricer.py

def get_option_data():
    """
    Fetch option data from the API and extract necessary fields for pricing.
    
    Returns:
    dict: Dictionary containing the extracted fields.
    """
    url = 'http://localhost:5000/getClass/FXOption'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Assuming the API returns a JSON with the necessary fields
        data = response.json()
        
        # Extracting fields (example fields based on assumptions)
        option_data = {
            'strike': data.get('strike'),
            'expiry': data.get('expiry'),
            'notional': data.get('notional'),
            'option_type': data.get('option_type')  # 'call' or 'put'
        }
        
        return option_data
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")

def calculate_option_delta(volatility, rate, spot):
    """
    Calculate the delta of an option by fetching data from the API and using the pricer.optionDelta function.
    
    Parameters:
    volatility (float): Volatility of the underlying asset (annualized).
    rate (float): Risk-free interest rate (annualized).
    spot (float): Current spot price of the underlying asset.
    
    Returns:
    float: Delta of the option.
    """
    # Step 1: Get option data from the API
    option_data = get_option_data()
    
    # Step 2: Extract the necessary fields
    strike = option_data['strike']
    expiry = option_data['expiry']
    notional = option_data['notional']
    option_type = option_data['option_type']
    
    # Step 3: Calculate delta using pricer.optionDelta
    delta = pricer.optionDelta(strike, expiry, rate, volatility, notional, spot, option_type)
    
    # Step 4: Return the delta
    return delta

# Example usage
volatility = 0.2  # User input or external data
rate = 0.05  # User input or external data
spot = 105  # User input or external data

try:
    delta = calculate_option_delta(volatility, rate, spot)
    print(f"Calculated delta: {delta}")
except Exception as e:
    print(f"An error occurred: {e}")
