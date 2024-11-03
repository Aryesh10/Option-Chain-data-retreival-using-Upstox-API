

# Upstox API Interaction Script

This Python script interacts with the Upstox API to perform several key functions, including user authentication, retrieving option chain data, and processing this data to analyze specific options based on criteria such as side (call or put) and price. The script is designed to support options trading data analysis with minimal setup.

## Prerequisites

To use this script, ensure that you:
- Have registered as a developer on Upstox and obtained API credentials: `client_id` and `client_secret`.
- Set up a **redirect URI** to receive the authorization response.

### Dependencies
The script uses the following libraries:
- `requests`: Handles HTTP requests to the Upstox API.
- `pandas`: Processes and analyzes option chain data.
- `webbrowser`: Opens the authorization URL in the default web browser.
- `time`: Manages delays, if necessary, to synchronize with API responses.

## Code Structure and Logic

1. **Authorization URL Generation**:
   - `get_authorization_code()`: Constructs the authorization URL and opens it in the browser, allowing the user to log in and authorize access. Afterward, the authorization code can be retrieved from the redirect URL and input manually.

2. **Access Token Retrieval**:
   - `get_access_token(authorization_code)`: Exchanges the authorization code for an access token by making a POST request to Upstox’s token endpoint. This token is essential for accessing Upstox’s protected API endpoints.

3. **Option Chain Data Retrieval**:
   - `fetch_option_chain_data(access_token, instrument_key, expiry_date)`: Retrieves options data for a specified instrument and expiry date. This function makes a GET request to Upstox’s option chain API, using the access token for authorization. 

4. **Data Processing and Analysis**:
   - `process_option_chain_data(data, side)`: Analyzes the option chain data by filtering it based on the `side` parameter (either "CE" for call options or "PE" for put options). It extracts key details like strike prices and last traded prices (LTP) and returns this information in a structured format using `pandas` DataFrames.

### Example Workflow

1. **Authentication**:
   - Run `get_authorization_code()` to open the Upstox login page in the browser.
   - After authorization, enter the authorization code when prompted.

2. **Data Retrieval**:
   - Pass the access token obtained to `fetch_option_chain_data()`, specifying the instrument and expiry date for the options chain.

3. **Data Processing**:
   - Use `process_option_chain_data()` to filter and organize the options data, ready for further analysis or strategy implementation.

## Security Considerations

- **Credentials and Tokens**: Secure your API credentials (`client_id`, `client_secret`) and the access token. Avoid storing sensitive data directly in the code or sharing it in public repositories.
- **Data Privacy**: Limit access to the data retrieved from Upstox’s API, especially if it contains sensitive market information.

## AI Tools Used
