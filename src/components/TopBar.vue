<script setup>
import DarkMode from "./DarkMode.vue";
import {defineProps, defineEmits, ref} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();

function home() {
  router.push(`/`);
}

const tabNames = ["Expenses", "Members", "Debts", "Metrics"];
const tabIcons = ["💸", "🧑‍🤝‍🧑", "💳", "📊"];
const labels = ["Search...", "Filter..."];

const searchTerm = ref("");
defineProps({
  modelValue: String, // modelValue is the conventional name used with v-model
  pageID: Number,
});

const emit = defineEmits(["update:modelValue"]); // Emit this event to update the parent's v-model binding

function updateInput(event) {
  emit("update:modelValue", event.target.value); // Update the bound value on input
}

// provide("searchTerm", searchTerm);
</script>

<template>
  <div
      class="fixed top-0 z-10 w-full border-b border-gray-200 bg-gray-100 p-4 dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="flex flex-row">
      <h1
          class="flex-auto px-1 pt-1 text-lg font-semibold text-gray-800 dark:text-white"
          :class="{ 'pb-3': pageID === 0 || pageID === 3 }"
      >
        <button @click="home">{{ tabIcons[pageID] }}
        </button
        >
        <span class="px-1"/>
        {{ tabNames[pageID] }}
      </h1>
      <div class="z-100">
        <DarkMode/>
      </div>
    </div>
    <form class="max-w" v-if="pageID === 0 || pageID === 3">
      <div class="relative">
        <div
            class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3"
        >
          <svg
              class="h-4 w-4 text-gray-500 dark:text-gray-400"
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
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
            />
          </svg>
        </div>
        <input
            type="search"
            id="default-search"
            class="block w-full rounded-lg border border-gray-300 bg-gray-100 p-2 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            :placeholder="labels[pageID % 2]"
            :value="modelValue"
            @input="updateInput"
            required
        />
      </div>
    </form>
  </div>
</template>

<style scoped></style>
