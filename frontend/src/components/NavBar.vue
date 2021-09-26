<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand to="/">Mikarezoo-flashcards</b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/explore">Explore</b-nav-item>
        <b-nav-item to="/train">Train</b-nav-item>
        <b-nav-item to="/manage" v-if="getUser.admin">Manage</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">

        <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">Français</b-dropdown-item>
          <b-dropdown-item href="#">فارسی</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right v-if="showLogin && getLoggedIn">
          <template #button-content>
            <em>{{getUser.email}}</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#" @click="logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item to="/login" v-else>Login</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
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
