<template>
  <div class="container-fluid">
    {{getUser}}
    <div class="row justify-content-md-center" style="margin: 1rem">
      <b-col sm="12" md="10" lg="10" xl="8">
        <b-tabs content-class="mt-3" lazy>
          <b-tab title="Explore">
            <CardExplorer />
          </b-tab>
          <b-tab title="Create">
            <LoginMessage><CardCreator/></LoginMessage>
          </b-tab>
          <b-tab title="Import from csv">
            <LoginMessage><CardUploader /></LoginMessage>
          </b-tab>
        </b-tabs>
      </b-col>
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
