<template>
  <div id="app">
    <NavBar />
    <div v-if="false && !getLoggedIn" style="margin-top: 2rem;">
      <b-container fluid>
        <b-row class="d-flex justify-content-center">
          <b-col xs="12" sm="10" xl="4" lg="6">
            <Login />
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div v-else id="content">
      <router-view />
    </div>
    
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";
import NavBar from "@/components/NavBar.vue";
import Login from "@/components/Login.vue";


import { mapGetters } from "vuex";


@Component({
  computed: mapGetters(["getLoggedIn"]),
  components: {
    NavBar,
    Login,
  },
})
export default class App extends Vue {
  getLoggedIn!: boolean;
  
  mounted() {
    axios
    .get("/login-check", {})
    .then((resp) => {
      console.log('LOG CHECK')
      console.log(resp.data)
      if(resp.data.email){
        this.$store
        .dispatch("setUser", resp.data)
        .then(console.log)
        .catch(console.error);
      }else{
        console.log("not logged in")
      }
    })
    .catch(console.log);

    
    axios
    .get("/api/langs", {})
    .then((resp) => {
      this.$store
      .dispatch("setLangs", resp.data)
      .then(console.log)
      .catch(console.error);
    })
    .catch(console.log);
    
    axios
    .get("/api/decks")
    .then((resp) => {
      this.$store
      .dispatch("setDecks", resp.data)
      .then(console.log)
      .catch(console.error);
    })
    .catch(console.log);
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#content a {
  font-weight: bold;
  color: #2c3e50;
}

#content a.router-link-exact-active {
  color: #42b983;
}
</style>
