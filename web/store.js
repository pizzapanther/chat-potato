import { defineStore } from 'pinia';

import APIWrapper from "@root/api.js";

function display_error(e) {
  console.error(e);
}


const useMainStore = defineStore('main', {
  state: () => {
    return {
      orgs: [
        // {wrapper, name, slug, id, rooms}
      ]
    }
  },
  actions: {
    async init_orgs(server_url) {
      var api = new APIWrapper(server_url);
      try {
        var response = await api.get_orgs();
        response.data.results.forEach((org) => {
          this.orgs.push({
            wrapper: APIWrapper(server_url, org.id),
            name: org.name,
            slug: org.slug,
            id: org.id,
            rooms: []
          });
        });
      }

      catch (e) {
        display_error(e);
      }
    }
  }
});

export default useMainStore;
