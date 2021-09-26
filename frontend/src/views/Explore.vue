<template>
  <div class="container-fluid">
    <div class="row" style="margin: 1rem; display: flex; justify-content: center;">
      <DeckExplorer />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";

import CardEditor from "@/components/CardEditor.vue";
import CardCreator from "@/components/CardCreator.vue";
import CardUploader from "@/components/CardUploader.vue";
import CardExplorer from "@/components/CardExplorer.vue";
import DeckExplorer from "@/components/DeckExplorer.vue";
import CardViewer from "@/components/CardViewer.vue";
import LoginMessage from "@/components/LoginMessage.vue";
axios.defaults.baseURL = "/mikarezoo-flashcards";
import { mapGetters } from "vuex";

@Component({
  components: {
    CardEditor,
    CardViewer,
    CardUploader,
    CardExplorer,
    DeckExplorer,
    CardCreator,
    LoginMessage,
  },
  computed: mapGetters(["getLoggedIn", "getUser"]),

})
export default class Explore extends Vue {
  getLoggedIn!: boolean;
  getUser!: any;
}
</script>

<style>
body {
  background: #f9f9f9;
}
.nav-tabs .nav-link.active {
  background: #f9f9f9;
}
.cardlangtitle {
  padding: 0 1rem;
}

#file-upload-errors {
  background-color: #ffd;
  color: #444;
}

#upload-success {
  background-color: #efe;
  color: #444;
}
</style>
