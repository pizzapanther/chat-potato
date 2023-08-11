<template>
<div>
  <div>
    <div v-if="mstore.current_room">
      {{ mstore.current_room.name }} &gt;
      <span v-if="mstore.current_topic">
        <q-input v-model="topic" outlined dense hide-bottom-space/>
      </span>
      <span v-else>No Topic Selected</span>
    </div>
    <div v-else>No Room Selected</div>
  </div>
  <div class="wrapper">
    <q-input ref="input" v-model="text" outlined autogrow type="textarea" @keyup.ctrl.enter="send_text" :disable="sending"/>
    <div><q-btn color="primary" icon="mdi-send" @click="send_text()" :disable="sending"/></div>
  </div>
</div>
</template>
<script>
import { ref } from "vue";
import useMainStore from '@root/store/index.js';

export default {
  setup() {
    var text = ref('');
    var input = ref(null);
    var sending = ref(false);
    var topic = ref('');
    const mstore = useMainStore();

    function send_text() {
      if (!sending.value) {
        sending.value = true;
        mstore.send_chat(text.value)
          .then((response) => {
            sending.value = false;
            text.value = '';
            setTimeout(() => {
              input.value.focus();
            }, 10);
          })
          .catch((e) => {
            console.error(e);
            sending.value = false;
            alert('Error sending message');
          });
      }
    }

    return {text, topic, input, send_text, mstore, sending};
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
