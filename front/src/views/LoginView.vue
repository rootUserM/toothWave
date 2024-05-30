<template>
    <v-container fluid fill-height class="px-0 py-0">
        <v-row class="fill-height" >
            <v-col cols="6"  class="mainBck  d-none d-md-flex align-center justify-center" >
                    <img src="../assets/here2.png">
            </v-col>
            <v-col class="mt-auto mb-auto" >
               
                    <v-row class=" mx-md-10 px-md-10  px-4">
                        <v-col class="fill-height">
                            <img class="d-md-none" src="../assets/here_black.png" alt="">
                            <v-form  class="mt-8" @submit.prevent>
                        <v-text-field
                            v-model="form.email"
                            type="email"
                            label="Email"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model="form.password"
                            label="Password"
                            type="password"
                            hint="Enter your password to access this website"
                        ></v-text-field>
                        <v-btn type="submit" block class="mt-2 text-none" :loading="loading" @click="submit()">Entrar</v-btn>
                    </v-form>
                        </v-col>
                    </v-row>
                
            </v-col>
    </v-row>
    <v-snackbar
      :timeout="2000"
      v-model="show"
      color="black"
    >
      Las credenciales son incorrectas. <v-icon color="red">mdi-alert-circle-outline</v-icon>
    </v-snackbar>
    </v-container>
</template>

<script>
import { mapActions } from 'vuex'


export default {
    name:'LoginView',
    data:()=>({
        loading: false,
        show:false,
        form:{
            email:'admin@citassalud.com',
            password:'tesca123',
        },
    }),
    mounted(){
        localStorage.setItem('token', '');
    },  
    methods:{
        ...mapActions(['login']),
        async submit(){
            this.loading = true
           try {
            let response = await this.login(this.form);
            if(response.code == 'ERR_BAD_REQUEST'){
                this.show = true
                this.loading = false
            }
            setTimeout(() => {
                if(this.$store.state.token != ''){
                this.$router.replace({ name: 'dashboard' }); 
                }
            }, 100);
              
           } catch (error) {
            this.show = true
            this.loading = false
           }
        }
    }

}
</script>

<style>
.mainBck{
    background-color: black;
}
.form{
  width: 50%;
}
</style>