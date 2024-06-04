<template>
  <div>
    <!-- <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list
        dense
      >
        <v-list-item
        href="/dashboard"
        >
          <v-list-item-icon>
            <v-icon>mdi-hospital-building</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Clinicas</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app>
      <v-row>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </v-row>
      <v-row justify="center" class="my-5 mx-5">
        <img class="" width="30" src="../assets/here_black.png" alt="">
      </v-row>
      <v-row justify="end" class="my-5 mx-5">
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          icon
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title>Configuraciones</v-list-item-title>
        </v-list-item>
        <v-list-item @click="closeSesion()">
          <v-list-item-title>Cerrar sesión</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
      </v-row>
    </v-app-bar> -->
    <template>
      <!-- <v-system-bar color="deep-purple darken-3"></v-system-bar> -->

      <v-app-bar app>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

        <!-- <img
          class=""
          style="margin-left: 110px"
          width="30"
          src="../assets/here_black.png"
          alt=""
        /> -->
        <v-spacer></v-spacer>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" icon>
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>Configuraciones</v-list-item-title>
            </v-list-item>
            <v-list-item @click="closeSesion()">
              <v-list-item-title>Cerrar sesión</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>
      <v-navigation-drawer v-model="drawer" absolute temporary>
        <v-list nav dense>
          <v-list-item-group
            v-model="group"
            active-class="blue  text--accent-4"
          >
            <v-list-item href="/dashboard">
              <v-list-item-icon>
                <v-icon>mdi-hospital-building</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title>Clinicas</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
      <v-card-text> </v-card-text>
    </template>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "NavBar",
  data: () => ({
    drawer: false,
    group: null,
  }),
  methods: {
    ...mapActions(["logout"]),
    closeSesion() {
      setTimeout(() => {
        this.logout();
        this.$router.replace("/");
      }, 200);
    },
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>

<style></style>
