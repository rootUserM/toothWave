<template>
  <v-app>
    <v-snackbar v-model="snackbar.show" color="error">
      {{ snackbar.message }}
    </v-snackbar>
  </v-app>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState({
      snackbar: (state) => state.snackbar,
    }),
  },
};
</script>
