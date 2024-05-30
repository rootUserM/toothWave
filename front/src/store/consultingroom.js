import axios from "../plugins/axios";
// Actions
const actions = {
  async getConsultingRoom(_, id) {
    try {
      return await axios.get("/consultingroom/" + id + "/");
    } catch (e) {
      console.log(e);
    }
  },
  async getConsultingRooms() {
    try {
      return await axios.get("/consultingroom");
    } catch (e) {
      console.log(e);
    }
  },
  async createConsultingRoom(_, form) {
    try {
      return await axios.post("/consultingroom/", form);
    } catch (e) {
      console.log(e);
    }
  },
  async editConsultingRoom(_, { id, form }) {
    try {
      return await axios.put("/consultingroom/" + id + "/", form);
    } catch (e) {
      console.log(e);
    }
  },
  async deleteConsultingRoom(_, id) {
    try {
      return await axios.delete("/consultingroom/" + id + "/");
    } catch (e) {
      console.log(e);
    }
  },
  async getConsultingRoomLogo(_, id) {
    try {
      return await axios.get("/consultingroom/" + id + "/logo");
    } catch (e) {
      console.log(e);
    }
  },
};
export default actions;
