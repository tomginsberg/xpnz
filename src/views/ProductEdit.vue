<template>
  <div>
    <Dialog v-model:visible="deleteModal" header="Confirm Delete" modal :style="{ width: '25rem' }"
            :pt="{
        root: 'border-none',
        mask: {
            style: 'backdrop-filter: blur(2px)'
        }
    }">
      <div class="text-center">
        <svg class="mx-auto mb-4 text-gray-200 w-12 h-12" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
             fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
        </svg>
        <h3 class="mb-5 text-lg font-normal text-gray-400">Are you sure you want to delete this expense?</h3>

        <div class="flex justify-content-center gap-2">
          <Button type="button" label="Yes" severity="secondary" @click="deleteProduct"
                  class="text-white bg-red-600 hover:bg-red-800
                focus:ring-4 focus:outline-none focus:ring-red-300
                dark:focus:ring-red-800 font-medium rounded-lg
                text-sm inline-flex items-center px-5 py-2.5 text-center"></Button>
          <Button type="button" label="Cancel" @click="deleteModal = false"
                  class="py-2.5 px-3 ms-3 text-sm font-medium
                        text-gray-400 focus:outline-none bg-gray-800 rounded-lg
                        border border-gray-600 hover:bg-gray-100 hover:text-white
                        focus:z-10 focus:ring-4 focus:ring-gray-700
                         "></Button>
        </div>
      </div>
    </Dialog>

    <Dialog v-model:visible="openCategoryModal" header="Add New Category" modal :style="{ width: '25rem' }">
      <div class="text-center">
        <InputText type="text" v-model="newCategory" class="bg-gray-950 rounded-lg text-white mb-3"
                   placeholder="New Category"/>
        <div class="flex justify-content-center gap-2">
          <Button type="button" label="Add" icon="pi pi-plus" @click="addCategory"
                  class="text-white bg-gray-950 font-medium rounded-lg border border-green-700
                text-sm inline-flex items-center px-5 py-2.5 text-center"></Button>
          <Button type="button" label="Cancel" icon="pi pi-times" @click="openCategoryModal = false"
                  class="text-white bg-gray-950 font-medium rounded-lg border border-red-700
                text-sm inline-flex items-center px-4 py-2.5 text-center"></Button>
        </div>
      </div>
    </Dialog>

    <div class="fixed bottom-0 left-0 w-full z-10 shadow-lg">
      <div class="bg-black flex justify-between items-center py-6 px-6 text-white">
        <div class="flex-1 flex justify-center items-center relative">
          <div class="absolute right-0 top-1/4 h-1/2 w-px bg-gray-400"></div>
          <Button label="Back" icon="pi pi-chevron-left" severity="success" @click="cancelEdit"/>
        </div>
        <div class="flex-1 flex justify-center items-center relative">
          <div v-if="!isNew" class="absolute right-0 top-1/4 h-1/2 w-px bg-gray-400"></div>
          <Button label="Save" icon="pi pi-save" severity="success" @click="saveProduct"/>
        </div>
        <div v-if="!isNew" class="flex-1 flex justify-center items-center">
          <Button label="Delete" icon="pi pi-trash" severity="success" @click="deleteModal = true"
          />
        </div>
      </div>
    </div>
    <div class="pb-24 p-fluid m-5 bg-gray-900">
      <h2 class="text-white text-center text-3xl font-bold pb-3">{{ product.id === 'new' ? 'New' : 'Edit' }}
        {{product.expenseType === 'Income' ? 'Income' : 'Expense'}}</h2>

      <!-- title -->
      <div class="field">
        <label for="name" class="text-white">Title</label>
        <div class="flex items-center bg-gray-950 rounded-lg">
        <InputText id="name" v-model.trim="product.name" class="bg-gray-950 p-3 text-white"
                   :class="{ 'p-invalid': submitted && !product.name }" placeholder="Expense"/>
