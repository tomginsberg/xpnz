<template>
  <div class="pt-[7.25rem]" id="profile" role="tabpanel">
    <div v-if="expenses.length === 0 && loaded">
      <h2
        class="px-8 pt-64 text-center text-2xl font-bold text-gray-900 dark:text-white"
      >
        Add an expense to get started<br />↓
      </h2>

      <div class="flex items-center justify-center">
        <button
          @click="newExpense"
          type="button"
          class="pulsing-border group inline-flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 font-medium hover:bg-blue-700 hover:bg-green-500 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
        >
          <svg
            class="h-6 w-6 text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 18 18"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 1v16M1 9h16"
            />
          </svg>
        </button>
      </div>
    </div>

    <div class="fixed right-12 top-4 z-50 p-2" @click="toggleExpansionOnAll">
      <svg
        v-show="!expansionToggle"
        class="h-5 w-5 text-gray-600 dark:text-gray-400"
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
          d="M8 4H4m0 0v4m0-4 5 5m7-5h4m0 0v4m0-4-5 5M8 20H4m0 0v-4m0 4 5-5m7 5h4m0 0v-4m0 4-5-5"
        />
      </svg>
      <svg
        v-show="expansionToggle"
        class="h-5 w-5 text-gray-600 dark:text-gray-400"
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
          d="M5 9h4m0 0V5m0 4L4 4m15 5h-4m0 0V5m0 4 5-5M5 15h4m0 0v4m0-4-5 5m15-5h-4m0 0v4m0-4 5 5"
        />
      </svg>
    </div>

    <div
      class="my-3 grid w-full grid-flow-dense grid-cols-2 gap-3 px-3 pb-32 md:grid-cols-3 lg:grid-cols-5"
    >
      <div
        v-for="(item, index) in filteredProducts"
        @click="toggleExpansion(index)"
        :key="index"
        :ref="setCardRef(index)"
        class="flex transform cursor-pointer flex-col justify-between text-wrap break-words rounded-lg p-4 text-black transition duration-150 ease-in-out active:scale-95 dark:text-gray-100"
        :class="[
          expandedCard[index] || filteredProducts.length === 1
            ? 'col-span-2 row-span-2 bg-gray-200 dark:bg-gray-700'
            : 'bg-gray-100 dark:bg-gray-800',
          isLong(item),
        ]"
      >
        <div class="flex-auto">
          <div class="flex flex-wrap justify-between">
            <h2
              class="mr-3 truncate text-balance text-lg font-bold tracking-tight text-gray-900 dark:text-white"
            >
              {{ getName(item) }}
            </h2>
            <p
              class="mt-[0.1rem] truncate font-normal tracking-tight text-gray-700 dark:text-gray-400"
            >
              {{
                item.converted_total > 0
                  ? "$" + roundToTwoDecimals(item.converted_total)
                  : "+ $" + roundToTwoDecimals(Math.abs(item.converted_total))
              }}
            </p>
          </div>
        </div>
        <div>
          <p
            v-show="getCategory(item) !== ''"
            class="font-normal text-gray-700 dark:text-gray-400"
          >
            {{ getCategory(item) }}
          </p>
          <div class="flex flex-row">
            <p
              class="flex-auto font-normal tracking-tight text-gray-700 dark:text-gray-400"
            >
              {{ item.date.split("T")[0] }}
            </p>
            <button
              href="https://google.com"
              class="hover:text-blue-500"
              @click="editProduct(item)"
            >
              <svg
                class="h-6 w-6"
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
                  d="M10.779 17.779 4.36 19.918 6.5 13.5m4.279 4.279 8.364-8.643a3.027 3.027 0 0 0-2.14-5.165 3.03 3.03 0 0 0-2.14.886L6.5 13.5m4.279 4.279L6.499 13.5m2.14 2.14 6.213-6.504M12.75 7.04 17 11.28"
                />
              </svg>
            </button>
          </div>
        </div>

        <div v-if="expandedCard[index] || filteredProducts.length === 1">
          <hr class="mb-3 mt-3 border-gray-300 dark:border-gray-600" />
          <!-- show item.expenseType -->
          <div class="pb-2">
            Type: <span class="font-bold">{{ item["expense_type"] }}</span>
          </div>
          <div class="flex w-full flex-wrap">
            <span class="mr-1">Paid:</span>
            <span
              v-for="(member, index) in item.by.members"
              :key="index"
              class="text-small mx-1 rounded-lg"
            >
              {{ member }} ({{ currencySymbols[item.currency]
              }}{{
                roundToTwoDecimals(Math.abs(item.by["split_values"][index]))
              }})
            </span>
          </div>
          <div class="flex w-full flex-wrap">
            <span class="mr-1">Split:</span>
            <span
              v-for="(member, index) in item.for.members"
              :key="index"
              class="text-small mx-1 rounded-lg"
            >
              {{ member }} ({{ currencySymbols[item.currency]
              }}{{
                roundToTwoDecimals(Math.abs(item.for["split_values"][index]))
              }})
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  onMounted,
  watch,
  computed,
  nextTick,
  reactive,
  defineProps,
} from "vue";
import { useRoute } from "vue-router";
import { XPNZService } from "../service/XPNZService.js";
import Fuse from "fuse.js";
import { useRouter } from "vue-router";
import Skeleton from "./Skeleton.vue";

