<template>
  <b-container>
    <b-row class="alert alert-info bg-green text-light" style="justify-content: center;">
      <h4 style="margin: 1rem 0; text-align: center;"><strong>{{deck.title}}</strong></h4>
    </b-row>
    <b-row style="justify-content: center; margin: 2rem 0;">
      <b-card style="width: 100%;">
        <b-card-title>
          <strong>My statistics on this Deck</strong>
        </b-card-title>
        <b-card-body style="padding-bottom: 0;">
          <LoginMessage>
            <div>
              <div>
                coming soon
              </div>
              <div style="margin: 1rem 0;">
                <router-link class="router-link-decorated" :to="{path: '/train', query: { deck: deck._id }}">Practice ></router-link>
              </div>
            </div>
          </LoginMessage>
        </b-card-body>
      </b-card>
    </b-row>
    <b-row
      style="display: flex; justify-content: center; margin-bottom: 0; position: sticky; top: 0;"
      v-show="total_cards > perPage"
    >
      <b-pagination
        class="pagination"
        v-model="currentPage"
        style="margin-bottom: 0; "
        :total-rows="total_cards"
        :per-page="perPage"
      ></b-pagination>
    </b-row>
    <b-row id="accordion" style="margin-top: 0.5rem; justify-content: center;">
      <b-col cols="8" v-for="c, i in cards" :key="c.fr">
        <div class="card" style="width: 100%">
          <div class="card-header" :id="'heading-'+i"
               style="cursor: pointer; display: flex; align-items: center; justify-content: space-between;"
               @click="c.opened = !c.opened">
            <div>
            <button class="btn">
              <h4><strong>{{prettyCardTitle(c.card)}}</strong></h4>
            </button>
            </div>
            <div style="display: inline-block;"><span v-if="getUser.admin" @click="toggleEditing(c)"><b-icon-pen-fill /></span></div>
          </div>
          <div class="card-body" v-if="c.editing"> <CardEditor :card="c.card" @saved="finishEditing(c)"></CardEditor> </div>
          <div class="card-body" v-else v-show="c.opened">
            <div class="container-fluid">
              <div class="row mb-3">
                <label for="lang-match-search" class="col-sm-2 col-form-label"
                >Difficulty</label
                           >
                <div class="col-sm-10">
                  <b-form-rating v-model="c.card.difficulty"
                                 icon-empty="journal"
                                 icon-half="journal-minus"
                                 icon-full="journal-text"
                                 variant="dark"
                                 readonly
                                 stars="5"
                                 show-value precision="1"></b-form-rating>
                </div>
              </div>
              <div class="row mb-3">
                <label for="lang-match-search" class="col-sm-2 col-form-label"
                >Importance</label
                           >
                <div class="col-sm-10">
                  <b-form-rating v-model="c.card.importance"
                                 icon-empty="chat"
                                 icon-half="chat-text"
                                 icon-full="chat-text-fill"
                                 variant="success"
                                 readonly
                                 stars="5"
                                 show-value precision="1"></b-form-rating>
                </div>
              </div>
            </div>
            <div style="margin: 1rem;">
              <hr>
              <div style="margin: 1rem 0;"><strong>Comments:</strong></div>
              <div v-for="comment in c.card.langs.map(e => e.comment).filter(e=>e)">
                <pre>{{comment}}</pre>
              </div>
            </div>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script lang="ts">
import { Component, Mixins, Watch, Prop } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";
import CardViewer from "@/components/CardViewer.vue";
import LoginMessage from "@/components/LoginMessage.vue";

import _ from "lodash";
import { mapGetters } from "vuex";

@Component({
  components: {
    CardEditor,
    CardViewer,
    LoginMessage,
  },
  mixins: [MathMixin],
  computed: mapGetters(["getLoggedIn", "getUser"]),
})
export default class DeckDetails extends Mixins(MathMixin) {
  @Prop()
  deck: any;
  
  total_cards = 0;
  perPage = 10;
  currentPage = 1;
  currentDeck: string | null= "";
  
  cards: any[] = [];
  
  setCurrentDeck(e){
    this.currentDeck = e;
  }
  


  @Watch("currentPage")
  pgchgd(){
    this.fetchDeckCards();
  }

  fetchDeckCards(){
    axios.get("/api/cards", {params: {
      first: this.perPage,
      offset: (this.currentPage-1) * this.perPage,
      deck: this.deck._id,
    }})
    .then(e => {
      this.cards = e.data.cards.map(c => {
        return {
          card: c,
          opened: false,
          editing: false,
        }
      });
      console.log('CARDS')
      console.log(this.cards)
      this.total_cards = e.data.n;
      console.log(this.cards)
    })
    .catch(console.log)

  }
  
  toggleEditing(c){
    c.editing=!c.editing
  }
  
  finishEditing(c){
    c.editing=false;
    this.fetchDeckCards();
  }
  
  mounted() {
    this.fetchDeckCards();
  }
}
</script>

<style scoped>
</style>
