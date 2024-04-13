<template>
  <div
    class="fixed top-0 z-10 w-full border-b border-gray-200 bg-gray-100 p-4 dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="flex flex-row">
      <h1
        class="flex-auto px-1 pt-1 text-lg font-semibold text-gray-800 dark:text-white"
        :class="{ 'pb-3': home == 0 }"
      >
        {{ tabIcons[home] }}<span class="px-1" />
        {{ tabNames[home] }}
      </h1>
      <div class="z-100">
        <DarkMode />
      </div>
    </div>
    <form class="max-w" v-if="home == 0">
      <label
        for="default-search"
        class="sr-only mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >Search</label
      >
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
          placeholder="Search..."
          v-model="searchTerm"
          required
        />
      </div>
    </form>
  </div>

  <div
    class="pr-2 fixed bottom-4 left-1/2 z-50 h-16 w-[60%] max-w-lg -translate-x-1/2 rounded-full bg-gray-100 shadow-xl dark:bg-gray-700"
  >
    <div
      class="mx-auto grid h-full max-w-lg grid-cols-4"
      id="default-tab"
      role="tablist"
    >
    <div
        id="tooltip-home"
        role="tooltip"
        class="tooltip invisible absolute z-10 inline-block rounded-lg bg-gray-900 px-3 py-2 text-sm font-medium text-white opacity-0 shadow-sm transition-opacity duration-300 dark:bg-gray-700"
      >
        Expenses
        <div class="tooltip-arrow" data-popper-arrow></div>
      </div>
      <div class="flex items-center justify-center">
        <button
          type="button"
          class="group inline-flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-medium hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
        >
          <svg
            class="h-4 w-4 text-white"
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

      <button
        @click="home = 0"
        id="profile-tab"
        type="button"
        role="tab"
        class="group inline-flex flex-col items-center justify-center rounded-s-full px-5"
      >
        <span
          class="p-1 text-2xl"
          :class="{ 'py-2 border-b dark:border-gray-600 border-gray-400': home == 0 }"
          >{{ tabIcons[0] }}</span
        >
      </button>
      

    


      <button
        @click="home = 1"
        type="button"
        class="group inline-flex flex-col items-center justify-center px-5"
      >
        <span
          class="p-1 text-2xl"
          :class="{ 'py-2 border-b dark:border-gray-600 border-gray-400': home == 1 }"
          >{{ tabIcons[1] }}</span
        >
      </button>


      <button
        id="dashboard-tab"
        type="button"
        role="tab"
        @click="home = 2"
        class="group inline-flex flex-col items-center justify-center rounded-e-full px-5"
      >
        <span
          class="p-1 text-2xl"
          :class="{ 'py-2 border-b dark:border-gray-600 border-gray-400': home == 2 }"
          >{{ tabIcons[2] }}</span
        >
      </button>

    </div>
  </div>

  <div id="default-tab-content">
    <div v-show="home == 0">
      <Expenses />
    </div>
    <div v-show="home == 1">
      <Members />
    </div>
    <div v-show="home == 2">
      <Debts />
    </div>
  </div>
</template>

<script setup>
import DarkMode from "../components/DarkMode.vue";
import Expenses from "../components/Expenses.vue";
import Members from "../components/Members.vue";
import Debts from "../components/Debts.vue";
import { ref, provide, onMounted } from "vue";

const tabNames = ["Expenses", "Members", "Debts"];
const tabIcons = ["💸", "🧑‍🤝‍🧑", "💳"];

const home = ref(0);
const searchTerm = ref("");
provide("searchTerm", searchTerm);
</script>
