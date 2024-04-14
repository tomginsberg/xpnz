import transactions from "./transactions.json";
import members from "./members.json";

const memberIDToNames = mapIdToValue(members, "name");
const memberIDToColors = mapIdToValue(members, "color");
const memberNames = members.map(member => member.name);
let transactionFormatted = transactions.map(cleanTransaction).sort((a, b) => b.date - a.date);
// sort by date
const transactionsIDs = mapByKey(transactionFormatted, "id");

const expenseNames = ["Coffee Break ☕", "Pet Supplies 🐾", "Book Club 📚", "Movie Night 🎬", "Travel Fund ✈️", "Art Supplies 🎨", "Game Night 🎲", "Concert Tickets 🎟️", "Tech Gadgets 📱", "Gardening Tools 🌱", "Pizza Party 🍕", "Ice Cream Treats 🍦", "Sunday Brunch 🍳", "Fitness Club 🏋️", "Spa Day 💆", "Chocolate Stash 🍫", "Sushi Date 🍣", "Beach Day 🏖️", "Happy Hour 🍹", "Cheese Platter 🧀", "DIY Projects 🔨", "Tea Time 🫖", "Vegan Snacks 🥑", "Wine Night 🍷", "Burger Bash 🍔", "Music Streaming 🎵", "Magic Show 🎩", "Vintage Finds 🕰️", "Plant Babies 🪴", "Candle Collection 🕯️", "Makeup Magic 💄", "Baking Bonanza 🧁", "Holiday Gifts 🎁", "Car Wash 🚗", "Photography 📸", "Knitting Kit 🧶", "Craft Beer 🍺", "Smoothie Sips 🥤", "Science Fiction 🛸", "Sports Gear ⚽", "Picnic Party 🧺", "Comedy Club 😂", "Thrift Shopping 🛍️", "Aquarium Visit 🐠", "Skate Session 🛹", "Ballet Tickets 🩰", "Poetry Books 📖", "Farmers Market 🥦", "Star Gazing 🔭", "Puzzle Pieces 🧩", "Herbal Remedies 🌿", "Video Games 🎮", "Jazz Night 🎷", "Camping Trip ⛺", "Fast Food Frenzy 🍟", "New Sneakers 👟", "Online Course 🖥️", "Fishing Trip 🎣", "Tailgate Party 🍗", "Ghost Tour 👻"];

function cleanTransaction(item) {
  const totalAmount = item.amounts.reduce((sum, current) => sum + current.amount, 0);
  const date = (new Date(item.date * 1000));
  const totalWeight = item.weights.reduce((sum, current) => sum + current.weight, 0);
  return {
    price: totalAmount,
    category: item.category,
    currency: item.currency,
    date: date,
    name: item.description,
    id: item.id,
    by: item.amounts.map(amount => memberIDToNames[amount.member_id]),
    for: item.weights.map(amount => memberIDToNames[amount.member_id]),
    weights: item.weights.map(amount => amount.weight),
    normalizedWeights: item.weights.map(amount => totalAmount * amount.weight / totalWeight),
    ledger_id: item.ledger_id,
    transfer: item.transfer,
    contributions: item.amounts.map(amount => amount.amount),
    expenseType: "Expense",
    isIncome: false
  };
}

function memberBalances(members, transactions) {
  const balances = {};
  members.forEach(member => {
      balances[member.id] = 0;
    }
  );
  // add contributions for each member in transaction.by
  // subtract normalizedWeights for each member in transaction.for
  transactions.forEach(transaction => {
    transaction.by.forEach((member, index) => {
      balances[member] += transaction.contributions[index];
    });

    transaction.for.forEach((member, index) => {
      balances[member] -= transaction.normalizedWeights[index];
    });
  });
  return balances;
}


function settle() {
  let balances = memberBalances(members, transactions);
  let neg = {};
  let pos = {};

  for (let member in balances) {
    let balance = balances[member];
    if (balance < 0) {
      neg[member] = -balance;
    } else if (balance > 0) {
      pos[member] = balance;
    }
  }
  return settleRecursive(pos, neg);
}

function dropMin(balances) {
  let minMember = Object.keys(balances).reduce((a, b) => balances[a] < balances[b] ? a : b);
  let minBalance = balances[minMember];
  let b = { ...balances };
  delete b[minMember];
  return [{ member: minMember, balance: minBalance }, b];
}

function popKey(d) {
  return Object.keys(d).pop();
}

function settleRecursive(pos, neg) {
  if (Object.keys(pos).length === 1) {
    let x = popKey(pos);
    return Object.keys(neg).map(a => [a, x, neg[a]]);
  }
  if (Object.keys(neg).length === 1) {
    let x = popKey(neg);
    return Object.keys(pos).map(a => [x, a, pos[a]]);
  } else {
    let [nm, nr] = dropMin(neg);
    let [pm, pr] = dropMin(pos);
    if (nm.balance <= pm.balance) {
      pos[pm.member] = pm.balance - nm.balance;
      let transactions = settleRecursive(pos, nr);
      transactions.push([nm.member, pm.member, nm.balance]);
      return transactions;
    } else if (nm.balance > pm.balance) {
      neg[nm.member] = nm.balance - pm.balance;
      let transactions = settleRecursive(pr, neg);
      transactions.push([nm.member, pm.member, pm.balance]);
      return transactions;
    } else {
      let transactions = settleRecursive(pr, nr);
      transactions.push([nm.member, pm.member, pm.balance]);
      return transactions;
    }
  }
}


function mapIdToValue(objectsArray, key) {
  const idColorMap = {};

  objectsArray.forEach(item => {
    idColorMap[item.id] = item[key];
  });

  return idColorMap;
}

function mapByKey(objectsArray, key) {
  const idColorMap = {};

  objectsArray.forEach(item => {
    idColorMap[item[key]] = item;
  });

  return idColorMap;
}

export const ProductService = {
  getProductsData() {
    return Promise.resolve(transactionFormatted);
  },
  getMembers() {
    console.log("Getting members", memberNames);
    return memberNames;
  },
  getRandomExpenseName() {
    return expenseNames[Math.floor(Math.random() * expenseNames.length)];
  },
  deleteProduct(id) {
    // Delete from transactionFormatted where id matches
    // use filter
    console.log("Deleting product with id:", id);
    delete transactionsIDs[id];
    transactionFormatted = transactionFormatted.filter(transaction => transaction.id !== id);
    return Promise.resolve();
  },
  getMemberColor(id) {
    return memberIDToColors[id];
  },
  getMemberNames() {
    return mapIdToValue(members, "name");
  },
  getMemberName(id) {
    return memberIDToNames[id];
  },
  async getProductById(id) {
    console.log("Getting product with id:", id);
    if (id === "new") {
      return {
        price: '',
        category: null,
        currency: "CAD",
        date: new Date(),
        name: "",
        id: "new",
        by: [],
        for: [],
        weights: [],
        normalizedWeights: [],
        ledger_id: null,
        transfer: false,
        contributions: [],
        expenseType: "Expense",
        isIncome: false
      };
    }
    return transactionsIDs[id];
  },

  async getCategories() {
    return [...new Set(transactionFormatted.map(transaction => transaction.category))];
  },

  async saveProduct(product) {
    // Implement save logic here
    // In a real application, this would involve an HTTP request to save the product data
    console.log("Saving product:", product);
    // Simulate saving by returning a resolved promise
    return Promise.resolve();
  }

};

