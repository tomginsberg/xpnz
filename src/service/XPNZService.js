// import axios
import axios from "axios";

const endpoint = "http://orion:8000/";

const expenseNames = [
  "Coffee Break ☕",
  "Pet Supplies 🐾",
  "Book Club 📚",
  "Movie Night 🎬",
  "Travel Fund ✈️",
  "Art Supplies 🎨",
  "Game Night 🎲",
  "Concert Tickets 🎟️",
  "Tech Gadgets 📱",
  "Gardening Tools 🌱",
  "Pizza Party 🍕",
  "Ice Cream Treats 🍦",
  "Sunday Brunch 🍳",
  "Fitness Club 🏋️",
  "Spa Day 💆",
  "Chocolate Stash 🍫",
  "Sushi Date 🍣",
  "Beach Day 🏖️",
  "Happy Hour 🍹",
  "Cheese Platter 🧀",
  "DIY Projects 🔨",
  "Tea Time 🫖",
  "Vegan Snacks 🥑",
  "Wine Night 🍷",
  "Burger Bash 🍔",
  "Music Streaming 🎵",
  "Magic Show 🎩",
  "Vintage Finds 🕰️",
  "Plant Babies 🪴",
  "Candle Collection 🕯️",
  "Makeup Magic 💄",
  "Baking Bonanza 🧁",
  "Holiday Gifts 🎁",
  "Car Wash 🚗",
  "Photography 📸",
  "Knitting Kit 🧶",
  "Craft Beer 🍺",
  "Smoothie Sips 🥤",
  "Science Fiction 🛸",
  "Sports Gear ⚽",
  "Picnic Party 🧺",
  "Comedy Club 😂",
  "Thrift Shopping 🛍️",
  "Aquarium Visit 🐠",
  "Skate Session 🛹",
  "Ballet Tickets 🩰",
  "Poetry Books 📖",
  "Farmers Market 🥦",
  "Star Gazing 🔭",
  "Puzzle Pieces 🧩",
  "Herbal Remedies 🌿",
  "Video Games 🎮",
  "Jazz Night 🎷",
  "Camping Trip ⛺",
  "Fast Food Frenzy 🍟",
  "New Sneakers 👟",
  "Online Course 🖥️",
  "Fishing Trip 🎣",
  "Tailgate Party 🍗",
  "Ghost Tour 👻",
];

function getRandomExpenseName() {
  return expenseNames[Math.floor(Math.random() * expenseNames.length)];
}

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
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint + `ledger/get/`, {
          params: {
            ledger: ledgerId,
          },
        })
        .then((response) => {
          resolve(response.data); // Resolve the promise with the response data
        })
        .catch((error) => {
          // return an empty array if there's an error
          resolve([]); // Reject the promise if there's an error
        });
    });
  },
  getRandomExpenseName() {
    return getRandomExpenseName();
  },
  getTransactionById(ledgerId, transactionId) {
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint + `transaction/get/`, {
          params: {
            ledger: ledgerId,
            transaction_id: transactionId,
          },
        })
        .then((response) => {
          resolve(response.data[0]); // Resolve the promise with the response data
        })
        .catch((error) => {
          // return an empty array if there's an error
          resolve([]); // Reject the promise if there's an error
        });
    });
  },
  getActiveMembers(ledgerId) {
    // get from endpoint /members with key ledgerId
    // [flat list of names (string)]
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint + `members/get/`, {
          params: {
            ledger: ledgerId,
          },
        })
        .then((response) => {
          resolve(response.data); // Resolve the promise with the response data
        })
        .catch((error) => {
          resolve([]); // Reject the promise if there's an error
        });
    });
  },
  getAllMembers(ledgerId) {
    return axios
      .get(endpoint + "members", {
        params: {
          ledger: ledgerId,
        },
      })
      .then((response) => {
        return response.data;
      });
  },
  getBalances(ledgerId) {
    // get from endpoint /balances with key ledgerId
    // {
    //   memberName: balance (int or float)
    // }
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint + `balances/get/`, {
          params: {
            ledger: ledgerId,
          },
        })
        .then((response) => {
          resolve(response.data); // Resolve the promise with the response data
        })
        .catch((error) => {
          resolve({});
        });
    });
  },
  getDebts(ledgerId) {
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint + `settlements/get/`, {
          params: {
            ledger: ledgerId,
          },
        })
        .then((response) => {
          resolve(response.data); // Resolve the promise with the response data
        })
        .catch((error) => {
          resolve([]); // Reject the promise if there's an error
        });
    });
  },
  getCategories(ledgerId) {
    // get from endpoint /categories with key ledgerId
    return axios
      .get(endpoint + "categories/get/", {
        params: {
          ledger: ledgerId,
        },
      })
      .then((response) => {
        return response.data;
      });
  },
  getWorkspaces() {
    // get from endpoint /workspaces
    return axios.get(endpoint + "workspaces").then((response) => {
      return response.data;
    });
  },
  editTransaction(transaction) {
    // post to endpoint /transactions with key ledgerId
    // transaction is the same as the response from getTransactions
    // but without the id field
    return axios
      .post(endpoint + "transaction/edit/", transaction)
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.error("Error:", error.response.data);
      });
  },
  deleteTransaction(ledgerId, transactionId) {
    // post to endpoint /transactions with key ledgerId
    return axios
      .post(endpoint + "transactions", {
        ledger_id: ledgerId,
        transactionId: transactionId,
      })
      .then((response) => {
        return response.data;
      });
  },
  addMember(ledgerId, member) {
    // post to endpoint /members with key ledgerId
    return new Promise((resolve, reject) => {
      axios
        .post(endpoint + `members/add/`, {
          ledger: ledgerId,
          member: member,
        })
        .then((response) => {
          resolve(response.data); // Resolve the promise with the response data
        })
        .catch((error) => {
          console.error("Error:", error.response.data);
          reject(error); // Reject the promise if there's an error
        });
    });
  },
  archiveMember(ledgerId, member) {
    // post to endpoint /members with key ledgerId
    return axios
      .post(endpoint + "members", {
        ledger_id: ledgerId,
        member: member,
        action: "archive",
      })
      .then((response) => {
        return response.data;
      });
  },
  settleDebt(debtData) {
    // post to endpoint /settleDebt with key ledgerId
    return axios.post(endpoint + "settle/", debtData).then((response) => {
      return response.data;
    });
  },
};
