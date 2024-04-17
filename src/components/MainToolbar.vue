<script setup>
import { defineProps } from "vue";
import { useRouter, useRoute } from "vue-router";

const route = useRoute();
const props = defineProps({
  pageID: Number,
});

const router = useRouter();

const tabIcons = ["💸", "🧑‍🤝‍🧑", "💳"];
const newExpense = () => {
  router.push(`/${route.params.ledgerId}/edit/new`);
};

const toHome = () => {
  router.push(`/${route.params.ledgerId}`);
};
const toMembers = () => {
  router.push(`/${route.params.ledgerId}/members`);
};
const toDebts = () => {
  router.push(`/${route.params.ledgerId}/debts`);
};

function getToolBarIconClass(pageNumber) {
  return {
    "border-b border-gray-400 py-2 dark:border-gray-600":
      props.pageID === pageNumber,
    "p-1 text-2xl": true,
  };
}
</script>

<template>
  <div
    class="fixed bottom-4 left-1/2 z-50 h-16 w-[60%] max-w-lg -translate-x-1/2 rounded-full bg-gray-200 pr-2 shadow-xl dark:bg-gray-700"
  >
    <div
      class="mx-auto grid h-full max-w-lg grid-cols-4"
      id="default-tab"
      role="tablist"
    >
      <div class="flex items-center justify-center">
        <button
          @click="newExpense"
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
        @click="toHome"
        :disabled="pageID === 0"
        id="profile-tab"
        type="button"
        role="tab"
        class="group inline-flex flex-col items-center justify-center rounded-s-full px-5"
      >
        <span class="p-1 text-2xl" :class="getToolBarIconClass(0)">{{
          tabIcons[0]
        }}</span>
      </button>

      <button
        @click="toMembers"
        :disabled="pageID === 1"
        type="button"
        class="group inline-flex flex-col items-center justify-center px-5"
      >
        <span class="p-1 text-2xl" :class="getToolBarIconClass(1)">{{
          tabIcons[1]
        }}</span>
      </button>

      <button
        id="dashboard-tab"
        type="button"
        role="tab"
        @click="toDebts"
        :disabled="pageID === 2"
        class="group inline-flex flex-col items-center justify-center rounded-e-full px-5"
      >
        <span class="p-1 text-2xl" :class="getToolBarIconClass(2)">{{
          tabIcons[2]
        }}</span>
      </button>
    </div>
  </div>
</template>
