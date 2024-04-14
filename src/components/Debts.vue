<template>
  <div class="px-3 pt-[4rem]" id="dashboard" role="tabpanel">
    <div
      v-for="(member, index) in members"
      :key="index"
      class="my-3 rounded-lg bg-gray-100 p-4 dark:bg-gray-800"
    >
      <div class="flex flex-row justify-between">
        <div>
          <h2
            class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
          >
            {{ member }} → {{ members[(index + 1) % members.length] }}

          </h2>
          <p
            class="mt-1 font-normal tracking-tight text-gray-700 dark:text-gray-400"
          >
            ${{ Math.floor(Math.random() * 1000) + 1 }}
          </p>
        </div>

        <div>
          <button
            class="rounded-lg p-2 shadow-lg bg-gray-200 dark:bg-gray-700 dark:text-white hover:text-blue-500"
          >
            <div class="flex">
              
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
                  d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
              </svg>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
const members = ref(["tom", "jerry", "spike", "tyke"]);
</script>
