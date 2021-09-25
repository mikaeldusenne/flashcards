<template>
  <nav class="navbar navbar-dark bg-dark navbar-expand-lg">
    <a class="navbar-brand" href="/mikarezoo-flashcards"> <b-nav-item to="/">Mikarezoo-flashcards</b-nav-item></a>
    <button class="navbar-toggler" type="button" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" @click="toggleNavbar">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent" :class="{in: expanded}">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <b-nav-item to="/train">Train</b-nav-item>
        </li>
      </ul>
      <ul class="navbar-nav mb-2 mb-lg-0" id="navright">
        <li class="nav-item" v-if="showLogin && getLoggedIn">
          <a class="nav-link" v-on:click="logout()" href="#"> Logout </a>
        </li>
        <!-- <span class="navbar-text" style="margin-right: 0.5rem;">
             {{ getUser.email }}
             </span> -->
        
      </ul>
    </div>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark" v-if="false">
      >
      <a class="navbar-brand" href="/mikarezoo-flashcards">
        mikarezoo-flashcards
      </a>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!-- <b-nav-item to="/about">About</b-nav-item> -->
          <b-nav-item to="/train">Train</b-nav-item>
          
          <!-- <b-navbar-nav v-if="showLogin && !getLoggedIn" class="ml-auto">
               <b-nav-item to="/login">Login</b-nav-item>
               <b-nav-item to="/register">Register</b-nav-item>
               </b-navbar-nav> -->
          
        </b-navbar-nav>
      </b-collapse>
    </nav>
  </nav>
  
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { mapGetters } from "vuex";
import axios from "axios";

@Component({
  computed: mapGetters(["getUser", "getLoggedIn"]),
})
export default class NavBar extends Vue {
  showLogin = true;
  expanded = false;
  toggleNavbar() {
    this.expanded = !this.expanded;
  }
  logout(){
    axios.get('/logout')
    .then(e => {
      this.$router.go(0)
    })
    .catch(console.log)
  }
  
  
}
</script>

<style scoped>

#nav-collapse > ul{
  display: flex;
  justify-content: space-between;
}

.in.collapse{
  display: inherit !important;
}

a.nav-link{
  color: white;
}

a.nav-link:visited{
  color: white;
}

.nav-item{
  margin: 0 0.5rem; 
}
</style>