<!--          <! expense type e.g. Expense or Income >-->
        <div>
          <Dropdown id="typeDropdown" :options="expenseTypes" v-model="product.expenseType"
                    placeholder="Type" class="flex-grow bg-gray-950"
                    inputClass="w-full bg-gray-950 text-white rounded-lg border-0 p-3"/>
          </div>
        </div>
        <small class="p-error" v-if="submitted && !product.name">Title is required.</small>
      </div>

      <!-- date picker -->
      <div class="field">
        <label for="date" class="text-white">Date</label>
        <Calendar id="date" v-model="product.date"
                  inputClass="text-white bg-gray-950 p-3 rounded-lg border-gray-950"/>
      </div>

      <!-- category dropdown -->
      <div class="field">
        <label for="categoryDropdown" class="block mb-2">Category</label>
        <div class="flex items-center bg-gray-950 rounded-lg">
          <Dropdown ref="categoryDropdownRef" id="categoryDropdown" v-model="product.category" :options="categories"
                    filter
                    placeholder="Select a Category" class="flex-grow bg-gray-950"
                    inputClass="w-full bg-gray-950 text-white rounded-lg border-0 p-3"/>
          <Button class="bg-gray-950 text-white font-bold rounded p-4 h-8"
                  icon="pi pi-plus" @click="openCategoryModal = true" style="width: 2.25rem; height: 2.25rem;"/>
        </div>
      </div>

      <!-- price -->
      <div class="field flex items-center space-x-4">
        <div class="flex-1">
          <label for="price" class="block text-white mb-2">Price</label>
          <div class="relative flex items-center bg-gray-950 rounded-lg p-2">

            <div v-if="!multiContribution">
            <VueInputCalculator enableKeyboard v-model="product.price" auto-apply
                                number-buttons-bg-color="#0f172a"
                                action-buttons-bg-color="#1e293b"
                                bg-color="#020617"
                                text-color="white"
                                event-buttons-bg-color="#334155"
                                action-success-button-bg-color="#1d4ed8">
              <i class="pi pi-calculator scale-150 ml-2"/>
            </VueInputCalculator>
              </div>
            <div v-else>
              <i class="pi pi-check-circle scale-150 ml-2 text-green-600"/>
            </div>
            <span class="ml-3">$</span>
            <input type="number"
                   v-model="product.price"
                   id="currency-input"
                   class="bg-gray-950 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-0"
                   placeholder="Amount"
                   :disabled="multiContribution">
            <Dropdown id="currency" v-model="product.currency"
                      :options="['CAD', 'USD']"
                      class="bg-gray-950"
                      inputClass="bg-gray-950 text-white p-2"/>
          </div>

        </div>


      </div>


      <hr class="my-5">

      <!-- by members -->
      <div class="field">
        <label for="membersby" class="text-white">By</label>
        <MultiSelect id="membersby" v-model="product.by" :options="members"
                     display="chip"
                     placeholder="Select Member(s)"
                     class="bg-gray-950 p-2"
                     @change="multiContribution = product.by.length > 1"
        />
      </div>

      <!-- for members -->
      <div class="field">
        <label for="membersfor" class="text-white">For</label>
        <MultiSelect id="membersfor" v-model="product.for"
                     :options="members" display="chip"
                     placeholder="Select Member(s)"
                     class="bg-gray-950 p-2"
        />
      </div>

      <!-- contribution amounts -->


      <!-- Unequal Split and Recurring toggles -->
      <div class="flex items-center mt-4">
        <label for="link-checkbox" class="font-medium"><span
            class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Unequal Split</span></label>
        <input v-model="unequalSplit" @change="scrollToUnequalSplit" id="link-checkbox" type="checkbox" value=""
               class="h-4 w-4 ml-3 text-blue-600 bg-gray-700 border-gray-600 rounded-lg focus:ring-0 ring-offset-gray-800">
        <label for="link-checkbox-rec" class="ml-4 font-medium"><span
            class="text-transparent bg-clip-text bg-gradient-to-r to-lime-600 from-indigo-400">Recurring</span></label>
        <input v-model="recurringExpense" @change="scrollToRecurring" id="link-checkbox-red" type="checkbox" value=""
               class="h-4 w-4 ml-3 text-blue-600 bg-gray-700 border-gray-600 rounded-lg focus:ring-0 ring-offset-gray-800">
      </div>

      <div v-if="multiContribution">
        <hr class="my-5">
        <h2 class="text-white text-left font-bold pb-3">Contribution Amounts</h2>
        <div v-for="(member, index) in product.by" class="flex items-center space-x-2">
          <span :class="getColorClass(member)" class="mt-2 p-2 rounded text-white">{{ member }}</span>
          <div class="relative flex items-center bg-gray-950 rounded-lg">
            <VueInputCalculator enableKeyboard v-model="contributions[index]" auto-apply
                                number-buttons-bg-color="#0f172a"
                                action-buttons-bg-color="#1e293b"
                                bg-color="#020617"
                                text-color="white"
                                event-buttons-bg-color="#334155"
                                action-success-button-bg-color="#1d4ed8">
              <i class="pi pi-calculator ml-2"/>
            </VueInputCalculator>
            <span class="ml-3">$</span>
            <input type="number"
                   v-model="contributions[index]"
                   id="currency-input"
                   class="bg-gray-950 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-0"
                   placeholder="Amount">
          </div>
        </div>
      </div>
      <!-- Unequal Split Options -->
      <div v-if="unequalSplit">
        <hr class="my-5">
        <h2 class="text-white text-left font-bold pb-3">Split Weights</h2>
        <div v-for="(member, index) in product.for" class="flex items-center space-x-2">
          <span :class="getColorClass(member)" class="mt-2 p-2 rounded text-white">{{ member }}</span>
          <InputNumber
              :id="'weight-' + member"
              v-model="product.weights[index]"
              mode="decimal"
              placeholder="Weight"
              class="flex-1"
              inputClass="bg-gray-950 text-white p-1"
          />
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
                        inputClass="text-white p-2 w-full"/>
            </div>
          </div>
          <div class="grid grid-cols-3 items-center mt-2">
            <label for="end-date" class="text-white pl-2">End Date:</label>
            <div class="col-span-2 flex items-center">
              <Calendar v-model="product.endDate"
                        placeholder="(Optional)"
                        inputClass="text-white bg-gray-950 p-2 rounded-lg border-gray-950 w-full"
                        id="end-date"/>
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
  </div>
