<template>
  <div class="row card border-dark" style="margin-bottom: 1rem">
    <div class="card-header">
      <strong>Upload from file:</strong>
    </div>
    <div class="card-body">
      <div class="row mb-3 list-item-form">
        <label for="lang-match-search" class="col-sm-2 col-xl-1 col-form-label"
        >Deck</label
             >
        <div class="col-sm-10 col-xl-11">
          <b-form-select
            v-model="deck"
            :options="deckOpts"
            class="form-control form-control"
          />
        </div>
      </div>

      <FileUploader
        :endpoint="endpoint"
        placeholder=""
        uploadButtonText="Upload"
        maxSize="1e6"
        @uploadFinished="finishUpload"
        @uploadError="errorUpload"
        @uploadStarted="startUpload"
      />
      <div class="upload-result" style="margin-top: 1rem">
        <div
          class="alert alert-success"
          id="upload-success"
          v-if="uploadResult"
        >
          {{ uploadResult.success }} words added to the database
        </div>
        <div v-if="fileUploadErrors.length">
          <div
            class="alert alert-warning"
            id="file-upload-errors"
            v-if="fileUploadErrors.length"
          >
            The upload worked, but there was some previously existing words:
            <div v-for="(e, i) in fileUploadErrors" :key="i" class="card">
              <div class="card-body">
                <div>
                  <strong>In the file:</strong>{{ e.file.fa }} /
                  {{ e.file.fr }}
                </div>
                <div>
                  <strong>In the database:</strong>
                  {{ e.db.langs.map(e => e.text).join(" / ") }}
                  <strong>created on: </strong
                  >{{ new Date(e.db.created).toLocaleDateString() }}
                  {{ new Date(e.db.created).toLocaleTimeString() }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Mixins } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";

import FileUploader from "@/components/FileUploader.vue";
axios.defaults.baseURL = "/mikarezoo-flashcards";

@Component({
  components: {
    FileUploader,
  },
  mixins: [MathMixin],
})
export default class CardUploader extends Mixins(MathMixin) {
  uploadResult: any = null;
  deck: string | null = null;
  
  get endpoint(){
    return '/api/upload'+(this.deck?'?decks='+this.deck:'')
  }
  
  get fileUploadErrors() {
    return this.uploadResult ? this.uploadResult.errors_details : [];
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
}
</script>

<style scoped>
#file-upload-errors {
  background-color: #ffd;
  color: #444;
}

#upload-success {
  background-color: #efe;
  color: #444;
}
</style>
