import axios from "../plugins/axios";
// Actions
const actions = {
  async createService(_, form) {
    try {
      return await axios.post("/services/", form);
    } catch (e) {
      console.log(e);
    }
  },
  async changeServiceStatus(_, form) {
    try {
      return await axios.put("/services/" + form.id + "/cahngestatus/", form);
    } catch (e) {
      console.log(e);
    }
  },
  async editService(_, form) {
    try {
      return await axios.put("/services/" + form.id + "/", form);
    } catch (e) {
      console.log(e);
    }
  },
  async getServicesAll(_, id) {
    try {
      return await axios.get("/services/" + id + "/all/");
    } catch (e) {
      console.log(e);
    }
  },
  async getServicesConsultingRoom(_, id) {
    try {
      return await axios.get("/services/" + id + "/consultingroom/");
    } catch (e) {
      console.log(e);
    }
  },
};
export default actions;