</template>

<script setup>
import {ref, onMounted, nextTick, computed, watch} from 'vue';
import {useRouter, useRoute} from 'vue-router';
import {ProductService} from '../service/ProductService';
import VueInputCalculator from "vue-input-calculator";

import MultiSelect from 'primevue/multiselect';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Dropdown from "primevue/dropdown";
import Button from "primevue/button";
import InputNumber from "primevue/inputnumber";
import Dialog from "primevue/dialog";

const router = useRouter();
const route = useRoute();
const categories = ref([]);
const submitted = ref(false);
const members = ref([]);
const recurringExpense = ref(false);
const multiContribution = ref(false);
const memberColors = ref({
  tom: 'blue',
  rhys: 'red',
  dom: 'green'
});
const unequalSplitRef = ref(null);
const recurringRef = ref(null);
const openCategoryModal = ref(false);
const newCategory = ref('');
const categoryDropdownRef = ref(null);
const product = ref({id: null, name: '', category: '', price: 0});
const isNew = ref(false)
const unequalSplit = ref(false);
const contributions = ref([]);
const deleteModal = ref(false);
const byMembers = ref([]);
const expenseTypes = ['Expense', 'Income'];

function addCategory() {
  product.value.category = newCategory.value;
  categories.value.push(newCategory.value);
  openCategoryModal.value = false;
}

function scrollToUnequalSplit() {
  if (unequalSplit.value) {
    nextTick(() => {
      if (unequalSplitRef.value) {
        unequalSplitRef.value.scrollIntoView({behavior: 'smooth'});
      }
    });
  }
}

function scrollToRecurring() {
  if (recurringExpense.value) {
    nextTick(() => {
      if (recurringRef.value) {
        recurringRef.value.scrollIntoView({behavior: 'smooth'});
      }
    });
  }
}

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
  router.push('/'); // Navigate back to the product list page
}

function cancelEdit() {
  router.push('/'); // Navigate back without saving
}

function deleteProduct() {
  deleteModal.value = false;
  ProductService.deleteProduct(product.value.id);
  router.push('/');
}

const getColorClass = (name) => {
  const color = memberColors.value[name] || 'red';
  return `inline-block text-xs font-medium mr-2 mb-2 px-2.5 py-0.5 rounded-lg bg-${color}-900 text-${color}-200`;
};

// Computed property for last member's contribution
const lastMemberContribution = computed(() => {
  if (contributions.value.length > 1) {
    const sumOfContributions = contributions.value.slice(0, -1).reduce((acc, curr) => acc + curr, 0);
    return product.value.price - sumOfContributions;
  }
  return 0;
});

const totalContributions = computed(() => {
  return contributions.value.reduce((total, contribution) => total + Number(contribution), 0);
});

watch(multiContribution, (newValue) => {
  if (newValue) {
    // When multiContribution is enabled, set product.price to the sum of contributions
    contributions.value = product.value.by.map(() => product.value.price / product.value.by.length);
    product.value.price = totalContributions.value;
  }
  else {
    contributions.value = product.value.by.map(() => product.value.price / product.value.by.length);
  }
});

watch(totalContributions, (newValue) => {
  if (multiContribution.value) {
    product.value.price = newValue;
  }
});


onMounted(async () => {
  const productId = route.params.productId;
  if (productId) {
    const fetchedProduct = await ProductService.getProductById(productId);
    if (productId === 'new') {
      isNew.value = true;
    }
    if (fetchedProduct) {
      product.value = fetchedProduct; // Update the product with fetched data
      unequalSplit.value = fetchedProduct.weights && fetchedProduct.weights.some((weight, index) => weight !== fetchedProduct.weights[0]);
      multiContribution.value = fetchedProduct.by.length > 1;
      contributions.value = fetchedProduct.contributions;
      byMembers.value = fetchedProduct.by;
    } else {
      console.error('Product not found');
      // Handle product not found, e.g., redirect
    }
    categories.value = await ProductService.getCategories();
    members.value = await ProductService.getMembers();
  }
});


</script>
