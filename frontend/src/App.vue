<template>
  <div id="app">
    <NavBar />
    <b-row style="text-align: center; margin-top: 1rem;"><h1>{{title}} Flashcards</h1></b-row>
    <div id="content">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import NavBar from "@/components/NavBar.vue";

@Component({
  components: {
    NavBar
  }
})
export default class App extends Vue {
  get title(){
    const rnd = Math.random()
    console.log(rnd)
    return rnd>0.5?"میکارزو":"mikarezoo"
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
