
# Upstox API Interaction Script

This Python script facilitates interaction with the Upstox API by enabling user authentication, retrieving options chain data, and processing this data for options trading analysis. Below is a breakdown of the functions, including explanations of their operations, assumptions, and sample API responses with the expected outputs.

## Prerequisites

To use this script, you need:
- Upstox API credentials (`client_id`, `client_secret`, and `redirect_uri`).
- Basic familiarity with Upstox’s [API documentation](https://upstox.com/developer/api/).

### Dependencies
- `requests` - Handles HTTP requests.
- `pandas` - Structures and analyzes data.
- `webbrowser` - Opens the authorization URL in a browser.
- `time` - Manages timing for API response synchronization.

## Code Structure and Functionality

### 1. `get_authorization_code()`

**Function**: Constructs the OAuth2 authorization URL, opens it in the browser, and prompts the user to enter the authorization code provided in the redirect URL.

- **Assumptions**: Assumes that the `client_id` and `redirect_uri` are correctly set and that the user completes authorization in a timely manner.
  
- **How It Works**: 
  - Builds the authorization URL using the `client_id` and `redirect_uri`.
  - Opens this URL in the default web browser.
  - After user authorization, the code expects the user to input the `authorization_code` manually.

**Example URL Opened**:
```
https://api.upstox.com/v2/login/authorization/dialog?client_id=73654a6c-48d4-418c-a328-6d0d5f8c1cc7&redirect_uri=https://webhook.site/fa266724-120b-457a-8d68-5c5990e318fa
```

**Example Input Prompt**:
```
Enter the authorization code from the URL:
```

### 2. `get_access_token(authorization_code)`

**Function**: Exchanges the `authorization_code` for an `access_token` to access other Upstox API endpoints.

- **Assumptions**: Assumes that the authorization code is valid and the Upstox token endpoint is accessible.

- **How It Works**:
  - Constructs a POST request with parameters including `client_id`, `client_secret`, `grant_type`, `redirect_uri`, and the provided `authorization_code`.
  - Sends the request to Upstox’s token endpoint to obtain the `access_token`.

**Example Request**:
```python
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code": authorization_code
}
```

**Example API Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Output**: Returns the `access_token` required for authenticated requests.

### 3. `fetch_option_chain_data(access_token, instrument_key, expiry_date)`

**Function**: Retrieves the option chain data for a specified `instrument_key` (such as `NSE_INDEX|NIFTY50`) and `expiry_date`.

- **Assumptions**: Assumes the `access_token` is valid, the instrument key exists, and the expiry date format matches `YYYY-MM-DD`.

- **How It Works**:
  - Constructs the request URL with `instrument_key` and `expiry_date`.
  - Passes the `access_token` in the headers to authorize the request.
  - Retrieves the JSON response containing data for various strike prices and market information for both call and put options.

**Example Request**:
```python
url = f"https://api.upstox.com/v2/option/chain?instrument_key={instrument_key}&expiry_date={expiry_date}"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

**Example API Response**:
```json
{
  "data": [
    {
      "strike_price": 17000,
      "call_options": {
        "market_data": {
          "ltp": 180.50
        }
      },
      "put_options": {
        "market_data": {
          "ltp": 190.75
        }
      }
    },
    {
      "strike_price": 17500,
      "call_options": {
        "market_data": {
          "ltp": 140.10
        }
      },
      "put_options": {
        "market_data": {
          "ltp": 200.25
        }
      }
    }
  ]
}
```

**Output**: Returns raw option chain data in JSON format.

### 4. `process_option_chain_data(data, side)`

**Function**: Processes the option chain data, filtering by `side` (either "CE" for call options or "PE" for put options) and extracting the last traded price (LTP) and strike price.

- **Assumptions**: Assumes `data` is correctly formatted JSON from the Upstox API, and the `side` parameter is valid.

- **How It Works**:
  - Iterates over each record in the `data` array, selecting `call_options` or `put_options` based on the `side` parameter.
  - Extracts `strike_price` and `ltp` (last traded price) and stores them in a list of dictionaries.
  - Converts the list into a `pandas` DataFrame for further analysis, such as identifying the highest price.

**Example Processing**:
```python
# For `side="CE"` (Call Options)
[
    {
        "strike_price": 17000,
        "side": "CE",
        "ltp": 180.50
    },
    {
        "strike_price": 17500,
        "side": "CE",
        "ltp": 140.10
    }
]
```

**Example DataFrame Output**:
| strike_price | side | ltp   |
|--------------|------|-------|
| 17000        | CE   | 180.5 |
| 17500        | CE   | 140.1 |

### Workflow

1. **Authentication**: 
   - Run `get_authorization_code()` and `get_access_token(authorization_code)`.
   
2. **Data Retrieval**:
   - Use `fetch_option_chain_data(access_token, instrument_key, expiry_date)` to retrieve option chain data.

3. **Data Processing**:
   - Process this data using `process_option_chain_data(data, side)` for insights into call or put options by side and strike price.

## Security Considerations

Secure your credentials and token to prevent unauthorized access. Ensure that sensitive data, such as API keys, is not hardcoded in public code.

## AI Tools Used

- Used ChatGPT for refining the code and detecting errors.
- Used ChatGPT to understand the working of Upstox API.
- 
