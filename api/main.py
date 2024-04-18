import datetime
import json
import os
from glob import glob

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status

from settle import settle

app = FastAPI()

expense_categories = {
    "Rent",
    "Utilities",
    "Groceries",
    "Dining",
    "Transportation",
    "Maintenance",
    "Insurance",
    "Health",
    "Education",
    "Entertainment",
    "Clothing",
    "Travel",
    "Gifts",
    "Household",
    "Childcare",
    "Subscriptions",
    "Transfer"
}


class TransactionFor(BaseModel):
    members: list[str]
    split_values: list[float]
    split_weights: list[float]
    total: float


class TransactionBy(BaseModel):
    members: list[str]
    split_values: list[float]
    total: float


class Transaction(BaseModel):
    paid_by: TransactionBy
    currency: str
    paid_for: TransactionFor
    name: str
    category: str
    date: datetime.datetime
    exchange_rate: float
    converted_total: float
    expense_type: str


def get_members(tr):
    names = set()
    for x, y in zip(tr['by'], tr['for']):
        names.update(x['members'] + y['members'])
    return names


def get_categories(tr) -> set[str]:
    return set(tr['category'])


ledgers: dict[str, pd.DataFrame] = {}
categories: dict[str, set[str]] = {}
members: dict[str, set[str]] = {}
for file in glob('ledgers/*.json'):
    ledgers[ledger_id := os.path.basename(file).removesuffix('.json')] = pd.read_json(file).sort_values('date',
                                                                                                        ascending=False)
    cats = get_categories(ledgers[ledger_id])
    cats.remove('')
    cats.union(expense_categories)
    categories[ledger_id] = cats
    members[ledger_id] = set(json.load(open(f'members/{ledger_id}.json')))


def get_balances(tr, members=None):
    if members is None:
        members = get_members(tr)
    balances = {name: 0 for name in members}
    for by, for_, ex in zip(tr['by'], tr['for'], tr['exchange_rate']):
        for name, amount in zip(by['members'], by['split_values']):
            balances[name] += float(amount) * ex
        for name, amount in zip(for_['members'], for_['split_values']):
            balances[name] -= float(amount) * ex
    return balances


def get_settlements(tr, members=None):
    balances = get_balances(tr, members)
    return settle(balances)


def check_ledger(ledger: str):
    if ledger not in ledgers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ledger not found")


@app.get("/transactions/get/")
def read_transactions(ledger: str):
    check_ledger(ledger)
    return ledgers[ledger].to_dict(orient='records')


@app.get("/settlements/")
def read_settlements(ledger: str):
    check_ledger(ledger)
    tr = ledgers[ledger]
    return get_settlements(tr)


@app.get("/members/get/")
def read_members(ledger: str):
    check_ledger(ledger)
    return members[ledger]


@app.get("/categories/")
def read_categories(ledger: str):
    check_ledger(ledger)
    tr = ledgers[ledger]
    cats = get_categories(tr) | expense_categories
    cats.remove('')
    return cats


@app.get("/balances/")
def read_balances(ledger: str):
    check_ledger(ledger)
    tr = ledgers[ledger]
    return get_balances(tr, members[ledger])


@app.post("/transactions/add/")
def add_transaction(ledger: str, transaction: Transaction):
    check_ledger(ledger)
    ledger_df = ledgers[ledger]
    # validate transaction
    for col in ledger_df.columns:
        if col not in transaction:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing column {col}")

    updated_ledger = (pd.concat([ledger_df, pd.DataFrame([transaction.dict()])])
                      .sort_values('date', ascending=False))
    ledgers[ledger] = updated_ledger
    categories[ledger].add(transaction.category)

    updated_ledger.to_json(f'{ledger}.json')
    return status.HTTP_201_CREATED


@app.post("/transactions/delete/")
def delete_transaction(ledger: str, transaction_id: int):
    check_ledger(ledger)
    ledger = ledgers[ledger]
    updated_ledger = ledger.drop(transaction_id)
    updated_ledger.to_json(f'{ledger}.json')
    return status.HTTP_200_OK


@app.post("/members/delete/")
def delete_member(ledger: str, member: str):
    check_ledger(ledger)
    balances = get_balances(ledgers[ledger], get_members(ledgers[ledger]))
    if balances.get(member, 0) != 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Member {member} has non-zero balance")
    if member not in members[ledger]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member {member} not found")
    members[ledger].remove(member)
    json.dump(list(members[ledger]), open(f'members/{ledger}.json', 'w'))
    return status.HTTP_200_OK


@app.post("/members/add/")
def add_member(ledger: str, member: str):
    check_ledger(ledger)
    if member in members[ledger]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Member already exists")
    members[ledger].add(member)
    json.dump(list(members[ledger]), open(f'members/{ledger}.json', 'w'))
    return status.HTTP_200_OK


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload
