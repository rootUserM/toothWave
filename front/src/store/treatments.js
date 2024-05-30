import axios from '../plugins/axios';
// Actions
const actions = {
    async createTreatment(_, form) {
      try {
        return await axios.post('/treatments/', form);
      } catch (e) {
        console.log(e)
      }
    },
    async getTreatmentsPatient(_, id) {
        try {
          return await axios.get('/treatments/'+id+'/patient/');
        } catch (e) {
          console.log(e)
        }
      },
      async updateTreatmentPatient(_, {id,form}) {
        try {
          return await axios.patch('/treatments/'+id+'/',form);
        } catch (e) {
          console.log(e)
        }
      }
   
}
export  default actions