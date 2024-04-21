<template>
  <div class="px-3 pb-32 pt-[5rem]" id="dashboard" role="tabpanel">
    <div
      v-if="isEmpty(members) && loaded"
      class="flex flex-col items-center justify-center"
    >
      <h2
        class="truncate px-8 pt-3 text-center text-2xl font-bold text-gray-900 dark:text-white"
      >
        Welcome to
        <span
          class="bg-gradient-to-r from-sky-400 to-emerald-600 bg-clip-text font-mono text-transparent"
          >{{ route.params.ledgerId }}</span
        ><br /><span class="text-base">Add some members to get started</span>
      </h2>
      <img
        class="my-8 max-w-xs object-contain"
        src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f304/512.gif"
        alt="🌄"
      />
    </div>
    <div class="relative">
      <div
        class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3"
      >
        <svg
          class="h-4 w-4 text-gray-500 dark:text-gray-400"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"
          />
        </svg>
      </div>
      <input
        type="text"
        v-model="newMember"
        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
        placeholder="Add new member"
        required
      />
      <button
        v-if="!newMemberDisabled"
        @click="addMember(newMember)"
        class="absolute bottom-2.5 end-2.5 rounded-lg bg-blue-700 px-4 py-2 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <i class="pi pi-plus"></i>
      </button>
    </div>

    <div
      v-for="(member, index) in Object.entries(members)"
      class="my-3 rounded-lg bg-gray-100 p-4 dark:bg-gray-800"
    >
      <div class="flex flex-row justify-between">
        <div>
          <h2
            class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
          >
            {{ member[0] }}
          </h2>
          <p
            class="mt-1 font-normal tracking-tight text-gray-700 dark:text-gray-400"
          >
            {{ getMemberOwingString(member[1]) }}
          </p>
        </div>

        <div>
          <button
            @click="openEditMemberDialog(member[0])"
            class="rounded-lg bg-gray-200 p-2 shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-gray-700 dark:text-white dark:hover:bg-blue-600"
          >
            <svg
              class="h-6 w-6 text-gray-800 dark:text-white"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="square"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 19H5a1 1 0 0 1-1-1v-1a3 3 0 0 1 3-3h1m4-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm7.441 1.559a1.907 1.907 0 0 1 0 2.698l-6.069 6.069L10 19l.674-3.372 6.07-6.07a1.907 1.907 0 0 1 2.697 0Z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div v-if="!isEmpty(members)" class="flex justify-center">
      <button
        @click="openArchiveDialog"
        class="inline-flex items-center rounded-lg bg-red-600 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 dark:focus:ring-red-800"
        type="button"
      >
        <i class="pi pi-trash mr-2"></i>
        Archive Member
      </button>
    </div>

    <div class="flex justify-center">
      <Dialog
        v-model:visible="visible"
        modal
        header="Header"
        :style="{ width: '50rem' }"
      >
        <template #container="{ closeCallback }">
          <div class="p-4">
            <div class="relative rounded-lg bg-white shadow dark:bg-gray-700">
              <button
                @click="visible = false"
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
                <svg
                  class="mx-auto mb-4 h-12 w-12 text-gray-400 dark:text-gray-200"
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
                    d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                  />
                </svg>
                <h3
                  class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400"
                >
                  Enter member name to delete
                </h3>
                <p
                  v-if="memberHasBalance"
                  class="hyphens-auto text-wrap pb-3 text-sm text-red-600"
                >
                  <span class="font-bold">{{ memberToDelete }}</span> has an
                  outstanding balance.
                </p>
                <div class="relative">
                  <div
                    class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3"
                  >
                    <svg
                      class="h-4 w-4 text-gray-500 dark:text-gray-400"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"
                      />
                    </svg>
                  </div>

                  <input
                    type="text"
                    v-model="memberToDelete"
                    :class="{ 'font-bold': !deleteButtonDisabled }"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                    required
                  />
                  <button
                    type="submit"
                    v-if="!deleteButtonDisabled"
                    @click="deleteMember(memberToDelete)"
                    :class="{
                      'bg-red-600 hover:bg-red-700': !deleteButtonDisabled,
                      'bg-red-400': deleteButtonDisabled,
                    }"
                    class="absolute bottom-2.5 end-2.5 rounded-lg px-4 py-2 text-sm font-medium text-white"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Dialog>
    </div>

    <div class="flex justify-center">
      <Dialog
        v-model:visible="editMemberVisible"
        modal
        header="Header"
        :style="{ width: '50rem' }"
      >
        <template #container="{ closeCallback }">
          <div class="p-4">
            <div class="relative rounded-lg bg-white shadow dark:bg-gray-700">
              <button
                @click="editMemberVisible = false"
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
                <svg
                  class="mx-auto mb-4 h-12 w-12 text-gray-400 dark:text-gray-200"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="square"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 19H5a1 1 0 0 1-1-1v-1a3 3 0 0 1 3-3h1m4-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm7.441 1.559a1.907 1.907 0 0 1 0 2.698l-6.069 6.069L10 19l.674-3.372 6.07-6.07a1.907 1.907 0 0 1 2.697 0Z"
                  />
                </svg>
                <h3
                  class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400"
                >
                  Edit name for member
                  <span class="font-bold">{{ editMemberName }}</span>
                </h3>
                <div class="relative">
                  <div
                    class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3"
                  >
                    <svg
                      class="h-4 w-4 text-gray-500 dark:text-gray-400"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"
                      />
                    </svg>
                  </div>

                  <input
                    type="text"
                    v-model="editMemberNewName"
                    :class="{ 'font-bold': editMemberNameValid }"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-4 ps-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                    required
                  />
                  <button
                    type="submit"
                    v-if="editMemberNameValid"
                    @click="editMember(editMemberName, editMemberNewName)"
                    :class="{
                      'bg-green-600 hover:bg-green-700': editMemberNameValid,
                      'bg-green-400': editMemberNameValid,
                    }"
                    class="absolute bottom-2.5 end-2.5 rounded-lg px-4 py-2 text-sm font-medium text-white"
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
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Dialog from "primevue/dialog";
import { XPNZService } from "../service/XPNZService.js";
import { useRoute } from "vue-router";

