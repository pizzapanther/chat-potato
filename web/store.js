import { defineStore } from 'pinia';

import APIWrapper from "@root/api.js";

function display_error(e) {
  console.error(e);
}


const useMainStore = defineStore('main', {
  state: () => {
    return {
      show_login: null,
      orgs: [
        // {wrapper, name, slug, id, rooms}
      ]
    }
  },
  actions: {
    async login_with_token(server_url, token) {
      var api = new APIWrapper(server_url);
      try {
        var response = await api.get_token(token);
        var index = this.orgs.length;
        this.orgs.push({user: response.data.user});
        this.init_orgs(server_url, index);
      } catch(e) {
        display_error(e);
      }
    },
    async init_orgs(server_url, index) {
      if (!this.orgs[index]) {
        this.show_login = server_url;
        return;
      }

      var api = new APIWrapper(server_url, this.orgs[index].user.jwt);
      try {
        var response = await api.get_orgs();
        response.data.results.forEach((org) => {
          this.orgs[index].wrapper = new APIWrapper(server_url, this.orgs[index].user.jwt);
          this.orgs[index].server_url = server_url;
          this.orgs[index].name = org.name;
          this.orgs[index].slug = org.slug;
          this.orgs[index].id = org.id;
          this.orgs[index].rooms = [];
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
