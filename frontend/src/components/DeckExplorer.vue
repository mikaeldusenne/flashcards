<template>
  <div>
    <b-row style="text-align: center; justify-content: center; margin: 1.5rem 0;">
      <h1><strong>Decks</strong></h1>
    </b-row>
    <!-- <b-row style="text-align: center; justify-content: center; margin: 1.5rem 0;">

         <div>
         <verte v-model="cardcolor" :picker="wheel" :model="rgb" />
         </div>
         {{cardcolor}}
         </b-row> -->
    <b-row
      v-if="false"
      style="display: flex; justify-content: center; margin-bottom: 0;"
    >
      <b-pagination
        class="pagination pagination-sm"
        v-model="currentPage"
        style="margin-bottom: 0;"
        :total-rows="total_cards"
        :per-page="perPage"
      ></b-pagination>
    </b-row>
    <b-container fluid>
      <div id="cardgrid" v-show="!currentDeck">
        <div
          v-for="d in getDecks"
          :key="d._id"
        >
          <div class="card mb-3 mr-3 ml-3 border-green" style="border-radius: 0.5rem;"
          >
            <b-card-header
              style="min-height: 8rem; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; padding: 0rem 0.5rem; cursor: pointer; border-radius: 0.5rem 0.5rem 0 0;"
              @click="setCurrentDeck(d._id)"
              class="cardheader bg-green"
              
            >
              <div style="width: 100%; margin-top: 2rem;"><h4><strong>{{d.title}}</strong></h4></div>
              <div ><em>{{d.n_cards}} card{{d.n_cards>1?'s':''}}.</em></div>
              
            </b-card-header>
            <b-card-body
              style="text-align: center; padding: 1rem 0; min-height: 20rem;"
              class="cardbody"
            >
              <TableCardViewer :deck="d._id" />
            </b-card-body>
          </div>
        </div>
      </div>
      <div class="row" v-if="currentDeck">
        <div class="col-12" style="margin-bottom: 2rem;">
          <em style="text-decoration: underline; cursor: pointer" @click="setCurrentDeck(null)">< back</em>
        </div>
        <DeckDetails :deck="getDecks.find(e => e._id==currentDeck)" />
      </div>
    </b-container>
    
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";
import CardViewer from "@/components/CardViewer.vue";
import TableCardViewer from "@/components/TableCardViewer.vue";
import DeckDetails from "@/components/DeckDetails.vue";

import _ from "lodash";
import { mapGetters } from "vuex";

@Component({
  components: {
    CardEditor,
    CardViewer,
    TableCardViewer,
    DeckDetails,
  },
  mixins: [MathMixin],
  computed: mapGetters(["getLoggedIn", "getDecks"]),
})
export default class DeckExplorer extends Mixins(MathMixin) {
  
  total_cards = 0;
  perPage = 28;
  currentPage = 1;
  currentDeck: string | null= "";
  
  cards: any = {};
  
  setCurrentDeck(e){
    this.currentDeck = e;
  }
  
}
</script>

<style scoped>
#cardgrid{
  /* max-width: 20rem; */
  margin: 0 auto;
  display: grid;
  grid-gap: 1rem;
  align-items: stretch;
}

@media (min-width: 50rem) {
  #cardgrid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 70rem) {
  #cardgrid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 85rem) {
  #cardgrid { grid-template-columns: repeat(4, 1fr); }
}


#cardgrid > div > .card{
  /* border: 1px solid #0763da; */
  /* border: 1px solid #057a53; */
}

#cardgrid > div > .card > .cardheader{
  color: #fff;
  /* background-color: #021a15; */
  text-align: center;
  text-transform: uppercase;
}

</style>
