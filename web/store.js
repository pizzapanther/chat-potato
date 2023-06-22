import { defineStore } from 'pinia';

import APIWrapper from "@root/api.js";

function display_error(e) {
  console.error(e);
}


const useMainStore = defineStore('main', {
  state: () => {
    return {
      show_login: null,
      users: {},
      orgs: {}
    }
  },
  persist: {
    paths: ["users"]
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

          this.orgs[server_url].push({
            wrapper: new APIWrapper(server_url, this.users[server_url].jwt),
            rooms: [],
            ...org
          });
        });
      }

      catch (e) {
        if (e.response && e.response.status >= 400 && e.response.status < 500) {
          this.show_login = server_url;
        } else {
          display_error(e);
        }
      }
    }
  }
});

export default useMainStore;
