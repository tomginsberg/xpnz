<template>
  <div class="px-3 pb-32 pt-[4.25rem]" role="tabpanel">
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
              class="rounded-lg bg-gray-200 p-2 shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-700 dark:text-white dark:hover:bg-blue-600"
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
    <!-- Copy debts to clipboard button -->
    <div class="flex w-8">
      <button v-if="loaded"
          @click="copyDebts()"
              class="rounded-lg bg-gray-200 p-3 shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-700 dark:text-white dark:hover:bg-blue-600"
      >
        <svg class="w-5 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
             width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
          <path
              d="M17.5 3a3.5 3.5 0 0 0-3.456 4.06L8.143 9.704a3.5 3.5 0 1 0-.01 4.6l5.91 2.65a3.5 3.5 0 1 0 .863-1.805l-5.94-2.662a3.53 3.53 0 0 0 .002-.961l5.948-2.667A3.5 3.5 0 1 0 17.5 3Z"/>
        </svg>
      </button>
    </div>

    <div
        v-if="debts.length === 0 && loaded"
        class="flex flex-col items-center justify-center"
    >
      <h2
          class="px-8 pt-16 text-center font-mono text-2xl font-bold text-gray-900 dark:text-white"
      >
        Looking good! <br/>No debts to settle.
      </h2>
      <img
          class="my-8 max-w-xs object-contain px-8"
          src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f9a7/512.gif"
          alt="🦧"
      />
    </div>
  </div>

  <div class="flex justify-center">
    <Dialog
        v-model:visible="settleVisible"
        modal
        header="Header"
        :style="{ width: '50rem' }"
    >
      <template #container="{ closeCallback }">
        <div class="p-4">
          <div class="relative rounded-lg bg-white shadow dark:bg-gray-700">
            <button
                @click="settleVisible = false"
                type="button"
                class="absolute end-2.5 top-3 ms-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-transparent text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900 dark:hover:bg-gray-600 dark:hover:text-white"
            >
              <svg
                  class="h-3 w-3"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 14 14"
              >
                <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
              </svg>
            </button>
            <div class="p-4 text-center md:p-5">
              <h2 class="pb-3 text-2xl font-bold text-gray-900 dark:text-white">
                💸 💸 💸
              </h2>
              <h3
                  class="mb-5 hyphens-auto text-wrap text-lg font-normal text-gray-500 dark:text-gray-400"
              >
                Settle ${{ settleAmount }} from
                <span class="font-bold">{{ settleMemberFrom }}</span> →
                <span class="font-bold">{{ settleMemberTo }}</span>
              </h3>

              <div class="flex justify-center">
                <button
                    type="submit"
                    @click="
                    settleDebt(settleMemberFrom, settleMemberTo, settleAmount)
                  "
                    class="rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white hover:bg-green-600"
                >
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
import {onMounted, ref} from "vue";
import Dialog from "primevue/dialog";
import {initFlowbite} from "flowbite";
import {useRoute} from "vue-router";
import {XPNZService} from "../service/XPNZService.js";

const debts = ref([]);
const route = useRoute();
const ledgerID = route.params.ledgerId;
const loaded = ref(false);
onMounted(async () => {
  initFlowbite();
  debts.value = await XPNZService.getDebts(ledgerID);
  loaded.value = true;
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
          debt[0] !== memberFrom || debt[1] !== memberTo || debt[2] !== amount,
  );
  XPNZService.settleDebt({
    ledger: ledgerID.toLowerCase(),
    from: memberFrom,
    to: memberTo,
    amount: amount,
  });
}

async function copyDebts() {
  let text = debts.value
      .map((debt) => `${debt[0]} → ${debt[1]}: $${debt[2]}`)
      .join("\n");
  console.log(text);
  // add workspcae url to the text
  text = `📊 Debts\n\n${text}\n\nsee expenses @ https://xpnz.titanium.ddns.me/${ledgerID}`;
  if (navigator.share){
    await navigator.share({
      text: text
    });
  }
  else if(navigator.clipboard){
    await navigator.clipboard.writeText(text);
  }
  else {
    alert(text);
  }
}
</script>
