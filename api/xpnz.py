from typing import Optional

from fastapi import FastAPI, HTTPException
from starlette import status
from pydantic import BaseModel
import pandas as pd
import datetime
from glob import glob

app = FastAPI()

ledgers: dict[str, pd.DataFrame] = {}
for file in glob('*.json'):
    ledgers[file.removesuffix('.json')] = pd.read_json(file)


class Transaction(BaseModel):
    id: int
    price: float
    category: str
    currency: str
    date: datetime.date
    name: str
    by: list[str]
    for_: list[str]
    weights: list[float]
    normalized_weights: list[float]
    contributions: list[float]
    expense_type: str
    recurring: Optional[list[str, datetime.date]] = None


def check_ledger(ledger: str):
    if ledger not in ledgers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ledger not found")


@app.get("/transactions/")
def read_transactions(ledger: str):
    check_ledger(ledger)
    return ledgers[ledger].to_dict(orient='records')


@app.post("/transactions/")
def add_transaction(ledger: str, transaction: Transaction):
    check_ledger(ledger)
    ledger = ledgers[ledger]
    updated_ledger = ledger.append(transaction.dict(), ignore_index=True)
    updated_ledger.to_json(f'{ledger}.json')
    # return success code
    return status.HTTP_201_CREATED


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload
