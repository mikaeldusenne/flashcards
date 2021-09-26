<template>
  <div class="container" style="max-width: 80%;">
    <div class="row" style="margin: 10rem 0; display: flex; justify-content: space-between;">
      <div class="col-md-6 col-xs-12">
          <b-row style="display: fluid; justify-content: center;" class="mr-4">
            <img src="./azadi_eiffel_tower.png" style="max-height: 10rem;">
          </b-row>
          <h1 style="font-weight: 600; font-size: 6rem; text-align: center;" class="mr-4">
              French with {{ title }}
            </h1>
      </div>
      <div class="col-md-6 col-xs-12" style="display: flex; align-items: center;">
        <b-container fluid class="ml-4">
          
          <b-row>
            <p style="font-size: 1.4rem;">Learn French with native speakers in both Farsi and French, working together to offer you polished content adapted to all levels.</p>
          </b-row>
          <b-row style="justify-content: center; margin-top: 2rem;">
            <button class="btn btn-outline-primary" style="font-size: 2rem;" @click="$router.push('explore')">Get Started</button>
          </b-row>
          
        </b-container>
        
      </div>
      
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
    CardCreator,
    LoginMessage,
  },
  computed: mapGetters(["getLoggedIn", "getUser"]),

})
export default class Home extends Vue {
  getLoggedIn!: boolean;
  getUser!: any;

  get title() {
    return Math.random() > 0.5 ? "میکارزو" : "Mikarezoo";
  }

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
