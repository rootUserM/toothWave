<template>
  <v-container>
    <v-row class="mt-3" justify="center">
      <v-col cols="12" md="6" class="comment-scolled">
        <img
          v-if="logoUrl"
          :src="logoUrl"
          alt=""
          width="100px"
          height="100px"
        />
        <img
          v-else
          src="../assets/here_black.png"
          width="100px"
          height="100px"
        />
        <v-form ref="form" v-model="valid" @submit.prevent="sendForm">
          <v-row>
            <v-col><p class="mt-3">Paciente de primera vez</p></v-col>
            <v-col>
              <v-radio-group v-model="form.firstTimePatient">
                <v-row>
                  <v-col>
                    <v-radio label="Si" :value="true"></v-radio>
                  </v-col>
                  <v-col>
                    <v-radio label="No" :value="false"></v-radio>
                  </v-col>
                </v-row>
              </v-radio-group>
            </v-col>
          </v-row>
          <v-col class="my-3">
            <div v-if="form.firstTimePatient">
              <v-text-field
                required
                name="client_name"
                outlined
                label="Nombre *"
                v-model="form.patient.Name"
                :rules="nameRules"
              ></v-text-field>
              <v-row>
                <v-col>
                  <v-text-field
                    required
                    name="last_name"
                    outlined
                    label="Apellido paterno *"
                    v-model="form.patient.Last_name"
                    :rules="nameRules"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    required
                    name="last_name"
                    outlined
                    label="Apellido materno *"
                    v-model="form.patient.Second_last_name"
                    :rules="nameRules"
                  ></v-text-field>
                </v-col>
              </v-row>
            </div>
            <v-text-field
              required
              name="phone"
              outlined
              type="phone"
              label="Numero celular *"
              hint=""
              v-model="form.patient.PhoneNumber"
              :rules="phoneRules"
            ></v-text-field>
            <v-textarea
              name="appointment_motive"
              outlined
              label="Motivo de consulta"
              v-model="form.appointmentMotive"
            ></v-textarea>
          </v-col>
          <v-row class="my-3 pr-4">
            <v-menu
              v-model="menu2"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="computedDateFormatted"
                  label="Fecha de consulta"
                  prepend-icon="mdi-calendar"
                  readonly
                  outlined
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="date"
                no-title
                @input="menu2 = false"
              ></v-date-picker>
            </v-menu>
          </v-row>
          <v-row class="my-md-3 pr-4">
            <v-menu
              ref="menu"
              v-model="menu3"
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
                v-if="menu3"
                v-model="time"
                full-width
                @click:minute="$refs.menu.save(time)"
                max="19:00:00"
                min="10:00:00"
              ></v-time-picker>
            </v-menu>
          </v-row>
          <v-btn
            :disabled="!valid"
            name="send_service_request"
            type="submit"
            :loading="loading"
            class="text-none"
            color="blue darken-1"
            text
          >
            Agendar
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
    <v-snackbar :timeout="2000" v-model="showAlert" color="black">
      {{ message }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data: () => ({
    phoneRules: [
      (v) => !!v || "Este campo es requerido",
      (v) => /^\d{0,10}$/.test(v) || "Telefono a 10 digitos",
    ],
    nameRules: [
      (v) => !!v || "Este campo es requerido",
      (v) => (v && v.length <= 20) || "No cumple con 20 caracteres maximo",
    ],
    valid: true,
    logoUrl: null,
    time: null,
    menu3: false,
    menu2: false,
    showAlert: false,
    loading: false,
    message: "",
    date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    dateFormatted: null,
    form: {
      patient: {
        Name: "",
        Last_name: "",
        Second_last_name: "",
        PhoneNumber: "",
        id_consultingRoom: "",
      },
      appointmentMotive: "",
      firstTimePatient: false,
      appointmentDate: null,
      id_consultingRoom: "",
      appointmentHour: null,
    },
  }),
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    },
  },
  watch: {
    date() {
      this.dateFormatted = this.formatDate(this.date);
    },
  },
  mounted() {
    this.init();
  },
  methods: {
    ...mapActions([
      "getConsultingRoom",
      "getAppointmentsPerConsultingRoom",
      "createAppointment",
      "getConsultingRoomLogo",
    ]),
    async init() {
      this.dateFormatted = this.formatDate(
        new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
          .toISOString()
          .substr(0, 10)
      );
      let response = await this.getConsultingRoomLogo(this.$route.params.id);
      this.logoUrl = response.data.logo_url;
    },
    async sendForm() {
      this.loading = true;
      this.form.appointmentHour = this.time + ":00";
      this.form.id_consultingRoom = this.$route.params.id;
      this.form.patient.id_consultingRoom = this.$route.params.id;
      this.form.appointmentDate = this.date;
      if (this.$refs.form.validate()) {
        try {
          await this.createAppointment(this.form);
          this.showAlert = true;
          this.$refs.form.reset();
          this.message = "Cita agendada";
        } catch (error) {
          console.log(error);
        }
        this.loading = false;
      }
    },
    formatDate(date) {
      if (!date) return null;

      const [year, month, day] = date.split("-");
      return `${month}/${day}/${year}`;
    },
    parseDate(date) {
      if (!date) return null;

      const [month, day, year] = date.split("/");
      return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    },
  },
};
</script>

<style></style>
