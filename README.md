# IB Test API

This project provides a REST API to interact with Interactive Brokers (IB) Gateway using FastAPI and Docker.

## Prerequisites
- Docker and Docker Compose installed
- IB username and password

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ib-test.git
   cd ib-test
   ```

2. **Configure environment variables**:
   - Copy `.env.example` to  `.env` file in the root directory.
    ```bash
    cp .env.example .env
    ```
   - Replace `your_ib_username` and `your_ib_password` with your IB credentials.

3. **Build and run the application**:
   ```bash
   docker-compose up --build -d
   ```

## Running the API
- The FastAPI server will be available at `http://localhost:8000`.
- Use `curl` or Postman to test the API.

## API Endpoints
- **GET /account**
  - Description: Fetch account summary from IB Gateway.
  - Example request using `curl`:
    ```bash
    curl http://localhost:8000/account
    ```
  - Example response:
    ```json
    {
      "account_id": "DU123456",
      "summary": [
        {"tag": "TotalCashValue", "value": "10000.00", "currency": "USD"},
        {"tag": "NetLiquidation", "value": "15000.00", "currency": "USD"}
      ]
    }
    ```
  - Or error response:
    ```json
    {"error": "IB Gateway not connected"}
    ```

## Troubleshooting
- Check logs:
  ```bash
  docker logs ibc
  docker logs fastapi
  ```
  
- Stop:
  ```bash
  docker-compose down
  ```
