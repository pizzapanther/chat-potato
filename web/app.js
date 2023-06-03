import { createApp } from "vue";
import { Quasar } from "quasar";


__VUE_OPTIONS_API__ = true;

if (process.env.NODE_ENV !== 'production') {
  __VUE_PROD_DEVTOOLS__ = true;
} else {
  __VUE_PROD_DEVTOOLS__ = false;
}


const app = createApp({
  setup () {
    return {}
  }
});

app.use(Quasar);
app.mount('#q-app');
