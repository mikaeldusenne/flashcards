<template>
  <LoginMessage>
    <div class="container-fluid">
      <b-row
        class="row justify-content-md-center"
        style="margin: 1rem"
        v-if="!training"
      >
        <div class="col-xl-6 col-lg-8 col-sm-12 col-xs-12">
          <div class="card">
            <div class="card-body" style="margin-top: 0.5rem">
              <!-- <div class="row mb-2 list-item-form">
                   <label for="lang-match-search" class="col-sm-3 col-form-label"
                   >User</label
                   >
                   <div class="col-sm-9">
                   <b-form-select
                   id="lang-match-search"
                   v-model="user"
                   :options="['Mikaël', 'آرزو']"
                   @change="getCards"
                   class="form-control form-control"
                   />
                   </div>
                   </div> -->

              <div class="row mb-3 list-item-form">
                <label for="lang-match-search" class="col-sm-3 col-form-label"
                >Deck</label
                     >
                <div class="col-sm-9">
                  <b-form-select
                    v-model="deck"
                    :options="deckOpts"
                    @change="getCards"
                    class="form-control form-control"
                  />
                </div>
              </div>

              <div class="row mb-2 list-item-form">
                <label for="lang-match-search" class="col-sm-3 col-form-label"
                >Language</label
                         >
                <div class="col-sm-9">
                  <b-form-select
                    id="lang-match-search"
                    v-model="showLang"
                    :options="langOpts"
                    class="form-control form-control"
                  />
                </div>
              </div>
              <div
                class="row"
                style="
                       display: flex;
                       justify-content: end;
                       margin: 0 0.5rem;
                       margin-top: 1rem;
                       "
              >
                <div style="display: flex; align-items: center; margin: 0 1rem;"><em>{{ cards.length }} cards.</em></div>
                <button
                  @click="startTrain"
                  class="btn btn-primary"
                  type="button"
                >
                  Start
                </button>
              </div>
            </div>
          </div>
          <div class="row" style="margin-bottom: 1rem">
          </div>
        </div>
      </b-row>
      
      <b-row class="row justify-content-md-center" v-if="showSession">
        <div class="col col-xs-10 col-lg-6 col-xl-4">
          <div class="card card-dark-border">
            <div class="card-body">
              <div class="alert alert-success">Félicitations! Session terminée.</div>
              <div><strong>Résultats:</strong></div>
              <Barplot :xdata="sessionPlot.keys" :ydata="sessionPlot.values" />
              
              <div><strong>Overall card repartition {{deck?`for the deck "${deckTitle}"`:''}}:</strong></div>
              <em>Shows how many cards should be shown often, moderately, or rarely based on your feedback during all your trainings</em>
              <Barplot :xdata="['often', 'moderately', 'rarely']" :ydata="Object.values(bucketCount)" />
              <!-- <div style="padding: 1rem; border: 1px solid #ccc; max-height: 15rem; overflow: auto;">
                   <div class="row" v-for="c in cards" :key="c.id" style="margin-bottom: 0">
                   {{prettyCardTitle(c.card)}}: {{c.bucket}}
                   </div>
                   </div> -->
            </div>
          </div>
        </div>
      </b-row>
      
      <b-row
        class="row justify-content-md-center"
        style="margin: 1rem"
        v-if="training"
      >
        
        <div
          style="
                 display: flex;
                 justify-content: center;
                 margin: 0 0.5rem;
                 margin-bottom: 0.5rem;
width: 100%;
                 "
          v-if="showResult"
        >
          <div v-for="difficulty in difficulties" :key="difficulty">
            <button
              @click="setDifficulty(difficulty)"
              class="btn btn-control-train"
              :class="{
                'btn-outline-secondary': difficulty != selectedDifficulty,
                'btn-secondary': difficulty == selectedDifficulty,
              }"
              type="button"
            >
              {{ difficulty }}
            </button>
          </div>
        </div>

        
        <div class="col col-xl-4 col-lg-6 col-sm8 col-xs-12" v-if="currentCard">
          <div class="card" v-if="!showResult">
            <div class="card-body" style="margin-top: 0.5rem">
              <div id="question">
                <h2>{{ getQuestion(currentCard) }}</h2>
              </div>
            </div>
            <div class="card-footer" v-if="!showResult">
              <div
                style="
                       display: flex;
                       justify-content: center;
                       margin: 0 0.5rem;
                       margin-top: 0.5rem;
                       "
              >
                <button
                  @click="showResult = !showResult"
                  class="btn btn-outline-primary btn-control-train"
                  type="button"
                >
                  {{ showResult ? "Hide" : "View" }}
                </button>
              </div>
            </div>
          </div>
          <cardViewer
            v-else
            :card="currentCard.card"
            :detailed="true"
          />

          
          
          <div
            style="
                   display: flex;
                   justify-content: end;
                   margin: 0 0.5rem;
                   margin-top: 0.5rem;
                   "
          >
            <button
              @click="exitTrain"
              class="btn btn-outline-secondary btn-control-train"
              type="button"
            >
              Finish
            </button>
          </div>
        </div>
      </b-row>
    </div>  
  </LoginMessage>
