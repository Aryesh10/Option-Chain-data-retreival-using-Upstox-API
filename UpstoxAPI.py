import requests
import pandas as pd
import webbrowser
import time

# Replace these values with your own Upstox API credentials
client_id = '73654a6c-48d4-418c-a328-6d0d5f8c1cc7'
client_secret = 'ik5uauezie'
redirect_uri = 'https://webhook.site/fa266724-120b-457a-8d68-5c5990e318fa'

# Step 1: Get Authorization Code
def get_authorization_code():
    auth_url = (
        f"https://api.upstox.com/v2/login/authorization/dialog?client_id=73654a6c-48d4-418c-a328-6d0d5f8c1cc7&redirect_uri=https://webhook.site/fa266724-120b-457a-8d68-5c5990e318fa"
        #f"client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
    print("Opening authorization URL in your browser...")
    webbrowser.open(auth_url)

    # After authorizing, Upstox will redirect to your redirect_uri with `code` parameter.
    authorization_code = input("Enter the authorization code from the URL: ")
    return authorization_code

# Step 2: Exchange Authorization Code for Access Token
def get_access_token(authorization_code):
    token_url = "https://api.upstox.com/v2/login/authorization/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": authorization_code
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

# Step 3: Fetch Option Chain Data
def fetch_option_chain_data(access_token, instrument_key, expiry_date):
    url = "https://api.upstox.com/v2/option/chain?instrument_key=NSE_INDEX|NIFTY50&expiry_date=2024-11-14"
    payload={}
    headers = {
        "Authorization": f"Bearer {access_token}",  # Replace with your access token
        "Content-Type": "application/json",         # Required for JSON payloads
        "Accept": "application/json"                # Expecting JSON response
    }
    # params = {
    #     "instrument_key": instrument_key,
    #     "expiry_date": expiry_date  # Format YYYY-MM-DD
    # }
    response = requests.get(url, headers=headers,data=payload) #params=params
    response.raise_for_status()
    return response.json()

# Step 4: Process Option Chain Data
def process_option_chain_data(data, side):
    options_data = []
    print("Raw Data for Processing:", data)  # Debug print

    for record in data.get('data', []):
        option = record.get('call_options' if side == "CE" else 'put_options', {})
        strike_price = record.get('strike_price', 0)
        price = option.get('market_data', {}).get('ltp', 0)
        options_data.append({
            "strike_price": strike_price,
            "side": side,
            "ltp": price
        })

    # Convert to DataFrame and find the highest price
    df = pd.DataFrame(options_data)
    print("DataFrame before filtering max price:", df)  # Debug print
    
    if not df.empty:
        max_price = df['ltp'].max()
        df = df[df['ltp'] == max_price]

    return df

# Main Script
if __name__ == "__main__":
    # Step 1: Get Authorization Code
    authorization_code = get_authorization_code()
    time.sleep(2)  # Wait for a moment to enter the authorization code

    # Step 2: Get Access Token
    access_token = get_access_token(authorization_code)
    print("Access Token:", access_token)

    # Step 3: Fetch Option Chain Data
    instrument_key = "NSE_INDEX|NIFTY50"  # Example instrument key for Nifty50
    expiry_date = "2024-11-14"  # Valid expiry date
    side = "CE"  # Replace with "CE" for Call options or "PE" for Put options

    # Fetch data and process it
    option_chain_data = fetch_option_chain_data(access_token, instrument_key, expiry_date)
    print("Fetched Option Chain Data:", option_chain_data)  # Debug the API response
    processed_data = process_option_chain_data(option_chain_data, side)
    print("Processed Data:", processed_data)


