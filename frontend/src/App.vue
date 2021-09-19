<template>
  <div id="app">
    <NavBar />
    <b-row style="text-align: center; margin-top: 1rem"
      ><h1>{{ title }} Flashcards</h1></b-row
    >
    <div id="content">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

@Component({
  components: {
    NavBar,
  },
})
export default class App extends Vue {
  get title() {
    return Math.random() > 0.5 ? "میکارزو" : "Mikarezoo";
  }
  mounted() {
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
