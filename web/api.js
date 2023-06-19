import axios from "axios";


class APIWrapper {
  constructor(base_url, jwt) {
    this.base_url = base_url;
    this.jwt = jwt;
    if (this.jwt) {
      this.http = axios.create({headers: {Authorization: `Bearer ${this.jwt.token}`}});
    } else {
      this.http = axios.create();
    }
  }

  get_orgs() {
    return this.http.get(`${this.base_url}/api-v1/my-orgs`);
  }

  get_token(temp) {
    return this.http.post(`${this.base_url}/api-v1/get-token`, {token: temp});
  }
}

export default APIWrapper;
