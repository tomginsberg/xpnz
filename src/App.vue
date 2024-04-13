<script setup>
import { onMounted, ref, watch } from "vue";
import { useRoute } from 'vue-router';

import { initFlowbite } from "flowbite";
onMounted(() => {
  initFlowbite();
});

const currentRoute = useRoute();
const transitionName = ref('forward');

    watch(currentRoute, (to, from) => {
      // Directly set the transition based on the path
      if (to.path === '/') {
        // If going back to the root path from an edit path
        transitionName.value = 'slide-left';
      } else if (to.path.includes('/edit/')) {
        // If navigating to an edit path from the root
        transitionName.value = 'slide-right';
      } else {
        // For other cases, you might want to handle differently or keep a default transition
        // This is optional and can be adjusted based on your navigation structure
        // For instance, you might want to check if to.path and from.path are the same or not
        transitionName.value = 'no-transition'; // Example default case, no movement
      }
    });
</script>

<template>
  <div>
    <!-- router view for default and edit, with transition -->
    <router-view v-slot="{ Component }">
      
        <component :is="Component" :key="$route.fullPath"/>
      
    </router-view>
  </div>
</template>

<style>
/* Slide-left transition */
.slide-left-enter-active, .slide-left-leave-active {
  transition: transform 0.35s ease;
}

.slide-left-enter, .slide-left-leave-to /* .slide-left-leave-active in <2.1.8 */
{
  transform: translateX(100%);
}

/* Slide-right transition */
.slide-right-enter-active, .slide-right-leave-active {
  transition: transform 0.35s ease;
}

.slide-right-enter, .slide-right-leave-to /* .slide-right-leave-active in <2.1.8 */
{
  transform: translateX(-100%);
}

</style>