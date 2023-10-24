# Crypto Market Microservice

This is a Python microservice for fetching cryptocurrency market updates from the Bittrex API. It provides endpoints to retrieve market summaries and individual market summary information.

## Project Structure

The project is structured as follows:

- `app`: Contains the microservice application code.
- `tests`: Contains unit tests for the microservice.
- `config.py`: Configuration file for the microservice.
- `main.py`: The entry point of the microservice.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Docker containerization configuration.
- `README.md`: This documentation file.

## Prerequisites

Before running the microservice, ensure you have the following:

- Python 3.x installed
- Dependencies installed (use `pip install -r requirements.txt`)
- Bittrex API key and secret

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/crypto-market-microservice.git
   cd crypto-market-microservice

2. Install dependencies:

    pip install -r requirements.txt

3. Set up Bittrex API credentials:

    Open config.py and replace "YOUR_API_KEY" and "YOUR_API_SECRET" with your Bittrex API key and secret.

4. Start the microservice:

    python main.py