<template>
    <div>
    
      <Nav></Nav>
   
    <v-main class=" " >
      <v-row class="mx-10 my-10" v-if="this.patient.data.Name" justify="center">
        <v-col cols="6">
            <v-row justify="start" class="mb-10 pl-6">
                <h3>Detalle de Paciente</h3>
            </v-row>
            <v-simple-table dense > 
                <tbody>
                    <tr>
                        <td width="200px"><b>Nombre completo</b></td>
                        <td>{{this.patient.data.Name+' '+this.patient.data.Last_name+' '+this.patient.data.Second_last_name}}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Número Telefónico</b></td>
                        <td>{{this.patient.data.PhoneNumber}}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Sexo</b></td>
                        <td>{{this.patient.data.Gender}}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Edad</b></td>
                        <td>{{this.patient.data.Eage}}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Email</b></td>
                        <td>{{this.patient.data.Email}}</td>
                    </tr>
                </tbody>
            </v-simple-table>
        </v-col>
        <v-col cols="6">
            <v-row justify="center" class="my-6">
                <v-avatar color="red">
                    <span class="white--text text-h5">{{ this.patient.data.Name[0]+''+ this.patient.data.Last_name[0]}}</span>
                </v-avatar>
            </v-row>
            <v-row justify="center">

              <v-col> 
                <PxCreate v-if="this.patient.data" 
                :toEdit="true" 
                :patient="this.patient.data"
                @reloadData="init()"
                ></PxCreate>
                </v-col>
                <v-col> 
                    <v-btn class="text-none" @click="createAppointmentDialog = true">
                        Agendar consulta
                    </v-btn>
                </v-col>
                <v-col> 
                    <v-btn class="text-none" @click="treatementDialog = true">
                      Nota de evolucion
                    </v-btn>
                </v-col>
            </v-row>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="6"  class="" >
          <h2 class="mx-3 my-3">Citas</h2>
          <Calendar 
            v-if="this.appointments.data.length"
            :events="this.appointments.data"
            :calendarshow="'month'"
            :showControls="false"
        ></Calendar>
        <div v-else>
            Aún no hay citas agendadas
          </div>
        </v-col>
        <v-col cols="6">
          <h2 class="mx-3 my-3">Tratamientos</h2>
          <v-data-table
            v-if="treatments.length"
            :headers="headers"
            :items="treatments"
            :items-per-page="5"
            class="elevation-1"
          >
          <template v-slot:[`item.note`]="{item }">
          <span v-html="item.note.replace(/\n/g, '<br>').substring(0,50) + '...'">
          </span>
        </template>
          <template v-slot:[`item.payment_info.name_services`]="{item }">
          <span>
            {{ item.payment_info.name_services.join() }}
          </span>
        </template>
        <template v-slot:[`item.id`]="{item }">
          <span>
          <v-btn class="text-none my-2 mx-2" density="compact" icon @click="editTreatment(item)"> 
                  <v-icon dark>
                    mdi-pencil
                  </v-icon>
            </v-btn>
          </span>
        </template>
        </v-data-table>
        <div v-else>
            Aún no hay tratamientos registrados para este Px
          </div>
        </v-col>
        
      </v-row>
    </v-main>
    <!-- Appointment dialog -->
    <create-appointment
    :createAppointmentDialog="createAppointmentDialog"
    :services="this.services"
    :patientName="this.patient.data.Name"
    :id_patient="this.$route.params.id"
    :id_consultingRoom="this.patient.data.id_consultingRoom"
    @sendForm="sendForm"
    @closeDialog="createAppointmentDialog = false"
    ></create-appointment>
    <!-- Edit Treatment dialog -->
   <treatment-edit
   :showDialog="treatementEditDialog"
   :currentData="currentItem"
   :patient="this.patient.data"
   :services="this.services"
    @getTreatments="getTreatments"
    @closeDialog="treatementEditDialog = false"
   >
   </treatment-edit>
   <!-- Create Treatment Dialog -->
   <treatment-create
   :showDialog="treatementDialog"
   :currentData="currentItem"
   :patient="this.patient.data"
   :services="this.services"
   @closeDialog="treatementDialog = false"
   @getTreatments="getTreatments"
   >
   </treatment-create>
   </div>

</template>

<script>
import CreateAppointment from '@/components/AppointmentComp.vue'
import TreatmentCreate from '@/components/TreatementCreate.vue'
import TreatmentEdit from '@/components/TreatmentEdit.vue'
import Nav from '../../components/NavBar.vue'
import Calendar from '../../components/CalendarComp.vue'
import PxCreate from './PxCreate.vue'
import { mapActions } from 'vuex'

export default {
    name:'PxDetail',
    components:{
        Calendar,
        PxCreate,
        Nav,
        TreatmentCreate,
        TreatmentEdit,
        CreateAppointment
    },
    
    data:()=>({
    currentItem:null,
    loading: false,
    treatementDialog:false,
    treatementEditDialog:false,
    createAppointmentDialog:false,
    time: null,
    menu3: false,
    patient:{
        data:{
            id_consultingRoom:null,
            id:'',
        }
    },
   
    treatment_form:{
        id_service:null,
        id_patient:null,
        id_consultingRoom:null,
        date:null,
        note:'',
        payment:0.0
    },
    appointments:{
        data:[]
    },
   
    services:[],
    treatments:[{
      date:'01/05/2023',
      name: 'Limpieza',
      payment_info:{
        name_services:[]
      },
      note:''
    }],
    headers: [
        { text: 'Fecha', value: 'date' },
          {
            text: 'Tratamiento(s)',
            align: 'center',
            sortable: false,
            value: 'payment_info.name_services',
          },
          { text: 'Descripcion', value: 'note' },
          // { text: 'Evidencias', value: 'fat' },
          { text: 'Precio del tratamiento',
          align: 'center',
          value: 'payment_info.total_amount_service' },
          // Precio de servico
          { text: 'A cuenta',
          align: 'center',
          value: 'payment_info.total_paid' },
          // Total de pagos
          { text: 'Faltante',
          align: 'center',
          value: 'payment_info.total_debt' },
          // La resta del total_de_pagos con el precio del servico
          { text: 'Acciones',
          align: 'center',
          value: 'id' },
        ],
    }),
    mounted(){
        this.init()
    },
    methods:{
        ...mapActions(['getPatient',
        'createAppointmentPrivate',
        'getAppointmentsPerUser',
        'getServicesConsultingRoom',
        'createTreatment',
        'getTreatmentsPatient',
        'createPayment'
      ]),
      async getTreatments(){
       try {
        this.treatments =  await this.getTreatmentsPatient(this.$route.params.id)
        this.treatments = this.treatments.data
        console.log(this.treatements)
        this.treatementDialog = false
       } catch (error) {
        console.log(error)
       }
      },
      async init(){
          this.patient = await this.getPatient(this.$route.params.id)
          this.appointments = await this.getAppointmentsPerUser(this.$route.params.id)
          this.getTreatments()
          this.services = await this.getServicesConsultingRoom(this.patient.data.id_consultingRoom)
          this.services = this.services.data
        },
      editTreatment(data){
        this.treatementEditDialog = true
        this.currentItem = data
      },
      async sendForm(form){
      try {
          await this.createAppointmentPrivate(form)
          this.showAlert = true
          this.appointments={data:[]}
          this.appointments = await this.getAppointmentsPerUser(this.$route.params.id)
          this.message = "Cita agendada"
          this.createAppointmentDialog= false
      } catch (error) {
        console.log(error)
      }
    },
    }

}
</script>

<style>

</style>