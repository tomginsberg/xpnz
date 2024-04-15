// import axios
import axios from "axios";

const endpoint = "http://titanium:3000/api/";

export const XPNZService = {
  getTransactions(workspaceId) {
    // get from endpoint /transactions with key workspaceId
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
    return axios.get(endpoint + "transactions", {
      params: {
        workspaceId: workspaceId
      }
    }).then(response => {
      return response.data;
    });
  },
  getActiveMembers(workspaceId) {
    // get from endpoint /members with key workspaceId
    // [flat list of names (string)]
    return axios.get(endpoint + "activeMembers", {
      params: {
        workspaceId: workspaceId
      }
    }).then(response => {
      return response.data;
    });
  },
  getAllMembers(workspaceId) {
    return axios.get(endpoint + "allMembers", {
      params: {
        workspaceId: workspaceId
      }
    }).then(response => {
      return response.data;
    });
  },
  getBalances(workspaceId) {
    // get from endpoint /balances with key workspaceId
    // {
    //   memberName: balance (int or float)
    // }
    return axios.get(endpoint + "balances", {
      params: {
        workspaceId: workspaceId
      }
    }).then(response => {
      return response.data;
    });
  },
  getCategories(workspaceId) {
    // get from endpoint /categories with key workspaceId
    return axios.get(endpoint + "categories", {
      params: {
        workspaceId: workspaceId
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
  addTransaction(workspaceId, transaction) {
    // post to endpoint /transactions with key workspaceId
    // transaction is the same as the response from getTransactions
    // but without the id field
    return axios.post(endpoint + "saveTransaction", {
      workspaceId: workspaceId,
      transaction: transaction
    }).then(response => {
      return response.data;
    });
  },
  addMember(workspaceId, member) {
    // post to endpoint /members with key workspaceId
    return axios.post(endpoint + "addMembers", {
      workspaceId: workspaceId,
      member: member
    }).then(response => {
      return response.data;
    });
  },
  archiveMember(workspaceId, member) {
    // post to endpoint /archiveMember with key workspaceId
    return axios.post(endpoint + "archiveMember", {
      workspaceId: workspaceId,
      member: member
    }).then(response => {
      return response.data;
    });
  },
  settleDebt(workspaceId, fromMember, toMember, amount) {
    // post to endpoint /settleDebt with key workspaceId
    return axios.post(endpoint + "settleDebt", {
      workspaceId: workspaceId,
      fromMember: fromMember,
      toMember: toMember,
      amount: amount
    }).then(response => {
      return response.data;
    });
  }
};