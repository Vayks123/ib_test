import os
from fastapi import FastAPI
from ib_insync import IB
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IB_PORT = int(os.getenv("IB_PORT", 4004))
IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", 1))
IB_HOST = os.getenv("IB_HOST", "ibc")

@app.on_event("startup")
async def startup_event():
    """Connect to IB Gateway on startup."""
    app.ib = IB()
    attempt = 1
    while True:
        try:
            await app.ib.connectAsync(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)
            logger.info("Connected to IB Gateway")
            return
        except Exception as e:
            logger.warning(f"Connection attempt {attempt} failed: {e}")
            attempt+=1
            logger.error(f"Failed to connect to IB Gateway after retries: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from IB Gateway on shutdown."""
    if hasattr(app, "ib") and app.ib.isConnected():
        app.ib.disconnect()
        logger.info("Disconnected from IB Gateway")

@app.get("/account")
async def get_account_summary():
    """Fetch account summary from IB Gateway."""
    try:
        if not app.ib.isConnected():
            raise Exception("IB Gateway not connected")
        account_summary = await app.ib.accountSummaryAsync()
        result = {
            "account_id": app.ib.wrapper.accounts[0] if app.ib.wrapper.accounts else "N/A",
            "summary": [
                {"tag": item.tag, "value": item.value, "currency": item.currency}
                for item in account_summary
            ]
        }
        return result
    except Exception as e:
        logger.error(f"Error fetching account summary: {e}")
        return {"error": str(e)}