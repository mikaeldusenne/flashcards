<template>
  <div class="container-fluid">
    <div
      class="row justify-content-md-center"
      style="margin: 1rem"
      v-if="langs.length"
    >
      <b-col sm="12" md="8" lg="6" xl="6">
        <CardUploader />
      </b-col>
    </div>

    <div
      class="row justify-content-md-center"
      style="margin: 1rem"
      v-if="langs.length"
    >
      <b-col sm="12" md="8" lg="6" xl="6">
        <CardCreator />
      </b-col>
    </div>

    <div class="row justify-content-md-center" style="margin: 1rem">
      <b-col sm="12" md="8" lg="6" xl="6">
        <CardExplorer />
      </b-col>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import axios from "axios";

import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";
import CardCreator from "@/components/CardCreator.vue";
import CardUploader from "@/components/CardUploader.vue";
import CardExplorer from "@/components/CardExplorer.vue";
import CardViewer from "@/components/CardViewer.vue";
axios.defaults.baseURL = "/mikarezoo-flashcards";
import _ from "lodash";

@Component({
  components: {
    CardEditor,
    CardViewer,
    CardUploader,
    CardExplorer,
    CardCreator,
  },
})
export default class Home extends Vue {
  total_cards = 0;
  cards: Card[] = [];
  langs: any[] = [];

  perPage = 25;
  currentPage = 1;

  uploadResult: any = null;

  get fileUploadErrors() {
    return this.uploadResult ? this.uploadResult.errors_details : [];
  }

  searchCard = "";

  newCard: Card = { id: "", langs: [] };

  prettyLang(e) {
    return this.langs.find((ee) => ee.id == e).title || e;
  }

  setupNewCard() {
    this.langs.forEach((lang) => {
      if (this.newCard.langs.find((e) => e.lang == lang.id) == undefined) {
        this.newCard.langs.push({
          lang: lang.id,
          text: "",
          comment: "",
          // examples: [],
        });
      }
    });
  }

  finishUpload(resp) {
    console.log("upload finished");
    this.uploadResult = resp;
  }

  startUpload() {
    this.uploadResult = null;
    console.log("upload started");
  }

  errorUpload() {
    console.log("upload error");
  }
  addCard() {
    console.log("add card");
    axios
      .post("/api/add-card", this.newCard)
      .then(console.log)
      .catch(console.log);
  }

  fetchCards() {
    axios
      .get("/api/cards", {
        params: {
          first: this.perPage,
          offset: (this.currentPage - 1) * this.perPage,
          search: this.searchCard,
        },
      })
      .then((resp) => {
        console.log("cards:");
        console.log(resp.data);
        this.total_cards = resp.data.n;
        this.cards = resp.data.cards.map((e) => {
          e.langs = _.sortBy(e.langs, [(ee) => ee.lang]);
          return e;
        });
      })
      .catch(console.log);
  }

  @Watch("currentPage")
  cpchgd() {
    // console.log(`current page changed ${oldv} -> ${v}`)
    this.fetchCards();
  }

  mounted() {
    this.fetchCards();
    axios
      .get("/api/langs")
      .then((resp) => {
        console.log("langs:");
        console.log(resp.data);
        this.langs = resp.data;
        this.setupNewCard();
      })
      .catch(console.log);
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
