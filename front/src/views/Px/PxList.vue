<template>
  <div>
    <Nav></Nav>
    <v-main class=" " style="min-height: 300px">
      <v-row class="mx-10 my-10">
        <v-col>
          <PxCreate @reloadData="init()"></PxCreate>
          <br />
          <v-data-table
            v-if="this.patients.length"
            :hide-default-footer="true"
            :disable-sort="true"
            :headers="headers"
            :items="this.patients"
            :items-per-page="5"
            class="elevation-1"
          >
            <template v-slot:[`item.detail`]="{ item }">
              <td>
                <v-btn
                  class="text-none my-2 mx-2"
                  density="compact"
                  :href="'/dashboard/detail/patient/' + item.id"
                  icon
                >
                  <v-icon dark> mdi-card-account-details-outline </v-icon>
                </v-btn>
              </td>
            </template>
          </v-data-table>
          <div v-else class="mt-5 pt-5">Aún no hay Px registrados</div>
        </v-col>
      </v-row>
    </v-main>
  </div>
</template>

<script>
import Nav from "../../components/NavBar.vue";
import { mapActions } from "vuex";
import PxCreate from "./PxCreate.vue";

export default {
  name: "PxList",
  components: {
    PxCreate,
    Nav,
  },
  data: () => ({
    patients: null,
    drawer: null,
    headers: [
      { text: "ID", value: "id" },
      {
        text: "Nombre",
        align: "center",
        sortable: false,
        value: "Name",
      },
      { text: "Apellido Paterno", value: "Last_name" },
      // { text: 'Evidencias', value: 'fat' },
      {
        text: "Apellido Materno",
        align: "center",
        value: "Second_last_name",
      },
      {
        text: "Sexo",
        align: "center",
        value: "Gender",
      },
      {
        text: "Edad",
        align: "center",
        value: "Eage",
      },
      {
        text: "Teléfono",
        align: "center",
        value: "PhoneNumber",
      },
      {
        text: "Email",
        align: "center",
        value: "Email",
      },
      {
        text: "Detalle",
        align: "center",
        value: "detail",
      },
    ],
  }),
  mounted() {
    this.init();
  },
  methods: {
    ...mapActions(["getPatients"]),
    async init() {
      const result = await this.getPatients(this.$route.params.id);
      this.patients = result.data;
    },
  },
};
</script>

<style></style>
