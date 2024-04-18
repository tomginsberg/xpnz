<script setup>
import DarkMode from "../components/DarkMode.vue";
import { ref, onMounted, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ProductService } from "../service/ProductService";
import VueInputCalculator from "vue-input-calculator";

import MultiSelect from "primevue/multiselect";
import Calendar from "primevue/calendar";
import Button from "primevue/button";
import Dropdown from "primevue/dropdown";

const expenseName = ref("");
const router = useRouter();
const route = useRoute();
const ledgerID = ref("");
const categories = ref([]);
const members = ref([]);
const recurringExpense = ref(false);
const multiContribution = ref(false);
const unequalSplitRef = ref(null);
const recurringRef = ref(null);
const product = ref({});
const isNew = ref(false);
const unequalSplit = ref(false);
const contributions = ref([]);
const deleteModal = ref(false);
const byMembers = ref([]);
import { initFlowbite } from "flowbite";
import Dialog from "primevue/dialog";

const date = ref(null);

const flagEmoji = {
  CAD: "🇨🇦",
  USD: "🇺🇸",
  EUR: "🇪🇺",
};
const currencies = ["CAD", "USD", "EUR"];
const showDropdown = ref(false);
function toggleDropdown() {
  showDropdown.value = !showDropdown.value;
}

function selectCurrency(currency) {
  product.value.currency = currency;
  showDropdown.value = false;
}

const weights = ref([]);
onMounted(async () => {
  initFlowbite();
  ledgerID.value = route.params.ledgerID;
  expenseName.value = ProductService.getRandomExpenseName();
  const productId = route.params.productId;
  if (productId) {
    const fetchedProduct = await ProductService.getProductById(productId);
    if (productId === "new") {
      isNew.value = true;
    }
    if (fetchedProduct) {
      product.value = fetchedProduct; // Update the product with fetched data
      unequalSplit.value =
        fetchedProduct.weights &&
        fetchedProduct.weights.some(
          (weight, index) => weight !== fetchedProduct.weights[0],
        );
      multiContribution.value = fetchedProduct.by.length > 1;
      contributions.value = fetchedProduct.contributions;
      byMembers.value = fetchedProduct.by;
      weights.value = fetchedProduct.weights;
      date.value = fetchedProduct.date.toISOString().split("T")[0];
    } else {
      console.error("Product not found");
      // Handle product not found, e.g., redirect
    }
    categories.value = await ProductService.getCategories();
    members.value = await ProductService.getMembers();
  }
});

function saveProduct() {
  // Save product logic goes here
  // update product.value.normalizedWeights
  // normalizedWeights: item.weights.map(amount => totalAmount * amount.weight / totalWeight),
  if (!unequalSplit.value) {
    product.value.weights = product.value.for.map(() => 1);
  }
  let totalWeight = product.value.weights.reduce(
    (acc, weight) => acc + weight,
    0,
  );
  product.value.normalizedWeights = product.value.for.map((member, index) => {
    return (product.value.price * product.value.weights[index]) / totalWeight;
  });
  ProductService.saveProduct(product.value);
  router.push(`/${route.params.ledgerId}`); // Navigate back to the product list page
}

function cancelEdit() {
  router.push(`/${route.params.ledgerId}`); // Navigate back without saving
}

const itemToDelete = ref("");
const deleteButtonDisabled = computed(() => {
  return !(itemToDelete.value === product.value.name);
});

function openDeleteModal() {
  itemToDelete.value = "";
  deleteModal.value = true;
}

function deleteProduct() {
  deleteModal.value = false;
  ProductService.deleteProduct(product.value.id);
  router.push(`/${route.params.ledgerId}`);
}

const totalContributions = computed(() => {
  return contributions.value.reduce(
    (total, contribution) => total + Number(contribution),
    0,
  );
});

watch(multiContribution, (newValue) => {
  if (newValue) {
    // When multiContribution is enabled, set product.price to the sum of contributions
    contributions.value = product.value.by.map(
      () => product.value.price / product.value.by.length,
    );
    product.value.price = totalContributions.value;
  } else {
    contributions.value = product.value.by.map(
      () => product.value.price / product.value.by.length,
    );
  }
});

watch(totalContributions, (newValue) => {
  if (multiContribution.value) {
    product.value.price = newValue;
  }
});
</script>

