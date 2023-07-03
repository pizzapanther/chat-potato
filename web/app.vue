<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="mdi-menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Chat Potato
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-tab v-for="org in mstore.orgs_flat" :label="org.name" />
      </q-tabs>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <ul>
        <li v-for="r in mstore.current_rooms">{{ r.name }}</li>
      </ul>
    </q-drawer>

    <q-page-container>
      <div v-if="mstore.show_login">
        <server-login :server="mstore.show_login"></server-login>
      </div>
      <div v-else>
        <room-viewer></room-viewer>
        <q-separator />
        <chat-input></chat-input>
      </div>
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue';

import useMainStore from '@root/store.js';
import ServerLogin from '@root/components/login.vue'
import ChatInput from '@root/components/chat-input.vue'
import RoomViewer from '@root/components/room-viewer.vue'


export default {
  components: {ServerLogin, ChatInput, RoomViewer},
  setup () {
    const leftDrawerOpen = ref(false);
    const mstore = useMainStore();

    function get_temp_token() {
      let params = new URLSearchParams(location.search);
      return {token: params.get("temp"), server: params.get("server")};
    }

    let params = get_temp_token();
    if (params.token) {
      mstore.login_with_token(params.server, params.token);
    } else {
      mstore.init_orgs('http://localhost:8000');
    }

    return {
      mstore,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      }
    }
  }
}
</script>
