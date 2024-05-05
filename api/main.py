import datetime
import json
import os
from glob import glob

import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette import status

from settle import settle
import argparse

# add a verbose flag to the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()


def vprint(message):
    if args.verbose:
        print(message)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allows specified origins (you can use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# don't settle debts less than this amount
CUTOFF = 0.1
expense_categories = {
    "🛒 Groceries",
    "🍽️ Food",
    "💡 Utilities",
    "🏡 Household",
    "🏠 Rent",
    "🛠️ Maintenance",
    "🛡️ Insurance",
    "🏥 Health",
    "🎬 Entertainment",
    "👗 Clothing",
    "📚 Subscriptions",
    "💸 Transfer",
    "📶 Internet",
    "🚿 Water",
    "🔥 Gas",
    "🚡 Transportation",
    "⚡ Hydro",
    "❓Misc"
}


def exchange_rates(currencies: tuple[str] = ('USD', 'EUR')):
    r = requests.get('https://open.er-api.com/v6/latest/CAD').json()
    return {c: 1 / r['rates'][c] for c in currencies}


class TransactionFor(BaseModel):
    split_weights: list[float]
    members: list[str]


class TransactionBy(BaseModel):
    members: list[str]
    split_values: list[float]
    total: float


class Recurring(BaseModel):
    frequency: str
    end_date: datetime.date


class Transaction(BaseModel):
    ledger: str
    name: str
    category: str
    by: TransactionBy
    to: TransactionFor
    expense_type: str
    currency: str
    date: datetime.date
    recurring: Recurring


def get_members(tr):
    names = set()
    for x, y in zip(tr['by'], tr['for']):
        names.update(x['members'] + y['members'])
    return names


def get_categories(tr) -> set[str]:
    return set(tr['category'])


def get_balances(tr, members=None):
    if members is None:
        members = get_members(tr)
    balances = {name: 0 for name in members}
    for by, for_, ex in zip(tr['by'], tr['for'], tr['exchange_rate']):
        for name, amount in zip(by['members'], by['split_values']):
            if name in balances:
                balances[name] += float(amount) * ex
        for name, amount in zip(for_['members'], for_['split_values']):
            if name in balances:
                balances[name] -= float(amount) * ex
    for name in balances:
        if abs(balances[name]) < CUTOFF:
            balances[name] = 0
        else:
            balances[name] = round(balances[name], 2)

    return balances


def get_settlements(tr, members=None):
    balances = get_balances(tr, members)
    s = settle(balances)
    return [(a, b, x) for a, b, c in s if abs(x := round(c, 2)) >= CUTOFF]


balances: dict[str, dict[str, float]] = {}
ledgers: dict[str, pd.DataFrame] = {}
categories: dict[str, set[str]] = {}
members: dict[str, set[str]] = {}
settlements: dict[str, list[tuple[str, str, float]]] = {}
for file in glob('ledgers/*.json'):
    df = pd.read_json(file)
    # convert date col to tz aware datetime with default EST
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    ledgers[ledger_id := os.path.basename(file).removesuffix('.json')] = (df
                                                                          .sort_values('date', ascending=False))
    ledgers[ledger_id].reset_index(drop=True, inplace=True)
    ledgers[ledger_id]['id'] = ledgers[ledger_id].index
    # round converted_total to 2 decimal places
    ledgers[ledger_id]['converted_total'] = ledgers[ledger_id]['converted_total'].apply(lambda x: round(x, 2))
    cats = get_categories(ledgers[ledger_id])
    cats.discard('')
    cats.union(expense_categories)
    categories[ledger_id] = cats
    members[ledger_id] = set(json.load(open(f'members/{ledger_id}.json')))
    balances[ledger_id] = get_balances(ledgers[ledger_id], members[ledger_id])
    settlements[ledger_id] = get_settlements(ledgers[ledger_id], members[ledger_id])


def check_ledger(ledger: str):
    if ledger not in ledgers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ledger {ledger} not found")


@app.get("/ledger/get/")
def get_transactions(ledger: str) -> list[dict]:
    check_ledger(ledger)
    return ledgers[ledger].to_dict(orient='records')


class TransactionID(BaseModel):
    ledger: str
    transaction_id: int


@app.get("/transaction/get/")
def get_transaction(ledger: str, transaction_id: int) -> list[dict]:
    check_ledger(ledger)
    ledger = ledgers[ledger]
    return [ledger.iloc[transaction_id].to_dict()]


@app.get("/settlements/get/")
def read_settlements(ledger: str) -> list[tuple[str, str, float]]:
    check_ledger(ledger)
    return settlements[ledger]


@app.get("/members/get/")
def read_members(ledger: str) -> set[str]:
    check_ledger(ledger)
    return members[ledger]


@app.get("/categories/get/")
def read_categories(ledger: str) -> set[str]:
    check_ledger(ledger)
    tr = ledgers[ledger]
    cats = get_categories(tr) | expense_categories
    cats.discard('')
    return cats


@app.get("/balances/get/")
def read_balances(ledger: str):
    print(f'Getting balances for {ledger}')
    check_ledger(ledger)
    return balances[ledger]


def parse_float(x):
    try:
        return float(x)
    except:
        return x


@app.post("/transaction/edit/")
async def edit_transaction(transaction: Request):
    transaction = await transaction.json()
    vprint(f'{transaction=}')
    id_ = transaction['id']
    ledger_name = transaction['ledger']
    del transaction['id']
    del transaction['ledger']
    # rename to -> for
    transaction['for'] = transaction['to']
    del transaction['to']
    check_ledger(ledger_name)

    is_income = transaction['expense_type'].lower() == 'income'
    vprint(f'{is_income=}')
    income_multiplier = -1 if is_income else 1
    vprint(f'{income_multiplier=}')

    if transaction['category'] not in categories[ledger_name]:
        categories[ledger_name].add(transaction['category'])

    # truncate split_values and split_weights to the length of members
    transaction['for']['split_weights'] = transaction['for']['split_weights'][:len(transaction['for']['members'])]
    transaction['by']['split_values'] = [
        abs(parse_float(x)) * income_multiplier for x in transaction['by']['split_values'][:len(transaction['by']['members'])]]

    # remove any none values from split_values and split_weights and the corresponding members
    valid_ids = [i for i, x in enumerate(transaction['by']['split_values']) if x is not None]
    transaction['by']['members'] = [transaction['by']['members'][i] for i in valid_ids]
    transaction['by']['split_values'] = [income_multiplier * abs(transaction['by']['split_values'][i]) for i in
                                         valid_ids]

    valid_ids = [i for i, x in enumerate(transaction['for']['split_weights']) if x is not None and x > 0]
    transaction['for']['split_weights'] = [transaction['for']['split_weights'][i] for i in valid_ids]
    transaction['for']['members'] = [transaction['for']['members'][i] for i in valid_ids]

    # correct any possible inconsistency errors from the frontend
    total = sum(float(x) for x in transaction['by']['split_values'] if x is not None)
    if transaction['expense_type'] == 'income':
        total = -abs(total)
    transaction['by']['total'] = total

    # compute total weight, and for.split_values
    total_weight = sum(transaction['for']['split_weights'])
    transaction['for']['split_values'] = [transaction['by']['total'] * w / total_weight for w in
                                          transaction['for']['split_weights']]
    transaction['for']['total'] = total_weight

    if (curr := transaction['currency']) != 'CAD':
        # use old exchange rate if provided
        if 'exchange_rate' not in transaction:
            transaction['exchange_rate'] = exchange_rates()[curr]
        transaction['converted_total'] = round(transaction['by']['total'] * transaction['exchange_rate'], 2)
    else:
        transaction['exchange_rate'] = 1
        transaction['converted_total'] = transaction['by']['total']

    if 'recurring' not in transaction:
        transaction['recurring'] = False

    transaction['date'] = pd.to_datetime(transaction['date'])
    print(transaction['date'])
    vprint(f'Final transaction:\n {transaction}')

    ledger = ledgers[ledger_name]
    if id_ == 'new':
        # append new transaction to the ledger
        if len(ledger) == 0:
            ledger = pd.DataFrame([transaction])
        else:
            ledger = pd.concat([ledger, pd.DataFrame([transaction])])
    else:
        # update existing transaction
        ledger.iloc[int(id_)] = transaction

    # sort ledger by date
    ledger = ledger.sort_values('date', ascending=False)
    ledger.reset_index(drop=True, inplace=True)
    ledger['id'] = ledger.index
    ledgers[ledger_name] = ledger
    balances[ledger_name] = get_balances(ledger, members[ledger_name])
    settlements[ledger_name] = get_settlements(ledger, members[ledger_name])
    ledger.to_json(f'ledgers/{ledger_name}.json', orient='records')
    return status.HTTP_200_OK


@app.post("/settle/")
async def settle_debt(data: Request):
    data = await data.json()
    ledger_name = data['ledger']
    check_ledger(ledger_name)
    ledger = ledgers[ledger_name]
    amount = abs(float(data['amount']))
    print(f'Settling {amount} from {data["from"]} to {data["to"]}')
    transaction = {
        'by': {
            'members': [data['from']],
            'split_values': [amount],
            'total': amount
        },
        'for': {
            'members': [data['to']],
            'split_weights': [1],
            'split_values': [amount],
            'total': 1
        },
        'name': f'{data["from"]} → {data["to"]}',
        'category': '💸 Transfer',
        'currency': 'CAD',
        'date': pd.to_datetime(datetime.datetime.now(), utc=True),
        'recurring': False,
        'expense_type': 'transfer',
        'converted_total': amount,
        'exchange_rate': 1
    }
    ledger = pd.concat([ledger, pd.DataFrame([transaction])])
    ledger = ledger.sort_values('date', ascending=False)
    ledger.reset_index(drop=True, inplace=True)
    ledger['id'] = ledger.index
    ledgers[ledger_name] = ledger
    balances[ledger_name] = get_balances(ledger, members[ledger_name])
    settlements[ledger_name] = get_settlements(ledger, members[ledger_name])
    ledger.to_json(f'ledgers/{ledger_name}.json', orient='records')
    return status.HTTP_200_OK


class DeleteTransaction(BaseModel):
    transaction_id: int
    ledger: str


@app.delete("/transaction/delete/")
def delete_transaction(ledger: str, transaction_id: int):
    ledger_name = ledger
    transaction_id = transaction_id
    print(f'Deleting transaction {transaction_id} from {ledger_name}')
    check_ledger(ledger_name)
    ledger = ledgers[ledger_name]
    print(f'Deleting transaction {transaction_id} ({ledger.iloc[transaction_id]}) from {ledger_name}')
    # drop index transaction_id from ledger
    updated_ledger = ledger.drop(transaction_id)
    updated_ledger.reset_index(drop=True, inplace=True)
    updated_ledger['id'] = updated_ledger.index
    updated_ledger.to_json(f'ledgers/{ledger_name}.json', orient='records')
    ledgers[ledger_name] = updated_ledger
    return status.HTTP_200_OK


@app.post("/members/delete/")
def delete_member(ledger: str, member: str):
    check_ledger(ledger)
    balances = get_balances(ledgers[ledger], get_members(ledgers[ledger]))
    if balances.get(member, 0) != 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Member {member} has non-zero balance")
    if member not in members[ledger]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member {member} not found")
    members[ledger].discard(member)
    json.dump(list(members[ledger]), open(f'members/{ledger}.json', 'w'))
    return status.HTTP_200_OK


class Member(BaseModel):
    member: str
    ledger: str


@app.post("/members/add/")
def add_member(member: Member):
    ledger = member.ledger
    member = member.member

    if ledger not in ledgers:
        # initialize ledger
        ledgers[ledger] = pd.DataFrame(columns=['by', 'currency', 'for', 'name',
                                                'category', 'date', 'exchange_rate',
                                                'converted_total', 'expense_type', 'id'])
        ledgers[ledger].to_json(f'ledgers/{ledger}.json')
        members[ledger] = set()
        categories[ledger] = expense_categories
        settlements[ledger] = []
        balances[ledger] = {}

    if member in members[ledger]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Member already exists")

    members[ledger].add(member)
    balances[ledger][member] = 0
    json.dump(list(members[ledger]), open(f'members/{ledger}.json', 'w'))
    return status.HTTP_201_CREATED


@app.delete("/ledger/delete/")
def delete_ledger(ledger: str):
    check_ledger(ledger)
    os.remove(f'ledgers/{ledger}.json')
    os.remove(f'members/{ledger}.json')
    del ledgers[ledger]
    del members[ledger]
    del categories[ledger]
    del settlements[ledger]
    del balances[ledger]
    return status.HTTP_200_OK


@app.get("/exchange_rate/")
def get_exchange_rates():
    return exchange_rates()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload
