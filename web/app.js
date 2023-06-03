import { createApp } from "vue";
import { Quasar } from "quasar";

import "@mdi/font/css/materialdesignicons.min.css";
import "quasar/dist/quasar.css";

import App from "@root/app.vue";


__VUE_OPTIONS_API__ = true;

if (process.env.NODE_ENV !== 'production') {
  __VUE_PROD_DEVTOOLS__ = true;
} else {
  __VUE_PROD_DEVTOOLS__ = false;
}


const app = createApp({
  components: {App},
  setup () {
    return {}
  }
});

app.use(Quasar);
app.mount('#q-app');
