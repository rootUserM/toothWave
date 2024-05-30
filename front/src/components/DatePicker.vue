<template>
  <v-menu
    v-model="internMenu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    max-width="290px"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="dateFormatted"
        :label="labelComp"
        prepend-icon="mdi-calendar"
        readonly
        outlined
        v-bind="attrs"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker v-model="date" no-title @input="sendDate()"></v-date-picker>
  </v-menu>
</template>

<script>
export default {
  name: "DatePicker",
  props: {
    label: {
      type: String,
      default: "Registra la fecha",
    },
  },
  data: () => ({
    dateFormatted: null,
    internMenu: false,
    date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    labelComp: "",
  }),
  mounted() {
    this.init();
  },
  methods: {
    sendDate() {
      this.internMenu = false;
      this.$emit("setDate", this.date);
    },
    init() {
      this.dateFormatted = this.formatDate(
        new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
          .toISOString()
          .substr(0, 10)
      );
      this.labelComp = this.label;
      this.$emit("setDate", this.date);
    },
    formatDate(date) {
      if (!date) return null;

      const [year, month, day] = date.split("-");
      return `${month}/${day}/${year}`;
    },
  },
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
};
</script>

<style></style>
