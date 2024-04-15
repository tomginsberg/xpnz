// import axios
import axios from "axios";

const endpoint = "http://titanium:3000/api/";

export const XPNZService = {
  getTransactions(ledgerId) {
    // get from endpoint /transactions with key ledgerId
    // {
    //   price: 66.6 (int or float),
    //   category: "expense category" (string),
    //   currency: "CAD" or "USD" or "EUR" (string),
    //   date: 1546318800 (unix timestamp),
    //   name: "name of expense" (string),
    //   id: unique id (int or string),
    //   by: [...] names of members who paid for the transaction (flat list of strings, no ids member names must be unique),
    //   for: [...] names of members who participated in the transaction (flat list of strings, no ids member names must be unique)
    //   weights: [...] weights of each member who participated in the transaction (flat list of numbers),
    //   normalizedWeights: [...] weights converted to amounts (flat list of numbers) == weights / sum(weights) * price,
    //   contributions: [...] amounts paid by each member who paid for the transaction (flat list of numbers),
    //   expenseType: "Expense" or "Transfer" or "Income" (string),
    //   recurring (optional): {
    //     frequency: "daily" or "weekly" or "monthly" or "yearly" (string),
    //     interval: 1 (int),
    //     endDate: 1546318800 (unix timestamp)
    //   }
    // }
    // results should be sorted by date
    return axios.get(endpoint + "transactions", {
      params: {
        "ledger_id": ledgerId
      }
    }).then(response => {
      return response.data;
    });
  },
  getActiveMembers(ledgerId) {
    // get from endpoint /members with key ledgerId
    // [flat list of names (string)]
    return axios.get(endpoint + "members", {
      params: {
        "ledger_id": ledgerId,
        "active": true
      }
    }).then(response => {
      return response.data;
    });
  },
  getAllMembers(ledgerId) {
    return axios.get(endpoint + "members", {
      params: {
        "ledger_id": ledgerId
      }
    }).then(response => {
      return response.data;
    });
  },
  getBalances(ledgerId) {
    // get from endpoint /balances with key ledgerId
    // {
    //   memberName: balance (int or float)
    // }
    return axios.get(endpoint + "members", {
      params: {
        "ledger_id": ledgerId,
        "balances": true
      }
    }).then(response => {
      return response.data;
    });
  },
  getCategories(ledgerId) {
    // get from endpoint /categories with key ledgerId
    return axios.get(endpoint + "categories", {
      params: {
        "ledger_id": ledgerId
      }
    }).then(response => {
      return response.data;
    });
  },
  getWorkspaces() {
    // get from endpoint /workspaces
    return axios.get(endpoint + "workspaces").then(response => {
      return response.data;
    });
  },
  addTransaction(ledgerId, transaction) {
    // post to endpoint /transactions with key ledgerId
    // transaction is the same as the response from getTransactions
    // but without the id field
    return axios.post(endpoint + "transactions", {
      "ledger_id": ledgerId,
      transaction: transaction
    }).then(response => {
      return response.data;
    });
  },
  deleteTransaction(ledgerId, transactionId) {
    // post to endpoint /transactions with key ledgerId
    return axios.post(endpoint + "transactions", {
      "ledger_id": ledgerId,
      transactionId: transactionId
    }).then(response => {
      return response.data;
    });
  },
  addMember(ledgerId, member) {
    // post to endpoint /members with key ledgerId
    return axios.post(endpoint + "members", {
      "ledger_id": ledgerId,
      member: member,
      action: "add"
    }).then(response => {
      return response.data;
    });
  },
  archiveMember(ledgerId, member) {
    // post to endpoint /members with key ledgerId
    return axios.post(endpoint + "members", {
      "ledger_id": ledgerId,
      member: member,
      action: "archive"
    }).then(response => {
      return response.data;
    });
  },
  settleDebt(ledgerId, fromMember, toMember, amount) {
    // post to endpoint /settleDebt with key ledgerId
    return axios.post(endpoint + "settle", {
      "ledger_id": ledgerId,
      fromMember: fromMember,
      toMember: toMember,
      amount: amount
    }).then(response => {
      return response.data;
    });
  }
};