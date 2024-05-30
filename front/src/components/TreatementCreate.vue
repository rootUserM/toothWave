<template>
  <v-dialog v-model="dialogVisible" max-width="600px" @input="handleCloseDialog" persistent>
    <v-card >
      <h1 class="pt-5">Nota de evolución para {{ patient.Name }}</h1>
      <v-form ref="form" @submit.prevent="createTreatmentFunc">
        <v-card-text>
          <v-container>
            <v-col cols="12" class="comment-scolled">
              <v-row class="my-3">
                <DatePicker @setDate="setDate" :label="'Fecha de registro'"></DatePicker>
              </v-row>
              <v-row>
                <v-select
                  v-if="services.length"
                  prepend-icon="mdi-bottle-tonic-plus-outline"
                  :items="services"
                  :menu-props="{ buttom: true, offsetY: true }"
                  label="Tratamiento(s)"
                  outlined
                  item-text="name"
                  item-value="id"
                  v-model="treatment_form.services"
                  multiple
                  density="compact"
                 @input="getTotalPrice()"
                ></v-select>
              </v-row>
              <v-row justify="center">
                <v-col cols="6">
                  <v-text-field
                    label="Pago"
                    required
                    v-model="treatment_form.payment"
                    hint="Registra el pago que hizo el px"
                    outlined
                    shaped
                    :rules="[priceRules]"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-textarea
                  outlined
                  label="Nota"
                  v-model="treatment_form.note"
                  hint="Describa procedimeinto"
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
            Registrar
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
import DatePicker from "@/components/DatePicker.vue";
import { mapActions } from "vuex";

export default {
  components: {
    DatePicker,
  },
  props: ["showDialog", "currentData", "patient", "services"],
  data: () => ({
    totalPrice:0,
    dialogVisible:false,
    loading: false,
    neededPrice:0,
    dataComponent:{
      payment_info:{},
            date:'',
            note:'',
    },
    treatment_form: {
      services: [],
      id_patient: null,
      id_consultingRoom: null,
      date: null,
      note:  new Date().toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' , hour:'numeric',minute:'numeric'})+'\n',
      payment: 0.0,
    },
    payment_form: {
      contribution: 0.0,
      id_consultingRoom: "",
      id_treatment: "",
    },
    payment_headers:[
    { text: 'Fecha de pago', value: 'date_created' },
    { text: 'Monto aportado', value: 'contribution' },
    ],
  }), 
  methods: {
    ...mapActions([
      "createAppointmentPrivate",
      "getAppointmentsPerUser",
      "getServicesConsultingRoom",
      "createTreatment",
      "createPayment",
    ]), 
   
    getTotalPrice(){
      let totalPrice= 0;
      this.treatment_form.services.forEach(x=>{totalPrice += Number(this.services.find( y => y.id == x).price)})
      this.totalPrice = totalPrice
    },
    handleCloseDialog(){
      this.dataComponent = {
      payment_info:{},
            date:'',
            note:'',
    }
      this.$emit('closeDialog')

    },
    closeDialog(){
      this.$emit('closeDialog');
    },
    setDate(value) {
      this.treatment_form.date = value;
    },
    async createTreatmentFunc() {
      this.loading = true;
      this.treatment_form.payment = parseFloat(this.treatment_form.payment);
      this.treatment_form.id_patient = this.patient.id;
      this.treatment_form.id_consultingRoom = this.patient.id_consultingRoom;
      try {
        await this.createTreatment(this.treatment_form);
        this.$refs.form.reset();
        this.$emit("getTreatments");
        this.$emit("colseDialog")
      } catch (error) {
        console.log(error);
      }
      this.loading = false;
    },
  },
  watch: {
    showDialog(newVal) {
      this.dialogVisible = newVal;
    },
    currentData(newVal){
      this.dataComponent = newVal
    },
  },
  computed:{
    priceRules(){
      const validateValue = (value) => {
    if (!value || isNaN(value) || parseFloat(value) > this.totalPrice) {
      return 'El monto no debe exeder los ' + this.totalPrice;
    }
    return true;
  };

  try {
    return validateValue;
  } catch (error) {
    console.log(error);
    return false;
  }
    }
  }
};
</script>

<style></style>
