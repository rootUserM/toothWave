<template>
  <v-dialog v-model="dialog" persistent width="1024">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="text-none"
        density="compact"
        v-if="toEdit"
        v-bind="attrs"
        v-on="on"
        icon
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>

      <v-row justify="end" v-else>
        <v-btn class="text-none mr-10" v-bind="attrs" v-on="on">
          Agregar consultorio
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">Clínica</span>
      </v-card-title>
      <v-form ref="form" @submit.prevent="validate" v-model="valid">
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  label="Nombre de Clínica *"
                  v-model="form.name"
                  :rules="nameRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.webpage"
                  label="Pagina Web"
                  hint="www.miconsultorio.com"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.email"
                  type="email"
                  label="Email de clínica"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.phone_number"
                  label="Número Telefónico *"
                  :rules="phoneRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col>
                <v-file-input
                  accept="image/png, image/jpeg"
                  placeholder="Sube aqui el logo que deseas ver en el formulario de citas."
                  prepend-icon="mdi-camera"
                  label="Logo *"
                  @change="handleFileUpload"
                  :rules="[(v) => !!v || 'Logo es requerido']"
                  required
                ></v-file-input>
                <div v-if="logoPreview">
                  <v-avatar>
                    <img :src="logoPreview" alt="Clinica imagen" />
                  </v-avatar>
                </div>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="form.address"
                  label="Dirección"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="text-none"
            @click="dialog = false"
            color="blue darken-1"
            text
          >
            Cancelar
          </v-btn>

          <v-btn
            :disabled="!valid"
            :loading="loading"
            class="text-none"
            color="blue darken-1"
            text
            type="submit"
          >
            Crear
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    toEdit: Boolean,
    formToEdit: Object,
    defaultOpen: Boolean,
    dialog: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    consulting_rooms: null,
    loading: false,
    nameRules: [
      (v) => !!v || "Name is required",
      (v) => (v && v.length <= 20) || "Name must be less than 10 characters",
    ],
    phoneRules: [
      (v) => !!v || "Phone number is required",
      (v) => /^\d{0,10}$/.test(v) || "Phone number must be at most 10 digits",
    ],
    form: {
      id_owner: null,
      webpage: "",
      address: "",
      name: "",
      email: "",
      phone_number: "",
    },
    valid: true,
    form2prov: {
      id_owner: null,
      webpage: "https://www.clinicashida.com",
      address: "Fake por ahi",
      name: "Una clinica chida",
      email: "mi@email.com",
      phone_number: "5255452172",
    },
    logo: null,
    logoPreview: null,
  }),
  mounted() {
    if (this.toEdit) {
      this.form = this.formToEdit;
    }
  },
  methods: {
    ...mapActions([
      "getConsultingRooms",
      "createConsultingRoom",
      "editConsultingRoom",
      "deleteConsultingRoom",
    ]),
    handleFileUpload(file) {
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.logoPreview = e.target.result;
        };
        reader.readAsDataURL(file);
        this.logo = file;
      }
    },
    validate() {
      if (this.$refs.form.validate()) {
        this.createCR();
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    async createCR() {
      this.loading = true;
      try {
        const formData = new FormData();
        formData.append("id_owner", this.$store.state.id);
        formData.append("name", this.form.name);
        formData.append("address", this.form.address);
        formData.append("webpage", this.form.webpage);
        formData.append("email", this.form.email);
        formData.append("phone_number", this.form.phone_number);
        if (this.logo) {
          formData.append("logo", this.logo);
        }
        await this.createConsultingRoom(formData);
        this.dialog = false;
        this.$emit("getConsulRooms");
        this.$refs.form.reset();
        this.loading = false;
      } catch (error) {
        console.log(error);
      }
    },
    async editCR() {
      this.loading = true;
      try {
        await this.editConsultingRoom({
          id: this.formToEdit.id,
          form: this.form,
        });
        this.dialog = false;
        this.$emit("getConsulRooms");
        this.loading = false;
      } catch (error) {
        console.log(error);
      }
    },
    async deleteCR() {
      this.loading = true;
      try {
        await this.deleteConsultingRoom(this.formToEdit.id);
        this.dialog = false;
        this.$emit("getConsulRooms");
        this.loading = false;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style></style>
