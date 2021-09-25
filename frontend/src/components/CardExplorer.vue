<template>
  <div class="row card border-dark" style="margin-bottom: 1rem">
    <div class="card-header">
      <div><strong>Card Explorer</strong></div>

      <div
        class="container-fluid"
        @keyup.enter="fetchCards"
        v-on:submit.prevent
      >
        <div class="row">
          <label
            for="'searchcard"
            style=""
            class="col-sm-3 col-xl-2 col-form-label"
            >search:
          </label>
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

        <div class="row mb-3 list-item-form">
          <label for="lang-match-search" class="col-sm-2 col-form-label"
            >Deck</label
          >
          <div class="col-sm-10">
            <b-form-select
              v-model="deck"
              :options="deckOpts"
              class="form-control form-control"
              @change="fetchCards"
            />
          </div>
        </div>

        <div
          style="
            display: flex;
            justify-content: end;
            margin: 0 0.5rem;
            margin-top: 0.5rem;
          "
        >
          <button
            @click="fetchCards"
            class="btn btn-outline-secondary"
            type="button"
          >
            search
          </button>
        </div>
      </div>
      <b-row v-show="!editing">
        <b-pagination
          :disabled="!getLoggedIn"
          v-b-tooltip.hover :title="getLoggedIn?'':'Please login to access all features.'"
          class="pagination"
          style="display: flex; justify-content: center"
          v-model="currentPage"
          :total-rows="total_cards"
          :per-page="perPage"
        ></b-pagination>
      </b-row>
    </div>
    <div class="card-body">
      <transition-group name="listtr" tag="div" class="row" >

        <div
          class="listtr-item"
          :class="{'col-sm-6': !editing, 'col-md-4': !editing, 'col-lg-4': !editing, 'col-xl-3': !editing, 'col-md-12': editing}"
          v-for="c in cards.filter(e => !editing || e.id==editing )"
          :key="c.id"
          style="margin-bottom: 0.5rem"
        >
          <div class="card">
            <CardViewer :editable="getLoggedIn" :card="c" @deleted="fetchCards"  @editing="toggleEditing"/>
          </div>
        </div>
        
      </transition-group>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";
import CardViewer from "@/components/CardViewer.vue";

import _ from "lodash";
import { mapGetters } from "vuex";

@Component({
  components: {
    CardEditor,
    CardViewer,
  },
  mixins: [MathMixin],
  computed: mapGetters(["getLoggedIn"]),
})
export default class Home extends Mixins(MathMixin) {
  total_cards = 0;
  cards: Card[] = [];
  deck: string | null = null;
  perPage = 28;
  currentPage = 1;
  
  getLoggedIn!: boolean;

  editing: string | null = null;

  searchCard = "";

  toggleEditing(cardId, b){
    
    console.log("TOGGLE EDITING")
    console.log(cardId)
    console.log(b)
    this.editing = b ? cardId : null;
  }

  fetchCards() {
    console.log('DECK:')
    axios
    .get("/api/cards", {
      params: {
        first: this.perPage,
        offset: (this.currentPage - 1) * this.perPage,
        search: this.searchCard,
        deck: this.deck,
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
    this.fetchCards();
  }

  mounted() {
    this.fetchCards();
  }
}
</script>

<style scoped>
.listtr-item {
  transition: all .25s;
  display: inline-block;
}

/* .listtr-enter, .listtr-leave-to{
   opacity: 0;
   transform: rotate(0.1turn);
transform: translateX(-600px);
}
 */

.listtr-leave-to{
  opacity: 0;
  /* transform: rotate(0.1turn); */
  /* transform: translateX(-800px); */
}

.listtr-enter{
  opacity: 0;
  /* transform: rotate(0.1turn); */
  /* transform: translateX(100px); */
}

.listtr-leave-active {
  position: absolute;
}

</style>
