<script setup>

import DarkMode from "../components/DarkMode.vue";
import { ref, onMounted, nextTick, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ProductService } from "../service/ProductService";
import VueInputCalculator from "vue-input-calculator";

import MultiSelect from "primevue/multiselect";
import InputText from "primevue/inputtext";
import Calendar from "primevue/calendar";
// import Dropdown from "primevue/dropdown";
import Button from "primevue/button";
import InputNumber from "primevue/inputnumber";
import Dialog from "primevue/dialog";

const expenseName = ref("");
const selectedCities = ref();
const cities = ref([
  { name: "New York", code: "NY" },
  { name: "Rome", code: "RM" },
  { name: "London", code: "LDN" },
  { name: "Istanbul", code: "IST" },
  { name: "Paris", code: "PRS" }
]);

const router = useRouter();
const route = useRoute();
const categories = ref([]);
const submitted = ref(false);
const members = ref([]);
const recurringExpense = ref(false);
const multiContribution = ref(false);
const memberColors = ref({
  tom: "blue",
  rhys: "red",
  dom: "green"
});
const unequalSplitRef = ref(null);
const recurringRef = ref(null);
const openCategoryModal = ref(false);
const newCategory = ref("");
const categoryDropdownRef = ref(null);
const product = ref({});
const isNew = ref(false);
const unequalSplit = ref(false);
const contributions = ref([]);
const deleteModal = ref(false);
const byMembers = ref([]);
const expenseTypes = ["Expense", "Income"];
import { initFlowbite } from "flowbite";
import Dropdown from "primevue/dropdown";

// date in MM/DD/YYYY format make sure to include leading zeroes
const date = ref(null);

