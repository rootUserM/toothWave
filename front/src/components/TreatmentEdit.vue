<template>
    <v-dialog v-model="dialogVisible" max-width="600px" @input="handleCloseDialog" persistent>
    <v-card >
      <h1 class="pt-5">Nota de evolución de {{ patient.Name }}</h1>
      
        <v-card-text>
          <v-container>
            <v-col cols="12" class="comment-scolled">
            
              <v-col cols="12">
            <v-simple-table dense v-if="dataComponent" > 
                <tbody>
                    <tr>
                        <td width="200px"><b>Fecha de registro</b></td>
                        <td>{{dataComponent.date}}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Servicio(s) relacionado(s)</b></td>
                        <td>{{ dataComponent.payment_info.name_services.join() }}</td>
                    </tr>
                    <tr>
                        <td width="200px"><b>Nota de registro</b></td>
                        <td> 
                          <v-row>
                            <v-col>
                              <v-btn icon @click="setToEditNote(dataComponent.note)" style="position: absolute; margin:auto 100px;"> <v-icon>mdi-pencil</v-icon></v-btn>
                             <p v-html="dataComponent.note.replace(/\n/g, '<br>')"></p>
                            </v-col>
                        </v-row> 
                      </td>
                    </tr>
                </tbody>
            </v-simple-table>
        </v-col>
              <div class="mb-10">
                <v-row justify="center" v-if="!this.dataComponent.payment_info.total_debt == 0">
                    <v-col cols="6">
                    <v-form ref="form">
                    <v-text-field
                      label="Añadir pago"
                      required
                      v-model="payment_form.contribution"
                      hint="Registra el pago que hizo el px"
                      outlined
                      shaped
                      density="compact"
                      :rules="[priceRules]"
                    ></v-text-field>
                </v-form>
                  </v-col>
                  <v-col cols="6">
                    <v-btn @click="createPaymentFunc()" icon
                      ><v-icon>mdi-plus</v-icon></v-btn
                    >
                  </v-col>
                </v-row>
                <div v-else class="mt-5 mb-5">
                    <p style="color: #1E88E5;" class="font-italic"> El tratamiento fue liquidado</p>
                  </div>
                <v-row v-if="dataComponent">
                  <v-data-table
                    :headers="payment_headers"
                    :items="dataComponent.payment_info.payments_list"
                    :items-per-page="5"
                    class="elevation-1"
                  >
                  <template v-slot:[`item.date_created`]="{item }">
                    <span v-html="item.date_created.substring(0,10)">
                    </span>
                  </template>
                  </v-data-table>
                </v-row>
                
              </div>
            </v-col>
            <v-row v-if="editFieldNote" class="mt-2">
                  <v-textarea
                  :autofocus="true"
                  outlined
                  label="Nota"
                  v-model="treatment_form.note"
                  hint="Describa procedimeinto"
                ></v-textarea>
                </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions v-if="!editFieldNote">
          <v-spacer></v-spacer>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            @click="closeDialog()"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
        <v-card-actions v-else>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            @click="editFieldNote =false"
          >
            Cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            @click="updateNote()"
          >
            Actualizar nota
          </v-btn>
        </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    showDialog:Boolean, 
    currentData:Object,
    patient:Object,
    services:Array
  },
  data: () => ({
    editFieldNote:false,
    dialogVisible: false,
    loading: false,
    neededPrice:0,
    treatment_form: {
      note: "",
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
    dataComponent:{
      payment_info:{
        total_debt:0,
        name_services:[]
      },
            date:'',
            note:'',
    },
  }), 
  methods: {
    ...mapActions([
      "createPayment",
      "updateTreatmentPatient"
    ]), 
    setToEditNote(currentNote){
      this.editFieldNote=true; 
      this.treatment_form.note = currentNote +'\n'+ new Date().toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' , hour:'numeric',minute:'numeric'})+'\n';
    },
    async updateNote(){
      try {
        await this.updateTreatmentPatient({id:this.currentData.id,form:this.treatment_form})
        this.$emit("getTreatments");
        this.treatment_form.note = ''
        this.editFieldNote=false; 
      } catch (error) {
        console.log(error)
      }
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
      this.$emit('closeDialog')
    },
    async createPaymentFunc() {
        try {
        this.payment_form.id_consultingRoom =  this.currentData.payment_info.payments_list[0].id_consultingRoom;
        this.payment_form.id_treatment =  this.currentData.id;
        this.payment_form.contribution = parseFloat(this.payment_form.contribution);
        let result = await this.createPayment(this.payment_form);
        if(this.dataComponent.payment_info.total_debt == this.payment_form.contribution ) this.dataComponent.payment_info.total_debt = 0;
        this.dataComponent.payment_info.payments_list =result.data;
        this.$refs.form.reset();
        this.$emit("getTreatments");
        } catch (error) {
         console.log(error) 
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
    priceRules() {
  try {
    let obj = this.dataComponent;
    return (value) => {
      if (!value || isNaN(value) || parseFloat(value) > (obj ? obj.payment_info.total_debt : 0)) {
        return 'El monto no debe exceder los ' + (obj ? obj.payment_info.total_debt : 0);
      }
      return true;
    };
  } catch (error) {
    return false;
  }
}

  }
};
</script>

<style>

</style>