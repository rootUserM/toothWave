<template>
  
    <v-dialog
      v-model="dialog"
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            class="text-none"
          v-bind="attrs"
          v-on="on"
        >
        <div v-if="form.id">
            Editar registro de px
        </div>
        <div v-else>
            Agregar px
        </div>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Paciente</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
                <v-col cols="6">
                    <v-text-field
                  label="Nombre*"
                  required
                  v-model="form.Name"
                ></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field
                  label="Apellido paterno*"
                  required
                  v-model="form.Last_name"
                ></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field
                  label="Apellido Materno*"
                  required
                  v-model="form.Second_last_name"
                ></v-text-field>
                </v-col>
               
              <v-col cols="6" >
                <v-text-field
                  label="Email"
                  v-model="form.Email"
                ></v-text-field>
              </v-col>
              <v-col cols="6" >
                <v-text-field
                  label="Teléfono celular*"
                  required
                  v-model="form.PhoneNumber"
                ></v-text-field>
              </v-col>
             
              <v-col
                cols="12"
                sm="6"
              > 
              <DatePicker @setDate="setDate" :label="'Fecha de nacimiento'"></DatePicker>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
              <v-radio-group v-model="form.Gender">
                <label for="">Sexo</label>
                <v-row>
                    <v-col><v-radio value="Masculino" label="Masculino"></v-radio></v-col>
                <v-col><v-radio value="Femenino" label="Femenino"></v-radio></v-col>
                </v-row>
            </v-radio-group>
              </v-col>
            </v-row>
          </v-container>
          <small>* indica campo requerido</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
             class="text-none"
            color="blue darken-1"
            text
            @click="dialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            class="text-none"
            color="blue darken-1"
            text
            @click="summit()"
          >
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>

<script>
import { mapActions } from 'vuex'
import DatePicker from '@/components/DatePicker.vue'
 export default {
  components:{
  DatePicker
  },
  props:{
        toEdit:Boolean,
        patient:Object,
    },
    data: () => ({
      dialog: false,
      chale:false,
      form:{
        Name:'',
        Last_name:'',
        Second_last_name:'',
        Eage:'',
        Birth_date:'',
        Gender:'',
        Email:'',
        PhoneNumber:'',
        id_consultingRoom:''
      }
    }),
    mounted(){
        if(this.toEdit){
            this.form=this.patient
        }
    },
    methods:{
        ...mapActions(['createPatient','editPatient']),
        setDate(value){
          const [year] = value.split("-");
          this.form.Eage = new Date().getFullYear() - Number(year);
          this.form.Birth_date =  value
        },
        async summit(){
            try {
              this.form.id_consultingRoom = this.$route.params.id
                if(this.toEdit){
                     await this.editPatient(this.form)
                    this.$emit('reloadData')
                }else{
                    await this.createPatient(this.form)
                    this.$emit('reloadData')
                }
               
               this.dialog = false
               
            } catch (error) {
                console.log(error)
            }
            
        }
    }
  }
</script>

<style>

</style>