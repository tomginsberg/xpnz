import { createRouter, createWebHistory } from "vue-router";
import ProductEdit from "./views/ProductEdit.vue";
import ProductView from "./views/Main.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component:
      ProductView,
      meta: { depth: 1 }},
    { path: "/edit/:productId",
      component: ProductEdit,
      meta: { depth: 2 } },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      // If savedPosition is available, use it
      // This is usually the case when navigating back/forward
      return savedPosition;
    } else {
      // Scroll to top for new navigation or when the savedPosition is not available
      return { top: 0 };
    }
  },
});
