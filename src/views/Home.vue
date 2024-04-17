<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import DarkMode from "../components/DarkMode.vue";

const router = useRouter();
const ledger = ref("");

function goToLedger() {
  router.push(`/${ledger.value}`);
}
</script>

<template>
  <div class="flex h-screen items-center justify-center">
    <section
      class="bg-white bg-[url('https://flowbite.s3.amazonaws.com/docs/jumbotron/hero-pattern.svg')] dark:bg-gray-900 dark:bg-[url('https://flowbite.s3.amazonaws.com/docs/jumbotron/hero-pattern-dark.svg')]"
    >
      <img
        src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4b8/512.gif"
        alt="money-wings"
      />
      <div
        class="relative z-10 mx-auto max-w-screen-xl px-4 py-8 text-center lg:py-16"
      >
        <h1
          class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white md:text-5xl lg:text-6xl"
        >
          xpnz
        </h1>
        <form class="mx-auto w-[80%]">
          <label
            for="default-search"
            class="mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Find your ledger</label
          >
          <div class="relative mt-4">
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
              v-model="ledger"
              id="default-search"
              class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-transparent dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
              placeholder="ledger name ..."
              required
            />
            <button
              @click="goToLedger"
              type="submit"
              class="absolute bottom-2.5 end-2.5 rounded-lg bg-blue-700 px-4 py-2 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Go
            </button>
          </div>
        </form>
      </div>
      <div
        class="absolute left-0 top-0 z-0 h-full w-full bg-gradient-to-b from-blue-50 to-transparent dark:from-blue-900"
      ></div>
      <div class="absolute right-2 top-1 z-10">
        <DarkMode />
      </div>
    </section>
  </div>
</template>

<style scoped></style>
