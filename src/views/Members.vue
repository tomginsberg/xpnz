<script setup>
import TopBar from "../components/TopBar.vue";
import Toolbar from "../components/MainToolbar.vue";
import MembersComponent from "../components/Members.vue";
</script>

<template>
  <TopBar :pageID="1" />
  <Toolbar :pageID="1" />
  <MembersComponent />
</template>

<style scoped></style>
