import { defineStore } from 'pinia';

import APIWrapper from "@root/api.js";

function display_error(e) {
  console.error(e);
}


const useMainStore = defineStore('main', {
  state: () => {
    return {
      selected_tab: null,
      show_login: null,
      users: {},
      orgs: {}
    }
  },
  persist: {
    paths: ["users"]
  },
  getters: {
    orgs_flat(state) {
      var ret = [];

      for (const url in state.orgs) {
        state.orgs[url].forEach((org) => {
          ret.push(org);
        });
      }

      return ret;
    },
    current_rooms(state) {
      if (state.selected_tab !== null) {
        return state.orgs_flat[state.selected_tab].rooms;
      }

      return [];
    }
  },
  actions: {
    async login_with_token(server_url, token) {
      var api = new APIWrapper(server_url);
      try {
        var response = await api.get_token(token);
        var index = this.orgs.length;

        this.users[server_url] = response.data.user;
        this.init_orgs(server_url);

        const url = new URL(location);
        url.searchParams.delete("temp");
        url.searchParams.delete("server");
        history.pushState({}, "", url);
      } catch(e) {
        display_error(e);
      }
    },
    async init_orgs(server_url) {
      if (!this.users[server_url]) {
        this.show_login = server_url;
        return;
      }

      var api = new APIWrapper(server_url, this.users[server_url]?.jwt);
      try {
        var response = await api.get_orgs();
        response.data.results.forEach((org) => {
          if (!this.orgs[server_url]) {
            this.orgs[server_url] = [];
          }

          var org_data = {
            wrapper: new APIWrapper(server_url, this.users[server_url].jwt),
            rooms: [],
            ...org
          };

          if (this.selected_tab === null) {
            this.selected_tab = 0;
          } else {
            this.selected_tab = this.orgs_flat.length;
          }
          this.orgs[server_url].push(org_data);
          this.get_rooms(this.orgs[server_url][this.orgs[server_url].length - 1]);
        });
      }

      catch (e) {
        if (e.response && e.response.status >= 400 && e.response.status < 500) {
          this.show_login = server_url;
        } else {
          display_error(e);
        }
      }
    },
    async get_rooms(org) {
      var api = org.wrapper;
      var response = await api.get_my_rooms(org.id);
      org.rooms = response.data.results;
    }
  }
});

export default useMainStore;
