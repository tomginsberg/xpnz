import { createRouter, createWebHistory } from "vue-router";
import Edit from "./views/Edit.vue";
import Expenses from "./views/Expenses.vue";
import Members from "./views/Members.vue";
import Debts from "./views/Debts.vue";
import Home from "./views/Home.vue";
import Plot from "./views/Plot.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home }, // Redirect to home if no ledgerId is provided
    { path: "/:ledgerId/edit/:productId", component: Edit },
    { path: "/:ledgerId", component: Expenses },
    { path: "/:ledgerId/members", component: Members },
    { path: "/:ledgerId/debts", component: Debts },
    { path: "/:ledgerId/plot", component: Plot },
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
