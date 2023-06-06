import axios from "axios";


class APIWrapper {
  constructor(base_url, oid) {
    this.base_url = base_url;
    this.oid = oid;
  }

  get_orgs() {
    return axios.get(`${this.base_url}/api-v1/my-orgs`);
  }
}

export default APIWrapper;