const memberToDelete = ref("");
const newMember = ref("");
const editMemberVisible = ref(false);

const editMemberName = ref("");
const editMemberNewName = ref("");
const editMemberNameValid = ref(false);

watch(editMemberNewName, () => {
  // check if new member is not empty and does not exist in members
  editMemberNameValid.value = !(
    editMemberNewName.value === "" ||
    members.value[editMemberNewName.value] !== undefined
  );
});

function openArchiveDialog() {
  memberToDelete.value = "";
  visible.value = true;
}

const newMemberDisabled = ref(true);
const memberHasBalance = ref(false);
const deleteButtonDisabled = ref(true);
const route = useRoute();

function openEditMemberDialog(name) {
  editMemberName.value = name;
  editMemberNewName.value = "";
  editMemberVisible.value = true;
}

watch(newMember, () => {
  // check if new member is not empty and does not exist in members
  newMemberDisabled.value =
    newMember.value === "" || members.value[newMember.value] !== undefined;
});

function editMember(oldName, newName) {
  // if oldName exists and newName does not exist then rename the member
  // if oldName does not exist then show error message
  // if newName exists then show error message
  if (
    members.value[oldName] !== undefined &&
    members.value[newName] === undefined
  ) {
    members.value[newName] = members.value[oldName];
    delete members.value[oldName];
    editMemberVisible.value = false;
    editMemberName.value = "";
    editMemberNewName.value = "";
  }
}

const members = ref({});
const visible = ref(false);

function getMemberOwingString(balance) {
  if (balance > 0) {
    return "↑ $" + balance;
  } else if (balance < 0) {
    return "↓ $" + Math.abs(balance);
  } else {
    return "✓ settled up";
  }
}

watch(memberToDelete, () => {
  // if member exists and has a balance set
  // if member does not exist then show error message invalidMember.value = true;
  if (members.value[memberToDelete.value] !== undefined) {
    if (members.value[memberToDelete.value] !== 0) {
      memberHasBalance.value = true;
      deleteButtonDisabled.value = true;
    } else {
      memberHasBalance.value = false;
      deleteButtonDisabled.value = false;
    }
  } else {
    memberHasBalance.value = false;
    deleteButtonDisabled.value = true;
  }
});

function deleteMember(name) {
  // if member name exists and has 0 balance then delete and close the dialog
  // if member exists and has a balance then show error message
  // if member does not exist then show error message
  if (members.value[name] === undefined) {
    memberHasBalance.value = true;
  } else if (members.value[name] === 0) {
    delete members.value[name];
    visible.value = false;
    XPNZService.archiveMember(name);
  } else {
    memberHasBalance.value = true;
  }
}

function addMember(name) {
  // if member name does not exist then add member
  // if member name exists then show error message
  if (members.value[name] === undefined) {
    members.value[name] = 0;
    newMember.value = "";
    console.log(XPNZService.addMember(route.params.ledgerId, name));
  }
}

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}
const loaded = ref(false);
onMounted(async () => {
  const ledgerID = route.params.ledgerId;
  members.value = await XPNZService.getBalances(ledgerID);
  loaded.value = true;
});
</script>
