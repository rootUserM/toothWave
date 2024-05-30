<template>

 
   <div>
    <Nav></Nav>
    <v-main class=" " style="min-height: 300px;">
      <v-row class="mx-10 my-10">
        <v-col>
        <ConsultingRoom @getConsulRooms="init()"></ConsultingRoom>
         <br>
         <v-simple-table class="text-center">
            <thead  class="text-center">
              <tr class="text-center">
                <th class="text-center">
                  Id
                </th>
                <th class="text-center">
                  Nombre de Clínica
                </th>
                <th class="text-center">
                  Dirección
                </th>
                <th class="text-center">
                  WebSite
                </th>
                <th class="text-center">
                  No. Citas en curso
                </th>
                <th class="text-center">
                  Detalle
                </th>
                <th class="text-center">
                  Pacientes
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in this.consulting_rooms"
                :key="item.name"
              >
                <td>{{ String(item.id).substring(0,8) }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.address }}</td>
                <td>{{ item.webpage }}</td>
                <td>{{ item.count_appointments }}</td>
                <td>
                  <v-btn class="text-none my-2 mx-2" density="compact" :href="'/dashboard/consultingroom/'+item.id" icon> 
                    <v-icon dark>
                      mdi-view-agenda
                    </v-icon>
                  </v-btn>
                </td>
                <td>
                  <v-btn class="text-none my-2 mx-2" density="compact" :href="'/dashboard/consultingroom/patients-all/'+item.id" icon> 
                    <v-icon dark>
                      mdi-account-injury-outline
                    </v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
        </v-simple-table>
        </v-col>
      </v-row>
    </v-main>
   </div>
</template>

<script>
import { mapActions } from 'vuex'
import ConsultingRoom from '@/components/C_E_ConsultingRoom.vue'
import Nav from '@/components/NavBar.vue'
export default {
  components:{
    ConsultingRoom,
    Nav
  },
  data:()=>({
    consulting_rooms:null,
    drawer:null,
    }),
  mounted(){
    this.init()
  },
  methods:{
    ...mapActions(['getAppointments','getConsultingRooms','createConsultingRoom']),
    async init(){
      try {
        var result = await this.getConsultingRooms()
      this.consulting_rooms = result.data
      } catch (error) {
        console.log(error)
      }
    },
}
}
</script>

<style>

</style>