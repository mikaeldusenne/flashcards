<template>
  <div>
    <b-row
      v-if="false"
      style="display: flex; justify-content: center; margin-bottom: 0;"
    >
      <b-pagination
        class="pagination"
        v-model="currentPage"
        style="margin-bottom: 0;"
        :total-rows="total_cards"
        :per-page="perPage"
      ></b-pagination>
    </b-row>
    <b-container fluid>
      <div class="row row-eq-height" v-show="!currentDeck">
        <div
          class="col-sm-12 col-md-6 col-lg-4 col-xl-4"
          v-for="d in getDecks"
          :key="d._id"
        >
          <div class="card"
          >
            <b-card-header
              style="min-height: 10rem; display: flex; align-items: center; justify-content: center; padding: 2rem; cursor: pointer;"
              @click="setCurrentDeck(d._id)"
            >
              <h2><strong>{{d.title}}</strong></h2>
              
            </b-card-header>
            <b-card-body style="text-align: center; padding: 1rem 0;">
              {{d.n_cards}} card{{d.n_cards>1?'s':''}}
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

<style scoped></style>
