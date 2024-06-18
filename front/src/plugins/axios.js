import axios from "axios";
import router from "@/router";
import store from "@/store";

const instance = axios.create({
  baseURL: "https://citassalud.com.mx/api",
  timeout: 5000,
});

instance.interceptors.request.use(
  (config) => {
    const accessToken = store.state.token;

    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      store.dispatch("logout");
      router.push({ name: "login" });
    }
    return Promise.reject(error);
  }
);

export default instance;
