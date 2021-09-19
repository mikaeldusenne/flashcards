<template>
  <div class="container-fluid">
    
    <b-row class="row justify-content-md-center" style="margin: 1rem;" v-if="!training">
      <div class="col col-xl-4 col-lg-6 col-sm8 col-xs-12">
        <div class="card">
          <div class="card-body" style="margin-top: 0.5rem;">
            
            <div class="row mb-2 list-item-form">
              <label for="lang-match-search" class="col-sm-2 col-form-label">User</label>
              <div class="col-sm-10">
                <b-form-select
                  id="lang-match-search"
                  v-model="user"
                  :options="['Mikaël', 'آرزو']"
                  @change="getCard"
                  class="form-control form-control"
                />
              </div>
            </div>
            <div class="row mb-2 list-item-form">
              <label for="lang-match-search" class="col-sm-2 col-form-label">Language</label>
              <div class="col-sm-10">
                <b-form-select
                  id="lang-match-search"
                  v-model="showLang"
                  :options="langOpts"
                  class="form-control form-control"
                />
              </div>
            </div>
            <div style="display: flex; justify-content: end; margin: 0 0.5rem; margin-top: 0.5rem;">
              <button
                @click="startTrain"
                class="btn btn-outline-secondary"
                type="button"
              >
                Start
              </button>
            </div>
          </div>
        </div>
        <div class="row" style="margin-bottom: 1rem;">
          <em>{{cards.length}} cards.</em>
        </div>
      </div>
    </b-row>
    <b-row class="row justify-content-md-center" style="margin: 1rem;" v-if="training">
      <div class="col col-xl-4 col-lg-6 col-sm8 col-xs-12" v-if="currentCard">
        <div class="card">
          <div class="card-body" style="margin-top: 0.5rem;">
            <div id="question"> <h2>{{getQuestion(currentCard)}}</h2></div>
            
          </div>
          <div class="card-footer" v-if="!showResult">
            <div style="display: flex; justify-content: center; margin: 0 0.5rem; margin-top: 0.5rem;">
              <button
                @click="showResult = !showResult"
                class="btn btn-outline-primary btn-control-train"
                type="button"
              >
                {{showResult?'Hide':'View'}}
              </button>
            </div>
          </div>
        </div>
        
        <cardViewer
          :card="currentCard.card"
          :detailed="true" v-if="showResult"
          :langs="currentCard.card.langs.map(e => e.lang).filter(e => e != showLang)"
        />
        
        <div style="display: flex; justify-content: center; margin: 0 0.5rem; margin-top: 0.5rem;" v-if="showResult">
          <div v-for="difficulty in difficulties">
            <button
              @click="setDifficulty(difficulty)"
              class="btn btn-control-train"
              :class="{'btn-outline-secondary': difficulty!=selectedDifficulty, 'btn-secondary': difficulty==selectedDifficulty}"
              type="button"
            >
              {{difficulty}}
            </button>
            
          </div>

        </div>
        <!-- <cardViewer :card="currentCard.card" :detailed="true" :langs="currentCard.card.langs.map(e => e.lang).filter(e => e != showLang)"></cardViewer>
        -->
        <div style="display: flex; justify-content: end; margin: 0 0.5rem; margin-top: 0.5rem;">
          <!-- <button
               @click="showResult = !showResult"
               class="btn btn-outline-secondary btn-control-train"
               type="button"
               
               >
               {{showResult?'Hide':'View'}}
               </button> -->
          <!-- <button
               @click="moveCard(-1)"
               class="btn btn-outline-secondary btn-control-train"
               type="button"
               >
               Previous
               </button> -->
          <!-- <button
               @click="moveCard(+1)"
               class="btn btn-outline-secondary btn-control-train"
               type="button"
               >
               Next
               </button> -->
          <button
            @click="exitTrain"
            class="btn btn-outline-secondary btn-control-train"
            type="button"
          >
            Finish
          </button>
        </div>
        <!-- <div class="row">
             <div class="col col-xl-4" v-for="i in [0, 1, 2]">
             <strong>Bucket #{{i}}</strong>
             <div v-for="c in cards.filter(e => e.bucket==i )">
             {{c.card.langs.map(e => e.text).join('/')}}
             </div>
             
             </div>
             </div> -->

      </div>
    </b-row>
    
  </div>
</template>


<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import axios from 'axios'

import {Card} from "@/types";
import CardViewer from "@/components/CardViewer.vue"
axios.defaults.baseURL = '/mikarezoo-flashcards';
import _ from 'lodash';

@Component({
  components: {
    CardViewer,
  },
})
export default class Train extends Vue {
  training = false;
  showResult = false;
  
  selectedDifficulty = null;
  difficulties = ['easy', 'normal', 'hard']
  cards: any[] = [];
  langs: any[] = [];
  
  showLang = "fr"
  langOpts = [
    {
      text: "Français -> فارسی",
      value: "fr"
    },
    {
      text: "فارسی -> Français",
      value: "fa"
    },
  ];
  
  currentCard: any | null = null;
  
  uploadResult: any = null;
  user = "آرزو"
  
  newCard: Card = {id: "", langs: []};

  setDifficulty(e){
    this.selectedDifficulty = e;
    this.updateUserCard();
  }
  
  getQuestion(c){
    return c.card.langs.find(e => e.lang == this.showLang).text;
  }
  
  prettyLang(e){
    return this.langs.find(ee => ee.id==e).title || e;
  }

  startTrain(){
    this.nextCard();
    this.training = true;
  }
  
  exitTrain(){
    this.training = false;
  }
  
  moveCard(k){
    this.selectedDifficulty = null;
    // console.log('movecard ' + k)
    this.showResult = false;
    if(this.currentCard){
      const currentIndex = this.cards.map(e => e.card.id).indexOf(this.currentCard.card.id);
      const nextid = (k + currentIndex + this.cards.length) % this.cards.length;
      this.currentCard = this.cards[ nextid ];
    }else{
      console.log('init')
      this.currentCard = this.cards[0];
    }
  }
  
  nextCard(){
    this.selectedDifficulty = null;
    this.showResult = false;
    // this.moveCard(1)
    axios.get('/api/train-card', {params: {user: this.user, current: this.currentCard?this.currentCard.card.id:null}})
    .then(resp => {
      this.currentCard = resp.data.card;
      this.getCard()
    })
    .catch(console.log)
  }

  updateUserCard(){
    
    axios.post('/api/update-usercard', {
      user: this.user,
      card: this.currentCard.card.id,
      difficulty: this.selectedDifficulty,
    })
    .then(resp => {
      this.currentCard.bucket = resp.data.bucket;
      this.nextCard();
    })
    .catch(console.log)
  }
  
  getCard(){
    axios.get('/api/train-cards', {params: {user: this.user}})
    .then(resp => {
      console.log("cards:")
      console.log(resp.data)
      this.cards = resp.data.map(c => {
        c.showResult = false;
        return c;
      });
      // this.currentCard = this.cards[0];
    })
    .catch(console.log)
  }
  
  mounted(){
    this.getCard()
    axios.get('/api/langs')
    .then(resp => {
      console.log("langs:")
      console.log(resp.data)
      this.langs = resp.data;
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

#question{
  text-align: center;
  
}
.btn-control-train{
  margin-left: 0.5rem;
}
</style>
