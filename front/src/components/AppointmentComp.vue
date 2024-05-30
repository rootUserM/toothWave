<template>
  <v-dialog v-model="showDialog" max-width="600px" persistent>
    <v-card>
      <h1 class="mt-5">Cita para {{ patientName }}</h1>
      <v-form ref="form" @submit.prevent="sendForm">
        <v-card-text>
          <v-container>
            <v-col cols="12" class="comment-scolled">
              <v-row class="my-3">
                <DatePicker @setDate="setDate" :label="'Fecha para la cita'"></DatePicker>
              </v-row>
              <v-row class="my-3">
                <v-menu
                  ref="menu"
                  v-model="timeMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="time"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      outlined
                      v-model="time"
                      label="Hora de consulta"
                      prepend-icon="mdi-clock-time-four-outline"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-if="timeMenu"
                    v-model="time"
                    full-width
                    @click:minute="$refs.menu.save(time)"
                    max="19:00:00"
                    min="10:00:00"
                  ></v-time-picker>
                </v-menu>
              </v-row>
              <v-row>
                <v-select
                  :menu-props="{ buttom: true, offsetY: true }"
                  prepend-icon="mdi-bottle-tonic-plus-outline"
                  :items="services"
                  label="Tratamiento"
                  outlined
                  v-model="form.id_service"
                  item-text="name"
                  item-value="id"
                ></v-select>
              </v-row>
              <v-row>
                <v-textarea
                  name="appointment_motive"
                  outlined
                  label="Notas para consulta"
                  v-model="form.appointmentMotive"
                  hint="Describa sintomas o molestias"
                ></v-textarea>
              </v-row>
            </v-col>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            @click="closeDialog()"
          >
            Cancelar
          </v-btn>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            type="submit"
            :loading="loading"
          >
            Agendar
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
import DatePicker from './DatePicker.vue';
export default {
  name:'AppointmentComp',
  props:{
    createAppointmentDialog:Boolean,
    services:Array,
    patientName:String,
    id_consultingRoom:String,
    id_patient:String
  },
  components:{
    DatePicker
  },
  data: () => ({
    timeMenu:false,
    time: null,
    loading:false,
    showDialog:false,
    form:{
      appointmentMotive:'',
      firstTimePatient:false,
      appointmentDate:null,
      id_consultingRoom:null,
      appointmentHour:null,
      id_patient:null,
      id_service:null
    },
  }),
  watch:{
    createAppointmentDialog(newVal){
      this.showDialog = newVal
    },
  },
  methods:{
    closeDialog(){
      this.$emit('closeDialog');
    },
    setDate(value){
      this.form.appointmentDate = value
    },
    sendForm(){
      this.loading = true
      this.form.id_consultingRoom=this.id_consultingRoom
      this.form.id_patient=this.id_patient
      this.form.appointmentHour = this.time+':00'
      this.$emit('sendForm',this.form)
      this.$refs.form.reset()
      this.loading = false  
    }
  }
};
</script>

<style>

</style>
