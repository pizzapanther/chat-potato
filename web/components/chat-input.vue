<template>
<div>
  <div>
    <div v-if="mstore.current_room">
      {{ mstore.current_room.name }} &gt;
      <span v-if="mstore.current_topic">{{ mstore.current_topic.name }}</span>
      <span v-else>No Topic Selected</span>
    </div>
    <div v-else>No Room Selected</div>
  </div>
  <div class="wrapper">
    <q-input v-model="text" outlined autogrow type="textarea" @keyup.ctrl.enter="send_text" :disable="sending"/>
    <div><q-btn color="primary" icon="mdi-send" @click="send_text()" :disable="sending"/></div>
  </div>
</div>
</template>
<script>
import { ref } from "vue";
import useMainStore from '@root/store.js';

export default {
  setup() {
    var text = ref('');
    var sending = ref(false);
    const mstore = useMainStore();

    function send_text() {
      if (!sending.value) {
        sending.value = true;
        console.log('NARF', text.value);
        mstore.send_chat(text.value)
          .then((response) => {
            sending.value = false;
            text.value = '';
          })
          .catch((e) => {
            console.error(e);
            sending.value = false;
            alert('Error sending message');
          });
      }
    }

    return {text, send_text, mstore, sending};
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
