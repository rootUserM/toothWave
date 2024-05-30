import axios from '../plugins/axios';
// Actions
const actions = {
    async createPatient(_, form) {
      try {
        return await axios.post('/patients/', form);
      } catch (e) {
        console.log(e)
      }
    },
    async getPatients(_,id) {
        try {
          return await axios.get('/patients/'+id+'/consultingroom/');
        } catch (e) {
          console.log(e)
        }
      },
      async getPatient(_,id) {
        try {
          return await axios.get('/patients/'+id);
        } catch (e) {
          console.log(e)
        }
      },
      async editPatient(_,form) {
        try {
          return await axios.put('/patients/'+form.id+'/',form);
        } catch (e) {
          console.log(e)
        }
      },
}
export  default actions