<template>
    <div>
    <Nav></Nav>
     <v-main class=" " style="min-height: 300px;">
       <v-row class="mx-10 my-10">
         <v-col>
            <PxCreate @reloadData="init()"></PxCreate>
            <br>
          <v-simple-table class="text-center" v-if="this.patients.length">
             <thead  class="text-center">
               <tr class="text-center">
                 <th class="text-center">
                   Id
                 </th>
                 <th class="text-center">
                   Nombre
                 </th>
                 <th class="text-center">
                   Apellido Paterno
                 </th>
                 <th class="text-center">
                   Apellido Materno
                 </th>
                 <th class="text-center">
                   Sexo
                 </th>
                 <th class="text-center">
                   Edad
                 </th>
                 <th class="text-center">
                  Teléfono
                 </th>
                 <th class="text-center">
                  Email
                 </th>
                 <th class="text-center">
                  Acciones
                 </th>
               </tr>
             </thead>
             <tbody  >
               <tr
                
                 v-for="item in this.patients"
                 :key="item.Name"
               >
                 <td>{{ item.id }}</td>
                 <td>{{ item.Name }}</td>
                 <td>{{ item.Last_name }}</td>
                 <td>{{ item.Second_last_name }}</td>
                 <td>{{ item.Gender }}</td>
                 <td>{{ item.Eage }}</td>
                 <td>{{ item.PhoneNumber }}</td>
                 <td>{{ item.Email }}</td>
                 <td>
                   <!-- <v-btn class="text-none my-2 mx-2" density="compact" :href="'/dashboard/consultingroom/'+item.id" icon> 
                     <v-icon dark>
                       mdi-view-agenda
                     </v-icon>
                   </v-btn> -->
                   <v-btn class="text-none my-2 mx-2" density="compact" :href="'/dashboard/detail/patient/'+item.id" icon> 
                     <v-icon dark>
                       mdi-card-account-details-outline
                     </v-icon>
                   </v-btn>
                 </td>
               </tr>
             </tbody>
             
         </v-simple-table>
         <div v-else class="mt-5 pt-5">
          Aún no hay Px registrados
         </div>
         </v-col>
       </v-row>
     </v-main>
    </div>
 </template>
 
 <script>
 import Nav from '../../components/NavBar.vue'
 import { mapActions } from 'vuex'
 import PxCreate from './PxCreate.vue'

 export default {
  name:'PxList',
   components:{
     PxCreate,
     Nav,
   },
   data:()=>({
     patients:null,
     drawer:null,
     }),
   mounted(){
     this.init()
   },
   methods:{
     ...mapActions(['getPatients']),
     async init(){
       const result = await this.getPatients(this.$route.params.id)
       this.patients = result.data
       
     },
 
     
 }
 }
 </script>
 
 <style>
 
 </style>