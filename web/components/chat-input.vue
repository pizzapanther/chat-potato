<template>
<div class="wrapper">
  <q-input v-model="text" outlined autogrow type="textarea"/>
  <div><q-btn color="primary" icon="mdi-send" @click="send_text()"/></div>
</div>
</template>
<script>
import { ref } from "vue";

export default {
  setup() {
    var text = ref('');

    function send_text() {
      console.log(text.value);
    }

    return {text, send_text};
  }
}
</script>
<style scoped lang="less">
.wrapper {
  display: flex;
  align-items: center;
  padding: 3px;
}

.wrapper > :first-child {
  flex: 1;
  padding-right: 7px;
}
</style>
