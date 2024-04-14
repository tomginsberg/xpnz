import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import PrimeVue from 'primevue/config';
import { router } from "./router";
import "primeicons/primeicons.css";
import Dropdown from 'primevue/dropdown';
import Panel from "primevue/panel";
import Lara from "./presets/lara";
// import "primevue/resources/themes/aura-dark-indigo/theme.css";

const app = createApp(App);


app.component("Panel", Panel);

app.use(router);
app.use(PrimeVue, {
  unstyled: true,
  pt: Lara
});
app.component('Dropdown', Dropdown);

app.mount("#app");