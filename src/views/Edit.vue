<script setup>
import DarkMode from "../components/DarkMode.vue";
import {ref, onMounted, computed, watch} from "vue";
import {useRouter, useRoute} from "vue-router";
import {XPNZService} from "../service/XPNZService.js";
import VueInputCalculator from "vue-input-calculator";
import {initFlowbite} from "flowbite";

import MultiSelect from "primevue/multiselect";
import Calendar from "primevue/calendar";
import Button from "primevue/button";
import Dropdown from "primevue/dropdown";
import Dialog from "primevue/dialog";

const flagEmoji = {
  CAD: "🇨🇦",
  USD: "🇺🇸",
  EUR: "🇪🇺",
  PLN: "🇵🇱",
};
const currencies = ["CAD", "USD", "EUR", "PLN"];

const router = useRouter();
const route = useRoute();
const ledgerID = route.params.ledgerId;
let transactionID = route.params.productId;

const categories = ref([]);
const members = ref([]);

const placeholderName = ref("");
const name = ref("");
const category = ref("");
const amount = ref(null);
const currency = ref("CAD");
const date = ref(new Date());

const isIncome = ref(false);
const unequalSplit = ref(false);
const isRecurring = ref(false);
const isNew = ref(false);
const isTransfer = ref(false);
const byMembers = ref([]);
const multiContribution = ref(false);
const expenseType = ref("Expense");

const forMembers = ref([]);
const byValues = ref([]);
const forWeights = ref([]);
const forValues = ref([]);

const frequency = ref(null);
const endDate = ref(null);

const deleteModal = ref(false);

onMounted(async () => {
  initFlowbite();
  if (transactionID === "new") {
    isNew.value = true;
    placeholderName.value = XPNZService.getRandomExpenseName();
  } else if (transactionID) {
    const transaction = await XPNZService.getTransactionById(
        ledgerID,
        transactionID,
    );
    if (transaction) {
      name.value = transaction.name;
      category.value = transaction.category;
      isIncome.value = transaction.expense_type.toLowerCase() === "income";
      if (isIncome.value && transaction.by.total < 0) {
        amount.value = -transaction.by.total;
      } else {
        amount.value = transaction.by.total;
      }

      currency.value = transaction.currency;
      date.value = new Date(transaction.date);

      isTransfer.value = transaction.expense_type.toLowerCase() === "transfer";
      isRecurring.value = transaction.recurring;
      byMembers.value = transaction.by.members;
      forMembers.value = transaction.for.members;
      byValues.value = transaction.by.split_values.map((value) =>
          Math.abs(value),
      );
      forWeights.value = transaction.for.split_weights;
      forValues.value = transaction.for.split_values.map((value) =>
          Math.abs(value),
      );
      multiContribution.value = transaction.by.members.length > 1;
      unequalSplit.value =
          transaction.for["split_weights"] &&
          transaction.for["split_weights"].some(
              (weight, index) => weight !== transaction.for["split_weights"][0],
          );
    } else {
      await router.push(`/${ledgerID}`);
    }
  }

  categories.value = await XPNZService.getCategories(ledgerID);
  members.value = await XPNZService.getActiveMembers(ledgerID);
  // add any members from forMembers and byMembers that are not in members
  forMembers.value.forEach((member) => {
    if (!members.value.includes(member)) {
      members.value.push(member);
    }
  });
  byMembers.value.forEach((member) => {
    if (!members.value.includes(member)) {
      members.value.push(member);
    }
  });
});

// make expense name computed property based on isIncome and isTransfer
watch([isIncome, isTransfer], () => {
  if (isIncome.value) {
    expenseType.value = "Income";
  } else if (isTransfer.value) {
    expenseType.value = "Transfer";
  } else {
    expenseType.value = "Expense";
  }
});

function selectCurrency(selectedCurrency) {
  currency.value = selectedCurrency;
  document.getElementById("dropdown-currency-button").click();
}