const router = useRouter();
const expenses = ref([]);
const expandedCard = ref([]);
const cardRefs = reactive({});
const route = useRoute();

// const searchTerm = inject("searchTerm");
const props = defineProps(["searchTerm"]);
// Fuse.js setup
const options = {
  keys: [
    "name",
    "category",
    "date",
    "for.members",
    "by.members",
    "expense_type",
    "_for",
    "_by",
    "month",
  ],
  includeScore: true,
  ignoreLocation: true,
  threshold: 0.1, // Adjust for more/less strict matching
  isCaseSensitive: false,
  shouldSort: false,
};

const currencySymbols = {
  USD: "US$",
  EUR: "€",
  CAD: "$",
};

const loaded = ref(false);
const fuse = ref(new Fuse([], options));

watch(expenses, (newValue) => {
  fuse.value = new Fuse(newValue, options);
});

// Computed property for filtered products
const filteredProducts = computed(() => {
  if (!props.searchTerm.trim()) {
    return expenses.value;
  }
  return fuse.value.search(props.searchTerm).map((result) => result.item);
});

function setCardRef(index) {
  return (el) => {
    if (el) cardRefs[index] = el; // Assign the DOM element to the reactive object
  };
}

const width = window.innerWidth;

function isLong(item) {
  if (width < 500) {
    // check is name is not null and is longer than 20 characters
    if (item.name) {
      if (item.name.length > 19) {
        return "col-span-2";
      }
    } else if (item.category && item.category.length > 19) {
      return "col-span-2";
    }
  }
}

function getName(item) {
  return item.name ? item.name : item.category;
}

function getCategory(item) {
  // if there is no name make the category ''
  return item.name ? item.category : "";
}

function toggleExpansion(index) {
  expandedCard.value[index] = !expandedCard.value[index];
  if (expandedCard.value[index]) {
    // Check if card is expanded and scroll it into view
    nextTick(() => {
      const navbarOffset = 125; // This is your navbar height in pixels, adjust if necessary
      const cardElement = cardRefs[index];
      const cardTop = cardElement.getBoundingClientRect().top;
      const offsetPosition = cardTop + window.pageYOffset - navbarOffset;

      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    });
  }
}

const expansionToggle = ref(false);

function toggleExpansionOnAll() {
  expansionToggle.value = !expansionToggle.value;
  expandedCard.value = expandedCard.value.map(() => expansionToggle.value);
}

const editProduct = (prod) => {
  const scrollPosition = window.scrollY;
  localStorage.setItem("mainPageScrollPosition", scrollPosition.toString());
  router.push(`${route.params.ledgerId}/edit/${prod.id}`);
};

// useRouter

onMounted(async () => {
  const ledgerID = route.params.ledgerId;
  const data = await XPNZService.getTransactions(ledgerID);
  const members = await XPNZService.getActiveMembers(ledgerID);
  if (members.length === 0) {
    await router.push(`/${ledgerID}/members`);
    return;
  }
  expenses.value = data;
  expenses.value.forEach((item) => {
    item["_for"] = item.for.members.map((mem) => `for-${mem}`);
    item["_by"] = item.by.members.map((mem) => `by-${mem}`);
    item["month"] = formatMonthYear(item.date);
  });

  expandedCard.value = Array(data.length).fill(false);
  loaded.value = true;
  await nextTick(() => {
    const savedPosition = localStorage.getItem("mainPageScrollPosition");
    if (savedPosition) {
      window.scrollTo({ top: parseInt(savedPosition), behavior: "auto" });
      localStorage.removeItem("mainPageScrollPosition");
    }
  });
});

function formatMonthYear(timestamp) {
  const date = new Date(timestamp);
  const options = { month: "long", year: "numeric" };
  return date.toLocaleDateString("en-US", options);
}

function roundToTwoDecimals(num) {
  return Math.round(num * 100) / 100;
}

const newExpense = () => {
  router.push(`/${route.params.ledgerId}/edit/new`);
};
</script>

<style scoped>
@keyframes pulse-border {
  0% {
    box-shadow: 0 0 0 0px rgba(34, 197, 94, 0.75);
  }
  100% {
    box-shadow: 0 0 0 10px rgba(34, 197, 94, 0);
  }
}

.pulsing-border {
  animation: pulse-border 2s infinite;
}
</style>
