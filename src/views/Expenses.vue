<script setup>
import TopBar from "../components/TopBar.vue";
import Toolbar from "../components/MainToolbar.vue";
import ExpensesComponent from "../components/Expenses.vue";
import { ref } from "vue";

const searchTerm = ref("");
</script>

<template>
  <TopBar :pageID="0" v-model="searchTerm" />
  <Toolbar :pageID="0" />
  <ExpensesComponent :searchTerm="searchTerm" />
</template>

<style scoped></style>