</template>

<script lang="ts">
import { Component, Mixins } from "vue-property-decorator";
import MathMixin from "@/MathMixin";


import axios from "axios";
import CardViewer from "@/components/CardViewer.vue";
import Barplot from "@/components/Barplot.vue";
import LoginMessage from "@/components/LoginMessage.vue";
axios.defaults.baseURL = "/mikarezoo-flashcards";

import _ from "lodash";

interface Session{
  easy: number;
  normal: number;
  hard: number;
}

@Component({
  components: {
    CardViewer,
    Barplot,
    LoginMessage,
  },
  mixins: [MathMixin],
})
export default class Train extends Mixins(MathMixin) {
  training = false;
  showResult = false;

  showSession = false;
  session : Session = {easy: 10, normal: 20, hard: 15}
  
  newSession(){
    this.session = {easy: 0, normal: 0, hard: 0}
  }

  get sessionPlot(){
    const keys = ["hard", "normal", "easy"]
    return {keys: keys, values: keys.map(e => this.session[e])}
  }
  
  deck: string | null = null;
  selectedDifficulty = null;
  difficulties = ["easy", "normal", "hard"];
  cards: any[] = [];
  langs: any[] = [];

  get deckTitle(){
    if(this.deck == null){
      return null
    }else{
      return (this.deckOpts.find(e => e.value)||{}).text
    }
  }

  showLang = null;
  langOpts = [
    {
      text: "random",
      value: null,
    },
    {
      text: "Français -> فارسی",
      value: "fr",
    },
    {
      text: "فارسی -> Français",
      value: "fa",
    },
  ];

  currentCard: any | null = null;

  uploadResult: any | null = null;
  user = "آرزو";

  setDifficulty(e) {
    this.selectedDifficulty = e;
    this.session[e] += 1;
    this.updateUserCard();
  }

  get bucketCount(){
    return this.cards.map(e => e.bucket).reduce((acc, e) => {
      acc[e] = (acc[e] || 0) + 1
      return acc
    }, [])
  }

  getQuestion(c) {
    if(this.showLang == null){
      const rnd = Math.random()
      const len = c.card.langs.length
      return c.card.langs[Math.floor(rnd * len)].text;
    }else{
      return c.card.langs.find((e) => e.lang == this.showLang).text;
    }
  }

  prettyLang(e) {
    return this.langs.find((ee) => ee.id == e).title || e;
  }

  startTrain() {
    this.showSession = false;
    this.newSession();
    this.nextCard();
    this.training = true;
  }

  exitTrain() {
    this.training = false;
    this.showSession = true;
  }


  nextCard() {
    this.selectedDifficulty = null;
    this.showResult = false;
    // this.moveCard(1)
    axios
    .get("/api/train-card", {
      params: {
        user: this.user,
        current: this.currentCard ? this.currentCard.card.id : null,
        deck: this.deck,
      },
    })
    .then((resp) => {
      this.currentCard = resp.data.card;
      this.getCards();
    })
    .catch(console.log);
  }

  updateUserCard() {
    axios
    .post("/api/update-usercard", {
      user: this.user,
      card: this.currentCard.card.id,
      difficulty: this.selectedDifficulty,
    })
    .then((resp) => {
      this.currentCard.bucket = resp.data.bucket;
      this.nextCard();
    })
    .catch(console.log);
  }

  getCards() {
    axios
    .get("/api/train-cards", { params: { user: this.user, deck: this.deck } })
    .then((resp) => {
      console.log("cards:");
      console.log(resp.data);
      this.cards = resp.data.map((c) => {
        c.showResult = false;
        return c;
      });
      // this.currentCard = this.cards[0];
    })
    .catch(console.log);
  }

  mounted() {
    if(this.$route.query.deck){
      const deck: string = (this.$route.query.deck as string);
      this.deck=deck;
    }
        
    this.getCards();
    axios
    .get("/api/langs")
    .then((resp) => {
      console.log("langs:");
      console.log(resp.data);
      this.langs = resp.data;
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

#question {
  text-align: center;
}
.btn-control-train {
  margin-left: 0.5rem;
}
</style>
