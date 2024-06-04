<template>
  <div>
    <Nav></Nav>
    <v-main class=" " style="min-height: 300px">
      <v-row class="mx-md-10 my-md-10 mx-4 my-4">
        <v-col>
          <ConsultingRoom @getConsulRooms="init()"></ConsultingRoom>
          <br />
          <v-data-table
            v-if="this.consulting_rooms.length"
            :hide-default-footer="true"
            :disable-sort="true"
            :headers="headers"
            :items="this.consulting_rooms"
            :items-per-page="5"
            class="elevation-1"
          >
            <template v-slot:[`item.id`]="{ item }">
              {{ String(item.id).substring(0, 8) }}
            </template>

            <template v-slot:[`item.detail`]="{ item }">
              <td>
                <v-btn
                  class="text-none my-2 mx-2"
                  density="compact"
                  :href="'/dashboard/consultingroom/' + item.id"
                  icon
                >
                  <v-icon dark> mdi-view-agenda </v-icon>
                </v-btn>
              </td>
            </template>
            <template v-slot:[`item.pxs`]="{ item }">
              <td>
                <v-btn
                  class="text-none my-2 mx-2"
                  density="compact"
                  :href="'/dashboard/consultingroom/patients-all/' + item.id"
                  icon
                >
                  <v-icon dark> mdi-account-injury-outline </v-icon>
                </v-btn>
              </td>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-main>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import ConsultingRoom from "@/components/C_E_ConsultingRoom.vue";
import Nav from "@/components/NavBar.vue";
export default {
  components: {
    ConsultingRoom,
    Nav,
  },
  data: () => ({
    consulting_rooms: [],
    drawer: null,
    headers: [
      { text: "ID", value: "id" },
      {
        text: "Nombre de Clínica",
        align: "center",
        sortable: false,
        value: "name",
      },
      { text: "Dirección", value: "address" },
      // { text: 'Evidencias', value: 'fat' },
      {
        text: "WebSite",
        align: "center",
        value: "webpage",
      },
      {
        text: "No. Citas en curso",
        align: "center",
        value: "count_appointments",
      },
      {
        text: "Detalle",
        align: "center",
        value: "detail",
      },
      {
        text: "Pacientes",
        align: "center",
        value: "pxs",
      },
    ],
  }),
  mounted() {
    this.init();
  },
  methods: {
    ...mapActions([
      "getAppointments",
      "getConsultingRooms",
      "createConsultingRoom",
    ]),
    async init() {
      try {
        var result = await this.getConsultingRooms();
        this.consulting_rooms = result.data;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style></style>
