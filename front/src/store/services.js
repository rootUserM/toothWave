import axios from '../plugins/axios';
// Actions
const actions = {
    async createService(_, form) {
      try {
        return await axios.post('/services/', form);
      } catch (e) {
        console.log(e)
      }
    },
    async getServicesConsultingRoom(_, id) {
        try {
          return await axios.get('/services/'+id+'/consultingroom/');
        } catch (e) {
          console.log(e)
        }
      }
   
}
export  default actions