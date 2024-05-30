import axios from '../plugins/axios';
// Actions
const actions = {
    async createPayment(_, form) {
      try {
        return await axios.post('/payments/', form);
      } catch (e) {
        console.log(e)
      }
    },   
    async getPaymentsPerConsultingRoom(_, id) {
      try {
        return await axios.get('/payments/'+id+'/consultingroom/');
      } catch (e) {
        console.log(e)
      }
    },   
}
export  default actions