function saveExpense() {
  // so some validation
  if (name.value === "" && category.value === "") {
    alert(`Please enter a name or a category for the ${expenseType.value}`);
    return;
  }
  if (amount.value === null || amount.value === 0) {
    alert("Please enter an amount for the expense");
    return;
  }
  if (amount < 0) {
    alert("Amount cannot be negative");
    return;
  }
  if (byMembers.value.length === 0) {
    alert("Please select at least one member who paid for the expense");
    return;
  }
  if (forMembers.value.length === 0) {
    alert("Please select at least one member to split the expense with");
    return;
  }
  // check for negative values in byValues
  if (byValues.value.some((value) => value < 0)) {
    alert("Contribution amounts cannot be negative");
    return;
  }
  // check for negative values in forWeights
  if (forWeights.value.some((weight) => weight < 0)) {
    alert("Split ratios cannot be negative");
    return;
  }
  // check if the sum of forWeights is 0
  if (sum(forWeights.value) === 0 && unequalSplit.value) {
    alert("At least one split ratio must be greater than 0");
    return;
  }
  console.log(
      "Saving expense",
      name.value,
      amount.value,
      currency.value,
      " for  date",
      date.value,
      date.value.getUTCDate(),
  );

  XPNZService.editTransaction({
    id: transactionID,
    ledger: ledgerID.toLowerCase(),
    name: name.value,
    category: category.value,
    by: {
      members: byMembers.value,
      split_values: byValues.value,
      total: amount.value,
    },
    to: {
      members: forMembers.value,
      split_weights: unequalSplit.value
          ? forWeights.value
          : Array(forMembers.value.length).fill(1),
    },
    expense_type: expenseType.value.toLowerCase(),
    currency: currency.value,
    date: date.value.toISOString(),
    recurring: isRecurring.value
        ? {frequency: frequency.value, end_date: endDate.value}
        : false,
  });
  router.push(`/${ledgerID}`); // Navigate back to the product list page
}

function cancelEdit() {
  router.push(`/${ledgerID}`); // Navigate back without saving
}

const itemToDelete = ref("");
const deleteButtonDisabled = computed(() => {
  return !(itemToDelete.value === name.value);
});

function openDeleteModal() {
  if (isNew.value) {
    router.push(`/${ledgerID}`);
    return;
  }
  console.log("Opening delete modal");
  itemToDelete.value = "";
  deleteModal.value = true;
}

function deleteExpense() {
  deleteModal.value = false;
  console.log("Deleting expense", name.value, transactionID);
  XPNZService.deleteTransaction(ledgerID, transactionID);
  router.push(`/${ledgerID}`);
}

// watch byMembers
watch(byMembers, () => {
  multiContribution.value = byMembers.value.length > 1;
});

function sum(arr) {
  return arr.reduce((acc, value) => acc + Number(value), 0);
}

// when byMembers has an item remove
// find the index of the removed item and remove the corresponding value from byValues
// and remove it as well and also subtract the value from the total amount
watch(byMembers, (newVal, oldVal) => {
  if (newVal.length === 0) {
    byValues.value = [];
  } else if (newVal.length < oldVal.length) {
    if (newVal.length === 1) {
      byValues.value = [sum(byValues.value)];
    } else {
      const removedMember = oldVal.filter(
          (member) => !newVal.includes(member),
      )[0];
      const removedIndex = oldVal.indexOf(removedMember);
      byValues.value.splice(removedIndex, 1);
    }
    amount.value = sum(byValues.value);
  } else if (newVal.length > oldVal.length) {
    if (oldVal.length === 0) {
      byValues.value = [amount.value];
      for (let i = 1; i < newVal.length - oldVal.length; i++) {
        byValues.value.push(null);
      }
    } else {
      for (let i = 0; i < newVal.length - oldVal.length; i++) {
        byValues.value.push(null);
      }
    }
    amount.value = sum(byValues.value);
  }
});

const totalContributions = computed(() => {
  return sum(byValues.value);
});

watch(totalContributions, (newValue) => {
  if (multiContribution.value) {
    amount.value = newValue;
  }
});

// watch amount when multiContribution is false and update byValues to be an array with a single value
watch(amount, (newValue) => {
  if (!multiContribution.value) {
    byValues.value = [newValue];
  }
});

watch(forMembers, (newVal, oldVal) => {
  if (newVal.length === 0) {
    forWeights.value = [];
  } else if (newVal.length < oldVal.length) {
    const removedMember = oldVal.filter(
        (member) => !newVal.includes(member),
    )[0];
    const removedIndex = oldVal.indexOf(removedMember);
    forWeights.value.splice(removedIndex, 1);
  } else if (newVal.length > oldVal.length) {
    for (let i = 0; i < newVal.length - oldVal.length; i++) {
      forWeights.value.push(1);
    }
  }
});


