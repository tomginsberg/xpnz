<script setup>
import TopBar from "../components/TopBar.vue";
import Toolbar from "../components/MainToolbar.vue";
import DebtsComponent from "../components/Debts.vue";
</script>

<template>
  <TopBar :pageID="2" />
  <Toolbar :pageID="2" />
  <DebtsComponent />
</template>

<style scoped></style>
