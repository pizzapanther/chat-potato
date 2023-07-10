<template>
  <ul>
    <li v-for="r in mstore.current_rooms">
      {{ r.name }}
      <ul>
        <li v-for="t in r.topics">
          {{ t.name }}
        </li>
      </ul>
    </li>
  </ul>
</template>
<script>
import useMainStore from '@root/store.js';

export default {
  setup() {
    const mstore = useMainStore();
    return {mstore};
  }
};
</script>
