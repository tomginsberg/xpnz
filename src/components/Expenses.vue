<template>
  <div class="pt-[7.5rem]" id="profile" role="tabpanel">
    <div
      class="my-3 grid w-full grid-flow-dense grid-cols-2 gap-3 px-3 pb-32 md:grid-cols-3 lg:grid-cols-5"
    >
      <div
        v-for="(item, index) in filteredProducts"
        @click="toggleExpansion(index)"
        :key="index"
        :ref="setCardRef(index)"
        class="flex transform cursor-pointer flex-col justify-between text-wrap break-words rounded-lg p-4 text-black transition duration-150 ease-in-out active:scale-95 dark:text-gray-100"
        :class="[(expandedCard[index] || filteredProducts.length === 1) ? 'row-span-2 dark:bg-gray-700 bg-gray-200' : 'bg-gray-100 dark:bg-gray-800',
        // make random cards have row-span-2 or col-span-2 (or both)
        // Math.random() > 0.75 ? 'row-span-2' : '',
        // Math.random() > 0.75 ? 'col-span-2' : ''
      ]"
      >
        <div class="flex-auto">
          <div class="flex flex-row justify-between">
            <h2
              class="basis-3/4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
            >
              {{ item.name }}
            </h2>
            <p
              class="mt-1 font-normal tracking-tight text-gray-700 dark:text-gray-400"
            >
              ${{ item.price }}
            </p>
          </div>
        </div>
        <div>
          <p class="font-normal text-gray-700 dark:text-gray-400">
            #{{ item.category }}
          </p>
          <div class="flex flex-row">
            <p
              class="flex-auto font-normal tracking-tight text-gray-700 dark:text-gray-400"
            >
              {{ item.date.toISOString().split("T")[0] }}
            </p>
            <button
              href="https://google.com"
              class="hover:text-blue-500"
              @click="editTransaction"
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
            Type: <span class="font-bold">{{ item.expenseType }}</span>
          </div>
          <div class="flex w-full flex-wrap">
            <span class="mr-1">Paid:</span>
            <span
              v-for="(member, index) in item.by"
              :key="index"
              :class="getColorClassShort(member)"
              class="text-small mx-1 rounded-lg"
            >
              {{ member }} (${{ item.contributions[index].toFixed(2) }})
            </span>
          </div>
          <div class="flex w-full flex-wrap">
            <span class="mr-1">Split:</span>
            <span
              v-for="(member, index) in item.for"
              :key="index"
              class="text-small mx-1 rounded-lg"
              :class="getColorClassShort(member)"
            >
              {{ member }} (${{ item.normalizedWeights[index].toFixed(2) }})
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, watch, computed, nextTick, reactive } from "vue";
import { ProductService } from "../service/ProductService.js";
import Fuse from "fuse.js";
import { useRouter } from "vue-router";

const router = useRouter();
const products = ref([]);
const expandedCard = ref([]);
const cardRefs = reactive({});

function editTransaction(prod) {
  const scrollPosition = window.scrollY;
  localStorage.setItem("mainPageScrollPosition", scrollPosition.toString());
  router.push(`/edit/${prod.id}`);
}

const searchTerm = inject("searchTerm");
// Fuse.js setup
const options = {
  keys: ["name", "category", "date", "price", "for", "by"],
  includeScore: true,
  ignoreLocation: true,
  threshold: 0.2, // Adjust for more/less strict matching
  isCaseSensitive: false,
};

const fuse = ref(new Fuse([], options));

watch(products, (newValue) => {
  fuse.value = new Fuse(newValue, options);
});

// Computed property for filtered products
const filteredProducts = computed(() => {
  if (!searchTerm.value.trim()) {
    return products.value;
  }
  return fuse.value.search(searchTerm.value).map((result) => result.item);
});

const expandedCardIndex = ref(0);
const memberColors = ref({
  tom: "red",
  rhys: "blue",
  dom: "green",
});

function setCardRef(index) {
  return el => {
    if (el) cardRefs[index] = el;  // Assign the DOM element to the reactive object
  };
}

function toggleExpansion(index) {
  expandedCard.value[index] = !expandedCard.value[index];
  if (expandedCard.value[index]) {
    // Check if card is expanded and scroll it into view
    nextTick(() => {
      const navbarOffset = 125;  // This is your navbar height in pixels, adjust if necessary
      const cardElement = cardRefs[index];
      const cardTop = cardElement.getBoundingClientRect().top;
      const offsetPosition = cardTop + window.pageYOffset - navbarOffset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    });
  }
}
function getColorClass(name) {
  console.log(name);
  const color = memberColors.value[name] || "red";
  console.log(color);
  return `inline-block text-xs font-medium mr-2 mb-2 px-2.5 py-0.5 rounded bg-${color}-900 text-${color}-200`;
}

function getColorClassShort(name) {
  const color = memberColors.value[name] || "red";
  return `bg-${color}-900 text-${color}-200`;
}

const editProduct = (prod) => {
  const scrollPosition = window.scrollY;
  localStorage.setItem("mainPageScrollPosition", scrollPosition.toString());
  router.push(`/edit/${prod.id}`);
};

onMounted(() => {
  ProductService.getProductsData().then((data) => {
    products.value = data;
    expandedCard.value = Array(data.length).fill(false);
    expandedCard[0] = true;
  });
});
</script>