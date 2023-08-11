import { defineStore } from 'pinia';

import APIWrapper from "@root/api.js";

function display_error(e) {
  console.error(e);
}


const useMainStore = defineStore('main', {
  state: () => {
    return {
      selected_tab: null,
      selected_room: null,
      selected_topic: null,
      show_login: null,
      users: {},
      orgs: {},
      messages: []
    }
  },
  persist: {
    paths: ["users"]
  },
  getters: {
    grouped_messages(state) {
      var ret = [];
      var tmp = [];
      var prev_topic = null;
      state.messages.forEach((msg) => {
        if (msg.topic != prev_topic) {
          if (tmp.length > 0) {
            ret.push(tmp);
            tmp = [];
          }
        }

        prev_topic = msg.topic;
        tmp.push(msg);
      });

      if (tmp.length > 0) {
        ret.push(tmp);
      }

      return ret;
    },
    orgs_flat(state) {
      var ret = [];

      for (const url in state.orgs) {
        state.orgs[url].forEach((org) => {
          ret.push(org);
        });
      }

      return ret;
    },
    current_org(state) {
      if (state.selected_tab !== null) {
        return state.orgs_flat[state.selected_tab];
      }
    },
    current_rooms(state) {
      if (state.selected_tab !== null) {
        return state.orgs_flat[state.selected_tab].rooms;
      }

      return [];
    },
    current_room(state) {
      if (state.current_rooms.length > 0) {
        return state.current_rooms[state.selected_room];
      }
    },
    current_topic(state) {
      if (state.current_room) {
        return state.current_room.topics[state.selected_topic];
      }
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
      if (this.selected_tab !== null && this.orgs_flat[this.selected_tab].id == org.id) {
        org.rooms = response.data.results;
        org.rooms.forEach((r) => {
          r.topics = [];
        });
        this.selected_room = 0;
        await this.get_topics(org, org.rooms[0]);
      }
    },
    async get_topics(org, room) {
      var api = org.wrapper;
      var response = await api.get_topics(org.id, room.id);
      if (this.selected_tab !== null && this.selected_room !== null) {
        if (this.orgs_flat[this.selected_tab].id == org.id && this.orgs_flat[this.selected_tab].rooms[this.selected_room].id == room.id) {
          this.selected_topic = 0;
          var topics = this.orgs_flat[this.selected_tab].rooms[this.selected_room].topics;
          response.data.results.forEach((t) => {
            topics.push(t);
          });
        }
      }
    },
    async send_chat(message) {
      var org = this.current_org;
      return org.wrapper.send_message(org.id, this.current_room.id, this.current_topic.name, message);
    }
  }
});

export default useMainStore;
