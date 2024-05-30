<template>
  <div>
    <Nav></Nav>
    <v-main class=" " style="min-height: 300px; margin-top: 110px;">
        <h1>404</h1>
        <img style="max-width: 100%;height: auto;" src="../assets/404.gif">
        <p><b>Lo sentimos el contenido que buscas no esta disponible. :(</b></p>
    </v-main>
</div>
</template>

<script>
import Nav from '@/components/NavBar.vue'
export default {
    components:{
        Nav
    }
}
</script>

<style>

</style>