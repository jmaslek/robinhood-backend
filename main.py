import json
from pathlib import Path
import os
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import robin_stocks.robinhood as r
from loguru import logger

import utils

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Application is starting up")
    try:
        _ = r.login(os.getenv("RH_EMAIL"), os.getenv("RH_PASS"))
        logger.info("LOGGED IN")
    except Exception as e:
        logger.error(f"LOGIN ERROR: {e}")
    yield
    r.logout()
    logger.info("LOGGED OUT")


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost",
    "http://localhost:1420",
    "http://localhost:5050",
    "https://pro.openbb.dev",
    "https://pro.openbb.co",
    "https://excel.openbb.co",
    "https://excel.openbb.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    return JSONResponse(
        content=json.load((Path(__file__).parent.resolve() / "widgets.json").open())
    )


@app.get("/")
async def root():
    return {"Info": "Backend For OpenBB Terminal with Custom Robinhood"}


@app.get("/hello")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/holdings")
async def get_holdings():
    return JSONResponse(content=utils.main_holdings())


@app.get("/l2")
async def get_l2_data(
    symbol: str,
):
    return JSONResponse(content=utils.l2_data(symbol))


@app.get("/l2-chart")
async def get_l2_chart(
    symbol: str,
    min_price: Optional[int | float] = None,
    max_price: Optional[int | float] = None,
):
    return JSONResponse(
        content=json.loads(utils.l2_chart(symbol, min_price, max_price))
    )
