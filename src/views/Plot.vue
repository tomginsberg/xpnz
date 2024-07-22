<script setup>
import TopBar from "../components/TopBar.vue";
import Toolbar from "../components/MainToolbar.vue";
import Plot from "../components/Plot.vue";
import { ref } from "vue";

const searchTerm = ref("");
</script>

<template>
  <TopBar :pageID="3" v-model="searchTerm" />
  <Toolbar :pageID="0" />
  <Plot/>
</template>

<style scoped></style>
