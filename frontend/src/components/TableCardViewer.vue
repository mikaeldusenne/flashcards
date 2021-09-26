<template>
  <div>
    <div :style="{'max-height': maxHeight, 'overflow-y': 'auto'}">
      <table class="table table-sm">
        <thead>
          <th style="text-align: right">
            fa
          </th>
          <th style="text-align: left">
            fr
          </th>
          <th>
            <b-icon-journal-text variant="dark" />
          </th>
          <th>
            <b-icon-chat-text-fill variant="success" />
          </th>
          
        </thead>
        <tbody>
          <tr v-for="c in tableView(cards)" :key="c.fr">
            <td style="text-align: right">{{c.fa}}</td>
            <td style="text-align: left">{{c.fr}}</td>
            <td>{{c.difficulty}}</td>
            <td>{{c.importance}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-row
      v-show="total_cards > perPage"
      style="display: flex; justify-content: center; margin-bottom: 0; "
    >
      <b-pagination
        class="pagination pagination-sm"
        v-model="currentPage"
        style="margin-bottom: 0;"
        :total-rows="total_cards"
        :per-page="perPage"
      ></b-pagination>
    </b-row>

  </div>
</template>

<script lang="ts">
import { Component, Mixins, Watch, Prop } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";
import CardViewer from "@/components/CardViewer.vue";

import _ from "lodash";

@Component({
  components: {
    CardEditor,
    CardViewer,
  },
  mixins: [MathMixin],
})
export default class DeckExplorer extends Mixins(MathMixin) {
  @Prop({default: null})
  deck!: string | null;
  
  @Prop({default: "20rem"})
  maxHeight!: string;
  
  @Prop({default: 5})
  perPage!: number;
  
  total_cards = 0;
  currentPage = 1;
  currentDeck: string | null= "";
  
  cards: Card[] = [];
  
  tableView(cs){
    return (cs || []).map(c => {
      const d: any = {}
      d.fa = c.langs.find(e => e.lang=="fa").text
      d.fr = c.langs.find(e => e.lang=="fr").text
      d.difficulty = c.difficulty
      d.importance = c.importance
      return d;
    })
  }

  @Watch("deck")
  dkchgd(){
    this.fetchDeckCards();
  }
  
  @Watch("currentPage")
  pgchgd(){
    this.fetchDeckCards();
  }
  
  fetchDeckCards(){
    axios.get("/api/cards", {params: {
      first: this.perPage,
      offset: (this.currentPage-1) * this.perPage,
      deck: this.deck,
    }})
    .then(e => {
      this.cards = e.data.cards;
      this.total_cards = e.data.n;
      console.log(this.cards)
    })
    .catch(console.log)
  }
  
  mounted() {
    this.fetchDeckCards();
  }
}
</script>

<style>

</style>
