<template>
  <div class="container-fluid">
    
    <div class="row justify-content-md-center" style="margin: 1rem;" v-if="langs.length">
      <b-col sm="12" md="8" lg="6" xl="6" >
        <div class="row card" style="margin-bottom: 1rem;">
          <div class="card-header">
            <strong>Upload from file:</strong>
          </div>
          <div class="card-body">
            <FileUploader
              :endpoint="'/api/upload'"
              placeholder=""
              uploadButtonText="Upload"
              maxSize="1e6"
              @uploadFinished="finishUpload"
              @uploadError="errorUpload"
              @uploadStarted="startUpload"
            />
            <div class="upload-result" style="margin-top: 1rem;">
              <div class="alert alert-success" id="upload-success" v-if="uploadResult">
                {{uploadResult.success}} words added to the database
              </div>
              <div v-if="fileUploadErrors.length">
                <div class="alert alert-warning" id="file-upload-errors" v-if="fileUploadErrors.length">
                  The upload worked, but there was some previously existing words:
                  <div v-for="e, i in fileUploadErrors" :key="i" class="card">
                    <div class="card-body">
                      <div><strong>In the file:</strong>{{e.file.fa}} / {{e.file.fr}}</div>
                      <div>
                        <strong>In the database:</strong><span v-for="l, i in e.db.langs"> {{l.text}}{{i < e.db.langs.length-1?' / ':''}} </span>
                        <strong>created on: </strong>{{new Date(e.db.created).toLocaleDateString()}} {{new Date(e.db.created).toLocaleTimeString()}}
                      </div>
                      
                    </div>
                  </div>
                </div>
                
              </div>
            </div>
          </div>
        </div>
      </b-col>
    </div>
    
    <div class="row justify-content-md-center" style="margin: 1rem;" v-if="langs.length">
      <b-col sm="12" md="8" lg="6" xl="6" >
        <div class="row card" style="margin-bottom: 1rem;">
          <div class="card-header">
            <strong>Create a new card:</strong>
          </div>
          <div class="card-body">
            <CardEditor :card="newCard" textButton="Create" @saved="fetchCards" />
          </div>
        </div>
      </b-col>
    </div>
    
    <div class="row justify-content-md-center" style="margin: 1rem;">
      <b-col sm="12" md="8" lg="6" xl="6" >
        <div class="row card" style="margin-bottom: 1rem;">
          <div class="card-header">
            <div><strong>Card Explorer</strong></div>
            <div class="container-fluid" @keyup.enter="fetchCards" v-on:submit.prevent>
              <div class="row">
                <label for="'searchcard" style="" class="col-sm-3 col-xl-2 col-form-label">search: </label>
                <div class="col-sm-9 col-xl-10">
                  <input
                    id="searchcard"
                    type="text"
                    maxlength="75"
                    class="form-control"
                    placeholder="search"
                    v-model="searchCard"
                  />
                </div>
              </div>
              <div style="display: flex; justify-content: end; margin: 0 0.5rem; margin-top: 0.5rem;">
                <button
                  @click="fetchCards"
                  class="btn btn-outline-secondary"
                  type="button"
                >
                  search
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div >
              <div class="card" v-for="c in cards" :key="c.id" style="margin-bottom: 0.5rem;">
                <CardViewer :card="c" @deleted="fetchCards" />
              </div>
            </div>
          </div>
        </div>
      </b-col>
    </div>
    <b-row style="position: sticky; bottom: 0; z-index: 9000;">
      <b-pagination
        class="pagination"
        style="display: flex; justify-content: center;"
        v-model="currentPage"
        :total-rows="total_cards"
        :per-page="perPage"
      ></b-pagination>
    </b-row>

  </div>
</template>


<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import axios from 'axios'

import {Card} from "@/types";
import CardEditor from "@/components/CardEditor.vue"
import CardViewer from "@/components/CardViewer.vue"
import FileUploader from "@/components/FileUploader.vue"
axios.defaults.baseURL = '/mikarezoo-flashcards';
import _ from 'lodash';

@Component({
  components: {
    CardEditor,
    CardViewer,
    FileUploader,
  },
})
export default class Home extends Vue {
  total_cards = 0;
  cards: Card[] = [];
  langs: any[] = [];
  
  perPage = 25;
  currentPage = 1;
  
  uploadResult: any = null;
  
  get fileUploadErrors(){
    return this.uploadResult ? this.uploadResult.errors_details : []
  }
  
  searchCard = ""
  
  newCard: Card = {id: "", langs: []};
  
  prettyLang(e){
    return this.langs.find(ee => ee.id==e).title || e;
  }
  
  setupNewCard(){
    this.langs.forEach(lang => {
      if(this.newCard.langs.find(e => e.lang == lang.id) == undefined){
        this.newCard.langs.push({
          lang: lang.id, 
          text: "",
          comment: "",
          // examples: [],
        })
      }
    })
  }
  
  finishUpload(resp){
    console.log('upload finished')
    this.uploadResult = resp
  }
  
  startUpload(){
    this.uploadResult = null;
    console.log('upload started')
  }
  
  errorUpload(){
    console.log('upload error')
  }
  addCard(){
    console.log("add card")
    axios.post("/api/add-card", this.newCard).then(console.log).catch(console.log)
  }
  
  fetchCards(){
    axios.get('/api/cards', {params: {
      first: this.perPage,
      offset: (this.currentPage-1) * this.perPage,
      search: this.searchCard
    }})
    .then(resp => {
      console.log("cards:")
      console.log(resp.data)
      this.total_cards = resp.data.n;
      this.cards = resp.data.cards.map(e => {
        e.langs = _.sortBy(e.langs, [ee => ee.lang])
        return e;
      })
    })
    .catch(console.log)
  }

  @Watch('currentPage')
  cpchgd(v, oldv){
    // console.log(`current page changed ${oldv} -> ${v}`)
    this.fetchCards();
  }

  
  mounted(){
    this.fetchCards()
    axios.get('/api/langs')
    .then(resp => {
      console.log("langs:")
      console.log(resp.data)
      this.langs = resp.data;
      this.setupNewCard();
    })
    .catch(console.log)
  }
  
}
</script>

<style>
body{
  background: #f9f9f9;
}
.nav-tabs .nav-link.active{
  background: #f9f9f9;
}
.cardlangtitle{
  padding: 0 1rem;
}

#file-upload-errors{
  background-color: #ffd;
  color: #444;
}

#upload-success{
  background-color: #efe;
  color: #444;
}
</style>