const weights = ref([]);
onMounted(async () => {
  initFlowbite();
  expenseName.value = ProductService.getRandomExpenseName();
  const productId = route.params.productId;
  if (productId) {
    const fetchedProduct = await ProductService.getProductById(productId);
    if (productId === "new") {
      isNew.value = true;
    }
    if (fetchedProduct) {
      product.value = fetchedProduct; // Update the product with fetched data
      unequalSplit.value = fetchedProduct.weights && fetchedProduct.weights.some((weight, index) => weight !== fetchedProduct.weights[0]);
      multiContribution.value = fetchedProduct.by.length > 1;
      contributions.value = fetchedProduct.contributions;
      byMembers.value = fetchedProduct.by;
      weights.value = fetchedProduct.weights;
      date.value = fetchedProduct.date.toISOString().split('T')[0];
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
  let totalWeight = product.value.weights.reduce((acc, weight) => acc + weight, 0);
  product.value.normalizedWeights = product.value.for.map((member, index) => {
    return product.value.price * product.value.weights[index] / totalWeight;
  });
  router.push("/"); // Navigate back to the product list page
}

function cancelEdit() {
  router.push("/"); // Navigate back without saving
}

function deleteProduct() {
  deleteModal.value = false;
  ProductService.deleteProduct(product.value.id);
  router.push("/");
}

const totalContributions = computed(() => {
  return contributions.value.reduce((total, contribution) => total + Number(contribution), 0);
});

watch(multiContribution, (newValue) => {
  if (newValue) {
    // When multiContribution is enabled, set product.price to the sum of contributions
    contributions.value = product.value.by.map(() => product.value.price / product.value.by.length);
    product.value.price = totalContributions.value;
  } else {
    contributions.value = product.value.by.map(() => product.value.price / product.value.by.length);
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
    class="pr-2 fixed bottom-4 left-1/2 z-50 h-16 w-[60%] max-w-lg -translate-x-1/2 rounded-full bg-gray-200 shadow-xl dark:bg-gray-700"
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
          class="group inline-flex h-10 w-10 items-center justify-center rounded-xl shadow-lg bg-gray-300 dark:bg-gray-800 font-medium hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
        >
          ⬅️

        </button>
      </div>

      <div class="flex items-center justify-center">
        <button
          type="button"
          class="group inline-flex h-10 w-10 items-center justify-center rounded-xl shadow-lg bg-gray-300 dark:bg-gray-800 font-medium hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
        >
          💾

        </button>
      </div>


      <div class="flex items-center justify-center">
        <button
          type="button"
          class="group inline-flex h-10 w-10 items-center justify-center rounded-xl shadow-lg bg-gray-300 dark:bg-gray-800 font-medium hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
        >
          ♻️

        </button>
      </div>


    </div>
  </div>

  <div class="px-5 pt-[5rem] pb-32">


    <form class="w-full mx-auto">
      <div class="mb-5">
        <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Expense Name</label>
        <input type="text" id="name" v-model="product.name"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
               :placeholder="expenseName" required />
      </div>
    </form>

    <div class="flex">
      <div class="relative w-full">
        <div class="absolute inset-y-0 start-0 top-0 flex items-center ps-3.5 pointer-events-none">
          <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
               fill="none" viewBox="0 0 20 16">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1M2 5h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm8 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" />
          </svg>
        </div>
        <input v-model="product.price" type="number" id="currency-input"
               class="block p-2.5 w-full z-20 ps-10 text-sm text-gray-900 bg-gray-50 rounded-s-lg border-e-gray-50 border-e-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-e-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
               placeholder="Enter amount" required :disabled="multiContribution"/>
      </div>
      <div
        class="text-gray-900 dark:text-gray-200 px-2 pt-2.5 border-l border-t border-b bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500 dark:focus:border-blue-500">

        <div v-if="!multiContribution">
        <VueInputCalculator enableKeyboard v-model="product.price"
                            number-buttons-bg-color="#0f172a"
                            action-buttons-bg-color="#1e293b"
                            bg-color="#020617"
                            text-color="white"
                            event-buttons-bg-color="#334155"
                            action-success-button-bg-color="#1d4ed8">
          <i class="pi pi-calculator text-xl"></i>
        </VueInputCalculator>
        </div>
        <div v-else>
          <i class="pi pi-lock text-xl text-green-500"></i>
        </div>


      </div>
      <button id="dropdown-currency-button" data-dropdown-toggle="dropdown-currency"
              class="flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-e-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600"
              type="button">
        <svg fill="none" aria-hidden="true" class="h-4 w-4 me-2" viewBox="0 0 20 15">
          <rect width="19.1" height="13.5" x=".25" y=".75" fill="#fff" stroke="#F5F5F5" stroke-width=".5" rx="1.75" />
          <mask id="a" style="mask-type:luminance" width="20" height="15" x="0" y="0" maskUnits="userSpaceOnUse">
            <rect width="19.1" height="13.5" x=".25" y=".75" fill="#fff" stroke="#fff" stroke-width=".5" rx="1.75" />
          </mask>
          <g fill="#FF3131" mask="url(#a)">
            <path d="M14 .5h5.6v14H14z" />
            <path fill-rule="evenodd"
                  d="M0 14.5h5.6V.5H0v14zM11.45 6.784a.307.307 0 01-.518-.277l.268-1.34-.933.466-.467-1.4-.467 1.4-.933-.466.268 1.34a.307.307 0 01-.518.277.307.307 0 00-.434 0l-.25.25-.933-.467L7 7.5l-.231.231a.333.333 0 000 .471l1.164 1.165h1.4l.234 1.4h.466l.234-1.4h1.4l1.164-1.165a.333.333 0 000-.471l-.231-.23.467-.934-.934.466-.25-.25a.307.307 0 00-.433 0z"
                  clip-rule="evenodd" />
          </g>
        </svg>
        CAD
        <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
             viewBox="0 0 10 6">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 4 4 4-4" />
        </svg>
      </button>
      <div id="dropdown-currency"
           class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-36 dark:bg-gray-700">
        <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdown-currency-button">

          <li>
            <button type="button"
                    class="inline-flex w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                    role="menuitem">
              <div class="inline-flex items-center">
                <svg fill="none" aria-hidden="true" class="h-4 w-4 me-2" viewBox="0 0 20 15">
                  <rect width="19.1" height="13.5" x=".25" y=".75" fill="#fff" stroke="#F5F5F5" stroke-width=".5"
                        rx="1.75" />
                  <mask id="a" style="mask-type:luminance" width="20" height="15" x="0" y="0"
                        maskUnits="userSpaceOnUse">
                    <rect width="19.1" height="13.5" x=".25" y=".75" fill="#fff" stroke="#fff" stroke-width=".5"
                          rx="1.75" />
                  </mask>
                  <g fill="#FF3131" mask="url(#a)">
                    <path d="M14 .5h5.6v14H14z" />
                    <path fill-rule="evenodd"
                          d="M0 14.5h5.6V.5H0v14zM11.45 6.784a.307.307 0 01-.518-.277l.268-1.34-.933.466-.467-1.4-.467 1.4-.933-.466.268 1.34a.307.307 0 01-.518.277.307.307 0 00-.434 0l-.25.25-.933-.467L7 7.5l-.231.231a.333.333 0 000 .471l1.164 1.165h1.4l.234 1.4h.466l.234-1.4h1.4l1.164-1.165a.333.333 0 000-.471l-.231-.23.467-.934-.934.466-.25-.25a.307.307 0 00-.433 0z"
                          clip-rule="evenodd" />
                  </g>
                </svg>
                CAD
              </div>
            </button>
          </li>
          <li>
            <button type="button"
                    class="inline-flex w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                    role="menuitem">
              <div class="inline-flex items-center">
                <svg fill="none" aria-hidden="true" class="h-4 w-4 me-2" viewBox="0 0 20 15">
                  <rect width="19.6" height="14" y=".5" fill="#fff" rx="2" />
                  <mask id="a" style="mask-type:luminance" width="20" height="15" x="0" y="0"
                        maskUnits="userSpaceOnUse">
                    <rect width="19.6" height="14" y=".5" fill="#fff" rx="2" />
                  </mask>
                  <g mask="url(#a)">
                    <path fill="#D02F44" fill-rule="evenodd"
                          d="M19.6.5H0v.933h19.6V.5zm0 1.867H0V3.3h19.6v-.933zM0 4.233h19.6v.934H0v-.934zM19.6 6.1H0v.933h19.6V6.1zM0 7.967h19.6V8.9H0v-.933zm19.6 1.866H0v.934h19.6v-.934zM0 11.7h19.6v.933H0V11.7zm19.6 1.867H0v.933h19.6v-.933z"
                          clip-rule="evenodd" />
                    <path fill="#46467F" d="M0 .5h8.4v6.533H0z" />
                    <g filter="url(#filter0_d_343_121520)">
                      <path fill="url(#paint0_linear_343_121520)" fill-rule="evenodd"
                            d="M1.867 1.9a.467.467 0 11-.934 0 .467.467 0 01.934 0zm1.866 0a.467.467 0 11-.933 0 .467.467 0 01.933 0zm1.4.467a.467.467 0 100-.934.467.467 0 000 .934zM7.467 1.9a.467.467 0 11-.934 0 .467.467 0 01.934 0zM2.333 3.3a.467.467 0 100-.933.467.467 0 000 .933zm2.334-.467a.467.467 0 11-.934 0 .467.467 0 01.934 0zm1.4.467a.467.467 0 100-.933.467.467 0 000 .933zm1.4.467a.467.467 0 11-.934 0 .467.467 0 01.934 0zm-2.334.466a.467.467 0 100-.933.467.467 0 000 .933zm-1.4-.466a.467.467 0 11-.933 0 .467.467 0 01.933 0zM1.4 4.233a.467.467 0 100-.933.467.467 0 000 .933zm1.4.467a.467.467 0 11-.933 0 .467.467 0 01.933 0zm1.4.467a.467.467 0 100-.934.467.467 0 000 .934zM6.533 4.7a.467.467 0 11-.933 0 .467.467 0 01.933 0zM7 6.1a.467.467 0 100-.933.467.467 0 000 .933zm-1.4-.467a.467.467 0 11-.933 0 .467.467 0 01.933 0zM3.267 6.1a.467.467 0 100-.933.467.467 0 000 .933zm-1.4-.467a.467.467 0 11-.934 0 .467.467 0 01.934 0z"
                            clip-rule="evenodd" />
                    </g>
                  </g>
                  <defs>
                    <linearGradient id="paint0_linear_343_121520" x1=".933" x2=".933" y1="1.433" y2="6.1"
                                    gradientUnits="userSpaceOnUse">
                      <stop stop-color="#fff" />
                      <stop offset="1" stop-color="#F0F0F0" />
                    </linearGradient>
                    <filter id="filter0_d_343_121520" width="6.533" height="5.667" x=".933" y="1.433"
                            color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse">
                      <feFlood flood-opacity="0" result="BackgroundImageFix" />
                      <feColorMatrix in="SourceAlpha" result="hardAlpha"
                                     values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" />
                      <feOffset dy="1" />
                      <feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.06 0" />
                      <feBlend in2="BackgroundImageFix" result="effect1_dropShadow_343_121520" />
                      <feBlend in="SourceGraphic" in2="effect1_dropShadow_343_121520" result="shape" />
                    </filter>
                  </defs>
                </svg>
                USD
              </div>
            </button>
          </li>
          <li>
            <button type="button"
                    class="inline-flex w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                    role="menuitem">
              <div class="inline-flex items-center">
                <svg fill="none" aria-hidden="true" class="h-4 w-4 me-2" viewBox="0 0 20 15">
                  <rect width="19.6" height="14" y=".5" fill="#fff" rx="2" />
                  <mask id="a" style="mask-type:luminance" width="20" height="15" x="0" y="0"
                        maskUnits="userSpaceOnUse">
                    <rect width="19.6" height="14" y=".5" fill="#fff" rx="2" />
                  </mask>
                  <g mask="url(#a)">
                    <path fill="#043CAE" d="M0 .5h19.6v14H0z" />
                    <path fill="#FFD429" fill-rule="evenodd"
                          d="M9.14 3.493L9.8 3.3l.66.193-.193-.66.193-.66-.66.194-.66-.194.193.66-.193.66zm0 9.334l.66-.194.66.194-.193-.66.193-.66-.66.193-.66-.193.193.66-.193.66zm5.327-4.86l-.66.193L14 7.5l-.193-.66.66.193.66-.193-.194.66.194.66-.66-.193zm-9.994.193l.66-.193.66.193L5.6 7.5l.193-.66-.66.193-.66-.193.194.66-.194.66zm9.369-2.527l-.66.194.193-.66-.194-.66.66.193.66-.193-.193.66.193.66-.66-.194zm-8.743 4.86l.66-.193.66.193-.194-.66.194-.66-.66.194-.66-.194.193.66-.193.66zm7.034-6.568l-.66.193.194-.66-.194-.66.66.194.66-.193-.193.66.193.66-.66-.194zm-5.326 8.276l.66-.193.66.193-.194-.66.194-.66-.66.194-.66-.193.193.66-.193.66zM13.84 10.3l-.66.193.194-.66-.194-.66.66.194.66-.194-.193.66.193.66-.66-.193zM5.1 5.827l.66-.194.66.194-.194-.66.194-.66-.66.193-.66-.193.193.66-.193.66zm7.034 6.181l-.66.193.194-.66-.194-.66.66.194.66-.193-.193.66.193.66-.66-.194zm-5.326-7.89l.66-.193.66.193-.194-.66.194-.66-.66.194-.66-.193.193.66-.193.66z"
                          clip-rule="evenodd" />
                  </g>
                </svg>
                EUR
              </div>
            </button>
          </li>


        </ul>
      </div>
    </div>

    <div class="pt-5">
      <Dropdown editable v-model="product.category" :options="categories" filter placeholder="Select a Category"
                class="w-full" />
    </div>


    <div class="max-w mt-5">

      <Calendar v-model="product.date" showIcon iconDisplay="input" touch-u-i class="w-full"/>

    </div>


    <div class="flex flex-row justify-between mb-5 mt-4 mx-3">


      <div class="flex items-center h-5">
        <input id="remember" type="checkbox" value=""
               v-model="product.isIncome"
               class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
               required />
        <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Income</label>
      </div>

      <div class="flex items-center h-5">
        <input id="remember" type="checkbox" value=""
               v-model="unequalSplit"
               @click="unequalSplit = !unequalSplit"
               class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
               required />
        <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Unequal Split</label>
      </div>

      <div class="flex items-center h-5">
        <input id="remember" type="checkbox" value=""
               v-model="recurringExpense"
               class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
               required />
        <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Recurring</label>
      </div>
    </div>

    <form>
      <label for="membersby" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Paid By</label>

      <MultiSelect id="membersby"
                   v-model="product.by" :options="members"
                   display="chip"
                   placeholder="Select Member(s)"
                   @change="multiContribution = product.by.length > 1"
      />
    </form>

    <form class="pt-3">
      <label for="membersfor" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Split By</label>

      <MultiSelect id="membersfor"
                   v-model="product.for" :options="members"
                   display="chip"
                   placeholder="Select Member(s)"
                   @change="multiContribution = product.by.length > 1"
      />
    </form>


    <div v-if="multiContribution" class="mt-5 rounded-lg border border-gray-300 dark:border-gray-600 py-3 px-2">
    <p class="text-gray-900 dark:text-white text-sm font-semibold">Contribution Amounts</p>
    <div class="pt-2 max-w flex flex-wrap justify-left">
      <div v-for="(member, index) in product.by" class="flex-col px-1">
        <label for="email"
               class="block mb-2 text-sm font-medium text-wrap
               text-gray-900 dark:text-white justify-content-center
               px-2 content-center flex-1 mt-2">
          {{member}}</label>
        <input type="number" v-model="contributions[index]" id="email" class="w-20 flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Amount" required />
      </div>
    </div>
    </div>

    <div v-if="unequalSplit" class="mt-5 rounded-lg border border-gray-300 dark:border-gray-600 py-3 px-2">
      <p class="text-white text-sm font-semibold">Split Weights</p>
      <div class="pt-2 max-w flex flex-wrap">
        <div v-for="(member, index) in product.for" class="flex flex-col px-1">
          <label for="email"
                 class="block mb-2 text-sm font-medium
               text-gray-900 dark:text-white justify-content-center
               px-2 content-center flex-1 mt-2">
            {{member}}</label>
          <input type="number" v-model="product.weights[index]" id="email" class="w-20 flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="0" required />
        </div>
      </div>
    </div>
    <footer ref="unequalSplitRef"></footer>

    <!-- Recurring Expense Options -->
    <div v-if="recurringExpense">
      <hr class="my-5">
      <h2 class="text-white text-left font-bold pb-5">Recurring Expense</h2>
      <div class="field">
        <div class="grid grid-cols-3 items-center">
          <label for="frequency" class="text-white pl-2">Frequency:</label>
          <div class="col-span-2">
            <Dropdown id="frequency" v-model="product.frequency"
                      :options="['Daily', 'Weekly', 'Monthly', 'Yearly']"
                      class="bg-gray-950 w-full"
                      inputClass="text-white p-2 w-full" />
          </div>
        </div>
        <div class="grid grid-cols-3 items-center mt-2">
          <label for="end-date" class="text-white pl-2">End Date:</label>
          <div class="col-span-2 flex items-center">
            <Calendar v-model="product.endDate"
                      placeholder="(Optional)"
                      inputClass="text-white bg-gray-950 p-2 rounded-lg border-gray-950 w-full"
                      id="end-date" />
            <button type="button" @click="product.endDate = null"
                    class="ml-2 text-white bg-red-500 hover:bg-red-600 p-2 rounded-lg transition ease-in-out duration-150">
              Clear
            </button>
          </div>
        </div>
      </div>

    </div>
    <footer ref="recurringRef"></footer>


  </div>
</template>
