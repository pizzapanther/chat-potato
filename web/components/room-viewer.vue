<template>
<div>
  <div v-for="group in mstore.grouped_messages">
    <div>
      <strong>{{ group[0].topic }}</strong>
    </div>
    <div v-for="(msg, i) in group" :key="msg.id">
      <div>
        {{ msg.text }}
      </div>
    </div>
  </div>
</div>
</template>
<script>
import useMainStore from '@root/store/index.js';

export default {
  setup() {
    const mstore = useMainStore();
    return {mstore};
  }
}
</script>