function showToast(message) {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  // Unique ID for the toast
  const toastId = `toast-${Date.now()}`;

  // Create toast element
  const toast = document.createElement('div');
  toast.id = toastId;
  toast.className = 'mx-4 my-1 flex items-center w-full max-w-lg p-4 mb-4 text-blue-800 bg-blue-50 rounded-lg shadow dark:text-blue-400 dark:bg-gray-700 transition-opacity duration-300 shadow-xl';
  toast.setAttribute('role', 'alert');

  // Create icon
  const icon = document.createElement('div');
  icon.className = 'inline-flex items-center justify-center flex-shrink-0 w-8 h-8';
  icon.innerHTML = `📋`;
  toast.appendChild(icon);

  // Create message
  const messageContainer = document.createElement('div');
  messageContainer.className = 'ms-3 text-sm font-normal';
  messageContainer.textContent = message;
  toast.appendChild(messageContainer);

  // Create close button
  const closeButton = document.createElement('button');
  closeButton.className = 'ms-auto -mx-1.5 -my-1.5 bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex items-center justify-center h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700';
  closeButton.setAttribute('data-dismiss-target', `#${toastId}`);
  closeButton.setAttribute('aria-label', 'Close');
  closeButton.innerHTML = `
    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
    </svg>
  `;
  closeButton.onclick = () => {
    const target = document.querySelector(closeButton.getAttribute('data-dismiss-target'));
    if (target) {
      target.classList.add('opacity-0');
      setTimeout(() => target.remove(), 300);
    }
  };
  toast.appendChild(closeButton);

  // Append toast to container
  toastContainer.appendChild(toast);

  // Auto fade-out and remove toast after a delay
  setTimeout(() => {
    toast.classList.add('opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 1000);
}


function copyExpense() {
  isNew.value = true;
  transactionID = "new";
  date.value = new Date();
  showToast('Expense copied');
}
</script>


<template>

  <div id="toast-container" class="fixed top-4 w-full flex justify-center z-50"></div>
  <div
      class="fixed top-0 z-10 w-full border-b border-gray-200 bg-gray-100 p-4 dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="flex flex-row">
      <h1
          class="flex-auto px-1 pt-1 text-lg font-semibold text-gray-800 dark:text-white"
      >
        {{ isNew ? "📝" : "✏️" }}
        ️<span class="px-1"/>
        {{ isNew ? "New" : "Edit" }}
        {{ expenseType }}
      </h1>
      <div class="z-100">
        <DarkMode/>
      </div>
    </div>
  </div>

  <div
      class="fixed bottom-4 left-1/2 z-50 h-16 w-[60%] max-w-lg -translate-x-1/2 rounded-full bg-gray-200 pr-2 shadow-xl dark:bg-gray-700"
  >
    <div
        class="mx-auto grid h-full max-w-lg grid-cols-3"
    >
      <div class="flex items-center justify-center">
        <button
            @click="cancelEdit"
            type="button"
            class="group inline-flex h-10 w-10 items-center justify-center rounded-xl bg-gray-300 font-medium shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-800 dark:focus:ring-blue-800"
        >
          ⬅️
        </button>
      </div>

      <div class="flex items-center justify-center">
        <button
            @click="saveExpense"
            type="button"
            class="group inline-flex h-10 w-10 items-center justify-center rounded-xl bg-gray-300 font-medium shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-800 dark:focus:ring-blue-800"
        >
          💾
        </button>
      </div>

      <div class="flex items-center justify-center">
        <button
            @click="openDeleteModal"
            type="button"
            class="group inline-flex h-10 w-10 items-center justify-center rounded-xl bg-gray-300 font-medium shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-800 dark:focus:ring-blue-800"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>

  <div
      v-show="!isNew"
      class="fixed bottom-6 right-3 z-50">
    <button
        @click="copyExpense"
        type="button"
        class="group inline-flex h-10 w-10 items-center justify-center rounded-xl bg-gray-300 font-medium shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-800 dark:focus:ring-blue-800"
    >
      <i class="pi pi-clone text-l dark:text-gray-400"></i>
    </button>
  </div>

  <div class="px-5 pb-32 pt-[5rem]">
    <form class="mx-auto w-full">
      <div class="mb-5">
        <label
            for="name"
            class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"
        >Expense Name</label
        >
        <input
            type="text"
            id="name"
            v-model="name"
            class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            :placeholder="placeholderName"
            required
        />
      </div>
    </form>

    <div class="flex">
      <div class="relative w-full">
        <div
            class="pointer-events-none absolute inset-y-0 start-0 top-0 flex items-center ps-3.5"
        >
          <svg
              class="h-4 w-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
          >
            <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1M2 5h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm8 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z"
            />
          </svg>
        </div>
        <input
            v-model="amount"
            type="number"
            id="currency-input"
            class="z-20 block w-full rounded-s-lg border border-e-2 border-gray-300 border-e-gray-50 bg-gray-50 p-2.5 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:border-e-gray-700 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500"
            placeholder="Enter amount"
            required
            :disabled="multiContribution"
        />
      </div>
      <div
          class="border-b border-l border-t border-gray-300 bg-gray-50 px-2 pt-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 dark:focus:border-blue-500"
      >
        <div v-if="!multiContribution">
          <VueInputCalculator
              enableKeyboard
              v-model="amount"
              number-buttons-bg-color="#0f172a"
              action-buttons-bg-color="#1e293b"
              bg-color="#020617"
              text-color="white"
              event-buttons-bg-color="#334155"
              action-success-button-bg-color="#1d4ed8"
          >
            <i class="pi pi-calculator text-xl"></i>
          </VueInputCalculator>
        </div>
        <div v-else>
          <i class="pi pi-lock text-xl text-green-500"></i>
        </div>
      </div>

      <button
          data-dropdown-toggle="dropdown-currency"
          id="dropdown-currency-button"
          class="z-[6] inline-flex flex-shrink-0 items-center rounded-e-lg border border-gray-300 bg-gray-100 px-4 py-2.5 text-center text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
          type="button"
      >
        <span class="mr-2">{{ flagEmoji[currency] }}</span>

        {{ currency }}
        <svg
            class="ms-2.5 h-2.5 w-2.5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 10 6"
        >
          <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m1 1 4 4 4-4"
          />
        </svg>
      </button>
      <div
          id="dropdown-currency"
          class="z-[6] hidden w-36 divide-y divide-gray-100 rounded-lg bg-white shadow dark:bg-gray-700"
      >
        <ul
            class="py-2 text-sm text-gray-700 dark:text-gray-200"
            aria-labelledby="dropdown-currency-button"
        >
          <li v-for="dropdownCurrency in currencies">
            <button
                @click="selectCurrency(dropdownCurrency)"
                type="button"
                class="inline-flex w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                role="menuitem"
            >
              <div class="inline-flex items-center">
                {{ flagEmoji[dropdownCurrency] }} {{ dropdownCurrency }}
              </div>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div class="pt-5">
      <Dropdown
          editable
          v-model="category"
          :options="categories"
          filter
          dropdown
          placeholder="Select a Category"
          class="w-full"
      />
    </div>

    <div class="max-w mt-5">
      <Calendar
          v-model="date"
          showIcon
          iconDisplay="input"
          touch-u-i
          class="w-full"
      />
    </div>

    <div class="mx-3 mb-5 mt-4 flex flex-row justify-between">
      <div class="flex h-5 items-center">
        <input
            id="remember"
            type="checkbox"
            value=""
            v-model="isIncome"
            :disabled="isTransfer"
            :class="{ 'cursor-not-allowed': isTransfer }"
            class="focus:ring-3 h-4 w-4 rounded border border-gray-300 bg-gray-50 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-blue-600 dark:focus:ring-offset-gray-800"
            required
        />
        <label
            for="remember"
            class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Income</label
        >
      </div>

      <div class="flex h-5 items-center">
        <input
            id="remember"
            type="checkbox"
            value=""
            v-model="unequalSplit"
            :disabled="isTransfer"
            :class="{ 'cursor-not-allowed': isTransfer }"
            class="focus:ring-3 h-4 w-4 rounded border border-gray-300 bg-gray-50 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-blue-600 dark:focus:ring-offset-gray-800"
            required
        />
        <label
            for="remember"
            class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Unequal Split</label
        >
      </div>

      <div class="flex h-5 items-center">
        <input
            id="remember"
            type="checkbox"
            value=""
            v-model="isRecurring"
            :disabled="isTransfer"
            :class="{ 'cursor-not-allowed': isTransfer }"
            class="focus:ring-3 h-4 w-4 rounded border border-gray-300 bg-gray-50 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-blue-600 dark:focus:ring-offset-gray-800"
            required
        />
        <label
            for="remember"
            class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Recurring</label
        >
      </div>
    </div>

    <form>
      <label
          for="membersby"
          class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"
      >Paid By</label
      >

      <MultiSelect
          id="membersby"
          v-model="byMembers"
          :options="members"
          :disabled="isTransfer"
          display="chip"
          placeholder="Select Member(s)"
      />
    </form>

    <form class="pt-3">
      <label
          for="membersfor"
          class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"
      >Split By</label
      >

      <MultiSelect
          id="membersfor"
          v-model="forMembers"
          :disabled="isTransfer"
          :options="members"
          display="chip"
          placeholder="Select Member(s)"
      />
    </form>

    <div
        v-if="multiContribution"
        class="mt-5 rounded-lg border border-gray-300 px-2 py-3 dark:border-gray-600"
    >
      <p class="text-sm font-semibold text-gray-900 dark:text-white">
        Contribution Amounts
      </p>
      <div class="max-w justify-left flex flex-wrap pt-2">
        <div v-for="(member, index) in byMembers" class="flex-col px-1">
          <label
              class="justify-content-center mb-2 mt-2 block flex-1 content-center text-wrap px-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            {{ member }}</label
          >
          <input
              type="number"
              v-model="byValues[index]"
              class="block w-20 flex-1 rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
              placeholder="Amount"
              required
          />
        </div>
      </div>
    </div>

    <div
        v-if="unequalSplit"
        class="mt-5 rounded-lg border border-gray-300 px-2 py-3 dark:border-gray-600"
    >
      <p class="text-sm font-semibold text-gray-900 dark:text-white">
        Split Ratios
      </p>
      <div class="max-w flex flex-wrap pt-2">
        <div v-for="(member, index) in forMembers" class="flex flex-col px-1">
          <label
              class="justify-content-center mb-2 mt-2 block flex-1 content-center px-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            {{ member }}
          </label>

          <VueInputCalculator
              enableKeyboard
              v-model="forWeights[index]"
              number-buttons-bg-color="#0f172a"
              action-buttons-bg-color="#1e293b"
              bg-color="#020617"
              text-color="white"
              event-buttons-bg-color="#334155"
              action-success-button-bg-color="#1d4ed8"
          >
            <input
              type="number"
              v-model="forWeights[index]"
              class="block w-20 flex-1 rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
              placeholder="0"
              required
          />
          </VueInputCalculator>
        </div>
      </div>
    </div>
    <footer ref="unequalSplitRef"></footer>

    <!-- Recurring Expense Options -->
    <div
        v-if="isRecurring"
        class="mt-5 rounded-lg border border-gray-300 px-4 py-3 text-gray-900 dark:border-gray-600 dark:text-white"
    >
      <p class="mb-2 text-sm font-semibold">Recurring Expense</p>
      <div class="field">
        <div class="grid grid-cols-3 items-center">
          <label for="frequency" class="pl-2 text-sm">Frequency:</label>
          <div class="col-span-2">
            <Dropdown
                id="frequency"
                v-model="frequency"
                :options="['Daily', 'Weekly', 'Monthly', 'Yearly']"
                class="w-full"
                inputClass="w-full"
            />
          </div>
        </div>
        <div class="mt-2 grid grid-cols-3 items-center">
          <label for="end-date" class="pl-2 text-sm">End Date:</label>
          <div class="col-span-2 flex items-center">
            <Calendar
                v-model="endDate"
                placeholder="(Optional)"
                inputClass="w-full"
                id="end-date"
            />
            <button
                type="button"
                @click="endDate = null"
                class="ml-2 rounded-lg bg-red-600 p-2 text-white transition duration-150 ease-in-out hover:bg-red-700"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
    <footer ref="recurringRef"></footer>
  </div>

  <div class="flex justify-center">
    <Dialog
        v-model:visible="deleteModal"
        modal
        header="Header"
        :style="{ width: '50rem' }"
    >
      <template #container="{ closeCallback }">
        <div class="p-4">
          <div class="relative rounded-lg bg-white shadow dark:bg-gray-700">
            <button
                @click="deleteModal = false"
                type="button"
                class="absolute end-2.5 top-3 ms-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-transparent text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900 dark:hover:bg-gray-600 dark:hover:text-white"
            >
              <svg
                  class="h-3 w-3"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 14 14"
              >
                <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
              </svg>
            </button>
            <div class="p-4 text-center md:p-5">
              <svg
                  class="mx-auto mb-4 h-12 w-12 text-gray-400 dark:text-gray-200"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 20"
              >
                <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
              </svg>
              <h3
                  class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400"
              >
                Type "<span class="font-semibold">{{ name }}</span
              >" to delete
              </h3>

              <div class="relative">
                <div
                    class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3"
                >
                  <svg
                      class="h-6 w-6 text-gray-800 dark:text-white"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      fill="none"
                      viewBox="0 0 24 24"
                  >
                    <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 12H5m14 0-4 4m4-4-4-4"
                    />
                  </svg>
                </div>

                <input
                    type="text"
                    v-model="itemToDelete"
                    :class="{ 'font-bold': !deleteButtonDisabled }"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                    required
                />
                <button
                    type="submit"
                    v-if="!deleteButtonDisabled"
                    @click="deleteExpense()"
                    :class="{
                    'bg-red-600 hover:bg-red-700': !deleteButtonDisabled,
                    'bg-red-400': deleteButtonDisabled,
                  }"
                    class="absolute bottom-2.5 end-2.5 rounded-lg px-4 py-2 text-sm font-medium text-white"
                >
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>