<template>
  <div
    class="fixed top-0 z-10 w-full border-b border-gray-200 bg-gray-100 p-4 dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="flex flex-row">
      <h1
        class="flex-auto px-1 pt-1 text-lg font-semibold text-gray-800 dark:text-white"
      >
        {{ product.id === "new" ? "📝" : "✏️" }}
        ️<span class="px-1" />
        {{ product.id === "new" ? "New" : "Edit" }}
        {{ product.isIncome ? "Income" : "Expense" }}
      </h1>
      <div class="z-100">
        <DarkMode />
      </div>
    </div>
  </div>

  <div
    class="fixed bottom-4 left-1/2 z-50 h-16 w-[60%] max-w-lg -translate-x-1/2 rounded-full bg-gray-200 pr-2 shadow-xl dark:bg-gray-700"
  >
    <div
      class="mx-auto grid h-full max-w-lg grid-cols-3"
      id="default-tab"
      role="tablist"
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
          @click="saveProduct"
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
          v-model="product.name"
          class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
          :placeholder="expenseName"
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
          v-model="product.price"
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
            v-model="product.price"
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
        @click="toggleDropdown"
        id="dropdown-currency-button"
        class="z-[6] inline-flex flex-shrink-0 items-center rounded-e-lg border border-gray-300 bg-gray-100 px-4 py-2.5 text-center text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus:ring-4 focus:ring-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-700"
        type="button"
      >
        <span class="mr-2">{{ flagEmoji[product.currency] }}</span>

        {{ product.currency }}
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
        class="z-[6] w-36 divide-y divide-gray-100 rounded-lg bg-white shadow dark:bg-gray-700"
        :class="[showDropdown ? 'block' : 'hidden']"
        style="
          position: absolute;
          inset: 0px auto auto 0px;
          margin: 0px;
          transform: translate3d(267.429px, 222.095px, 0px);
        "
        data-popper-placement="bottom"
      >
        <ul
          class="py-2 text-sm text-gray-700 dark:text-gray-200"
          aria-labelledby="dropdown-currency-button"
        >
          <li v-for="currency in currencies">
            <button
              @click="selectCurrency(currency)"
              type="button"
              class="inline-flex w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
              role="menuitem"
            >
              <div class="inline-flex items-center">
                {{ flagEmoji[currency] }} {{ currency }}
              </div>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div class="pt-5">
      <Dropdown
        editable
        v-model="product.category"
        :options="categories"
        dropdown
        placeholder="Select a Category"
        class="w-full"
      />
    </div>

    <div class="max-w mt-5">
      <Calendar
        v-model="product.date"
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
          v-model="product.isIncome"
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
          @click="unequalSplit = !unequalSplit"
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
          v-model="recurringExpense"
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
        v-model="product.by"
        :options="members"
        display="chip"
        placeholder="Select Member(s)"
        @change="multiContribution = product.by.length > 1"
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
        v-model="product.for"
        :options="members"
        display="chip"
        placeholder="Select Member(s)"
        @change="multiContribution = product.by.length > 1"
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
        <div v-for="(member, index) in product.by" class="flex-col px-1">
          <label
            for="email"
            class="justify-content-center mb-2 mt-2 block flex-1 content-center text-wrap px-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            {{ member }}</label
          >
          <input
            type="number"
            v-model="contributions[index]"
            id="email"
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
        Split Weights
      </p>
      <div class="max-w flex flex-wrap pt-2">
        <div v-for="(member, index) in product.for" class="flex flex-col px-1">
          <label
            for="email"
            class="justify-content-center mb-2 mt-2 block flex-1 content-center px-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            {{ member }}</label
          >
          <input
            type="number"
            v-model="product.weights[index]"
            id="email"
            class="block w-20 flex-1 rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            placeholder="0"
            required
          />
        </div>
      </div>
    </div>
    <footer ref="unequalSplitRef"></footer>

    <!-- Recurring Expense Options -->
    <div
      v-if="recurringExpense"
      class="mt-5 rounded-lg border border-gray-300 px-4 py-3 text-gray-900 dark:border-gray-600 dark:text-white"
    >
      <p class="mb-2 text-sm font-semibold">Recurring Expense</p>
      <div class="field">
        <div class="grid grid-cols-3 items-center">
          <label for="frequency" class="pl-2 text-sm">Frequency:</label>
          <div class="col-span-2">
            <Dropdown
              id="frequency"
              v-model="product.frequency"
              :options="['Daily', 'Weekly', 'Monthly', 'Yearly']"
              class="w-full bg-gray-950"
              inputClass="text-white p-2 w-full"
            />
          </div>
        </div>
        <div class="mt-2 grid grid-cols-3 items-center">
          <label for="end-date" class="pl-2 text-sm">End Date:</label>
          <div class="col-span-2 flex items-center">
            <Calendar
              v-model="product.endDate"
              placeholder="(Optional)"
              inputClass="p-2 w-full"
              id="end-date"
            />
            <button
              type="button"
              @click="product.endDate = null"
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
                Type "<span class="font-semibold">{{ product.name }}</span
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
                  @click="deleteProduct()"
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

<style scoped>
.dropdown-hidden {
  display: none;
}
.dropdown-visible {
  display: block;
}
</style>
