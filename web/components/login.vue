<template>
  <div>
    <q-dialog v-model="dstate">
      <q-card>
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Login</div>
          <q-space />
        </q-card-section>
        <q-card-section>
          <q-form @submit="onSubmit">
            <q-input v-model="server_url" outlined/>
            <br>
            <q-btn color="primary" label="Go to Login" type="submit"/>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
<script>
import { ref } from "vue";

export default {
  props: ['server'],
  setup (props) {
    const server_url = ref(`${props.server}`);

    function onSubmit() {
      location.href = `${server_url.value}/account/login/?next=${location.href}`;
    }

    return {
      server_url: server_url,
      dstate: true,
      onSubmit
    }
  }
}
</script>
<style lang="less" scoped>
.q-card {
  width: 300px;
}
</style>
