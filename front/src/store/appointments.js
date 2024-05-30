import axios from '../plugins/axios';
// Actions
const actions = {
    //Obtener todos los pagos
    async createAppointment(_,form) {
      try {
        return await axios.post('/appointment/createappointment/',form);
      } catch (e) {
        console.log(e)
      }
    },
    async createAppointmentPrivate(_,form){
      try {
        return await axios.post('/appointment/',form);
      } catch (e) {
        console.log(e)
      }
    },
    async getAppointments() {
      try {
        return await axios.get('/appointment');
      } catch (e) {
        console.log(e)
      }
    },
    async getAppointmentsPerUser(_,id) {
      try {
        return await axios.get('/appointment/'+id+'/patient/');
      } catch (e) {
        console.log(e)
      }
    },
    async getAppointmentsPerConsultingRoom(_,id) {
      try {
        return await axios.get('/appointment/'+id+'/consultingroom/');
      } catch (e) {
        console.log(e)
      }
    },
}
export  default actions