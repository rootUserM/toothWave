<template>
  <div>
    <Nav></Nav>
    <v-main class=" ">
      <v-row
        class="mx-10 my-10"
        v-if="this.consulting_room.data"
        justify="center"
      >
        <v-col cols="12" md="6">
          <v-row justify="start" class="mb-10 pl-6">
            <h3>Detalle de Consultorio</h3>
          </v-row>
          <v-simple-table dense>
            <tbody>
              <tr>
                <td width="200px"><b>Consultorio</b></td>
                <td>{{ this.consulting_room.data.name }}</td>
              </tr>
              <tr>
                <td width="200px"><b>Número Telefónico</b></td>
                <td>{{ this.consulting_room.data.phone_number }}</td>
              </tr>
              <tr>
                <td width="200px"><b>Correo</b></td>
                <td>{{ this.consulting_room.data.email }}</td>
              </tr>
              <tr>
                <td width="200px"><b>Dirección</b></td>
                <td>{{ this.consulting_room.data.address }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-col>
        <v-col cols="12" md="6">
          <v-img
            class="mx-auto my-10"
            :src="this.consulting_room.data.qr_code"
            width="200"
          ></v-img>
          <v-row justify="center">
            <v-col>
              <PxCreate></PxCreate>
            </v-col>
            <v-col>
              <v-btn
                class="text-none"
                :href="
                  '/dashboard/consultingroom/patients-all/' +
                  this.consulting_room.data.id
                "
              >
                Ver lista de Px
              </v-btn>
            </v-col>
            <v-col>
              <v-btn
                class="text-none"
                :href="'/appointment/gen/' + this.consulting_room.data.id"
              >
                Agendar consulta
              </v-btn>
            </v-col>
            <v-col>
              <v-btn class="text-none" @click="qrDownload()">
                Descargar código
              </v-btn>
            </v-col>
            <v-col>
              <v-btn class="text-none"> Imprimir código </v-btn>
            </v-col>
            <v-col>
              <v-btn class="text-none" @click="CreateServiceDialog = true">
                Añadir servicio
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row justify="center" class="mx-2 my-2">
        <v-col>
          <h2 class="mx-3 my-3">Pagos</h2>
          <v-data-table
            v-if="this.payments.data.length"
            :headers="payment_headers"
            :items="payments.data"
            :items-per-page="5"
            class="elevation-1"
          ></v-data-table>
          <div v-else>Aún no hay pagos que mostrar</div>
        </v-col>
        <v-col>
          <h2 class="mx-3 my-3">Citas</h2>
          <Calendar
            v-if="this.appointments.data.length"
            :events="this.appointments.data"
            :showControls="true"
          ></Calendar>
          <div v-else>Aún no hay citas agendadas</div>
        </v-col>
        <v-col>
          <h2 class="mx-3 my-3">Servicios registrados</h2>
          <v-data-table
            v-if="this.services.data.length"
            :headers="headers"
            :items="services.data"
            :items-per-page="5"
            class="elevation-1"
          >
            <template #[`item.active`]="{ item }">
              <v-icon color="red" v-if="!item.active">mdi-dots-hexagon</v-icon>
              <v-icon color="green" v-if="item.active">mdi-dots-grid</v-icon>
            </template>
            <template #[`item.actions`]="{ item }">
              <v-icon small class="mr-2" @click="editServiceDialog(item)">
                mdi-pencil
              </v-icon>

              <v-icon
                small
                @click="changeServiceStatusFunc(item, false)"
                v-if="item.active"
              >
                mdi-sync-off
              </v-icon>
              <v-icon small @click="changeServiceStatusFunc(item, true)" v-else>
                mdi-sync
              </v-icon>
            </template>
          </v-data-table>
          <div v-else>Aún no hay servicios registrados</div>
        </v-col>
      </v-row>
    </v-main>
    <v-dialog v-model="CreateServiceDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Servico</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form ref="serviceForm">
              <v-row>
                <v-col cols="6">
                  <v-text-field
                    label="Nombre*"
                    required
                    v-model="form.name"
                  ></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    label="Precio*"
                    required
                    v-model="form.price"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
          <small>* indica campo requerido</small>
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
          <v-btn class="text-none" color="blue darken-1" text @click="submit()">
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Nav from "../../components/NavBar.vue";
import Calendar from "../../components/CalendarComp.vue";
import PxCreate from "../Px/PxCreate.vue";
import { mapActions } from "vuex";

export default {
  components: {
    Calendar,
    PxCreate,
    Nav,
  },
  data: () => ({
    toEditService: false,
    CreateServiceDialog: false,
    drawer: false,
    services: {
      data: [],
    },
    payment_headers: [
      { text: "ID", value: "id" },
      { text: "Monto", value: "contribution" },
      { text: "Fecha de registro", value: "date_created" },
      {
        text: "Servicio realizado",
        value: "treatment_service_name",
        sortable: false,
      },
    ],
    headers: [
      { text: "ID", value: "id" },
      { text: "Servicio", value: "name" },
      { text: "Precio", value: "price" },
      { text: "Estatus", value: "active" },
      { text: "", value: "actions", sortable: false },
    ],
    form: {
      id_consultingRoom: "",
      name: "",
      price: 0.0,
    },
    consulting_room: {
      data: {
        name: "",
        qr_code: "",
      },
    },
    appointments: {
      data: [],
    },
    payments: {
      data: [],
    },
  }),
  mounted() {
    this.init();
  },
  methods: {
    ...mapActions([
      "getConsultingRoom",
      "getAppointmentsPerConsultingRoom",
      "createService",
      "editService",
      "changeServiceStatus",
      "getServicesAll",
      "getPaymentsPerConsultingRoom",
    ]),
    closeDialog() {
      this.CreateServiceDialog = false;
      this.$refs.serviceForm.reset();
    },
    editServiceDialog(item) {
      this.form.name = item.name;
      this.form.price = item.price;
      this.form.id = item.id;
      this.toEditService = true;
      this.CreateServiceDialog = true;
    },
    async changeServiceStatusFunc(item, status) {
      let form = {
        id: item.id,
        status: status,
      };
      await this.changeServiceStatus(form);
      this.services = await this.getServicesAll(this.$route.params.id);
    },
    async init() {
      this.consulting_room = await this.getConsultingRoom(
        this.$route.params.id
      );
      this.appointments = await this.getAppointmentsPerConsultingRoom(
        this.$route.params.id
      );
      this.services = await this.getServicesAll(this.$route.params.id);
      this.payments = await this.getPaymentsPerConsultingRoom(
        this.$route.params.id
      );
    },
    async submit() {
      try {
        this.form.id_consultingRoom = this.$route.params.id;
        if (this.toEditService) {
          await this.editService(this.form);
        } else {
          await this.createService(this.form);
        }
        this.CreateServiceDialog = false;
        this.$refs.serviceForm.reset();
        this.services = await this.getServicesAll(this.$route.params.id);
      } catch (error) {
        console.log(error);
      }
    },
    qrDownload() {
      var url = this.consulting_room.data.qr_code;
      fetch(url)
        .then((response) => response.blob())
        .then((blob) => {
          var link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          var url_new = new URL(url);
          var filename = url_new.pathname.split("/").pop();
          link.download = filename;
          link.click();
        });
    },
  },
};
</script>

<style></style>
