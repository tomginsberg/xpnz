<template>
  <div class="px-3 pt-[4rem] pb-32" id="dashboard" role="tabpanel">
    <div id="alert-1" class="mt-4 flex items-center p-4 mb-3 text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400" role="alert">
      <svg class="flex-shrink-0 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
      </svg>
      <span class="sr-only">Info</span>
      <div class="ms-3 text-sm font-medium">
        A simple info alert with an <a href="#" class="font-semibold underline hover:no-underline">example link</a>. Give it a click if you like.
      </div>
      <button type="button" class="ms-auto -mx-1.5 -my-1.5 bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex items-center justify-center h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700" data-dismiss-target="#alert-1" aria-label="Close">
        <span class="sr-only">Close</span>
        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
        </svg>
      </button>
    </div>

    <div
      v-for="(member, index) in debts"
      :key="index"
      class="my-3 rounded-lg bg-gray-100 p-4 dark:bg-gray-800"
    >
      <div class="flex flex-row justify-between">
        <div>
          <h2
            class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
          >
            {{ member[0] }} → {{ member[1] }}

          </h2>
          <p
            class="mt-1 font-normal tracking-tight text-gray-700 dark:text-gray-400"
          >
            ${{ member[2] }}
          </p>
        </div>

        <div>
          <button
            @click="openSettleDialog(member[0], member[1], member[2])"
            class="rounded-lg p-2 dark:text-white shadow-lg bg-gray-200 dark:bg-gray-700 hover:bg-blue-500 dark:hover:bg-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-300"
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

  <div class="flex justify-center">
    <Dialog v-model:visible="settleVisible" modal header="Header" :style="{ width: '50rem' }">
      <template #container="{ closeCallback }">
        <div class="p-4">
          <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
            <button @click="settleVisible = false"
                    type="button"
                    class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
              <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 14 14">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
              </svg>
            </button>
            <div class="p-4 md:p-5 text-center">

              <h2 class="text-2xl font-bold text-gray-900 dark:text-white pb-3">💸 💸 💸</h2>
              <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400 text-wrap hyphens-auto">Settle
                ${{ settleAmount }} from
                <span class="font-bold">{{ settleMemberFrom }}</span> → <span
                  class="font-bold">{{ settleMemberTo }}</span></h3>


              <div class="flex justify-center">
              <button type="submit"
                        @click="settleDebt(settleMemberFrom, settleMemberTo, settleAmount)"
                        class="text-white font-medium rounded-lg text-sm px-4 py-2 bg-green-500 hover:bg-green-600">
                  <i class="pi pi-check"></i>
                </button>
              </div>

            </div>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Dialog from "primevue/dialog";
import { ProductService } from "../service/ProductService.js";
import { initFlowbite } from "flowbite";

onMounted(() => {
  initFlowbite();
});

const settleVisible = ref(false);
const settleMemberFrom = ref("");
const settleMemberTo = ref("");
const settleAmount = ref(0);

function openSettleDialog(memberFrom, memberTo, amount) {
  settleMemberFrom.value = memberFrom;
  settleMemberTo.value = memberTo;
  settleVisible.value = true;
  settleAmount.value = amount;
}

function settleDebt(memberFrom, memberTo, amount) {
  settleVisible.value = false;
  console.log(`Settling $${amount} from ${memberFrom} to ${memberTo}`);
  // delete [memberFrom, memberTo, amount] from debts
  debts.value = debts.value.filter(
    (debt) =>
      debt[0] !== memberFrom || debt[1] !== memberTo || debt[2] !== amount
  );
  ProductService.settleDebt(memberFrom, memberTo, amount);
}

const debts = ref([
    ["tom", "jerry", 22],
    ["jerry", "spike", 33],
    ["spike", "tyke", 44],
    ["tom", "tyke", 55]
  ]
);
</script>
