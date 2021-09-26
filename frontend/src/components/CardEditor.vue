<template>
  <!-- @keyup.enter="saveCard" -->
  <div class="container-fluid form" v-on:submit.prevent>
    <div class="row mb-3 list-item-form">
      <label for="lang-match-search" class="col-sm-2 col-form-label"
      >Deck</label
           >
      <div class="col-sm-10">
        <DeckSelector v-model="card.decks" />
      </div>
    </div>
    <div class="row mb-3 list-item-form">
      <label for="lang-match-search" class="col-sm-2 col-form-label"
      >Difficulty</label
                 >
      <div class="col-sm-10">
        <b-form-rating v-model="card.difficulty"
                       icon-empty="journal"
                       icon-half="journal-minus"
                       icon-full="journal-text"
                       variant="dark"
                       stars="5"
                       show-value precision="1"></b-form-rating>
      </div>
    </div>
    <div class="row mb-3 list-item-form">
      <label for="lang-match-search" class="col-sm-2 col-form-label"
      >Importance</label
                 >
      <div class="col-sm-10">
        <b-form-rating v-model="card.importance"
                       icon-empty="chat"
                       icon-half="chat-text"
                       icon-full="chat-text-fill"
                       variant="success"
                       stars="5"
                       show-value precision="1"></b-form-rating>
      </div>
    </div>

    <div v-for="l in card.langs" :key="l.id">
      <hr v-if="showAdvanced" />
      <div class="row mb-3">
        <label
          :for="'searchform-' + l.lang"
          style=""
          class="col-sm-4 col-xl-3 col-form-label"
        ><strong>{{ prettyLang(l.lang) }}</strong></label
        >
        <div class="col-sm-8 col-xl-9">
          <input
            :id="'searchform-' + l.lang"
            type="text"
            maxlength="75"
            class="form-control"
            :placeholder="'translation in ' + prettyLang(l.lang)"
            v-model="l.text"
          />
        </div>
      </div>
      <div class="row mb-3" v-show="showAdvanced">
        <label
          :for="'commentform-' + l.lang"
          style=""
          class="col-sm-4 col-xl-3 col-form-label"
          >comment</label
        >
        <div class="col-sm-8 col-xl-9">
          <textarea
            :id="'commentform-' + l.lang"
            v-model="l.comment"
            rows="2"
            class="form-control"
            :placeholder="'comment for ' + prettyLang(l.lang)"
          />
        </div>
      </div>
    </div>
    <div class="" style="display: flex; justify-content: center">
      <div style="display: flex; justify-content: center; margin: 0 0.5rem">
        <button
          @click="saveCard"
          class="btn btn-outline-primary"
          type="button"
        >
          {{ textButton }}
        </button>
      </div>
      <div style="display: flex; justify-content: center; margin: 0 0.5rem">
        <button
          @click="$emit('saved')"
          class="btn btn-outline-secondary"
          type="button"
        >
          Cancel
        </button>
      </div>
      <div
        style="display: flex; justify-content: center; margin: 0 0.5rem"
        v-if="card.id"
      >
        <button
          @click="deleteCard"
          class="btn btn-outline-danger"
          type="button"
        >
          Delete
        </button>
      </div>
    </div>
    <div style="display: flex; justify-content: end">
      <em
        style="text-decoration: underline; cursor: pointer; color: #888"
        @click="showAdvanced = !showAdvanced"
        >show {{ showAdvanced ? "basic" : "advanced" }} mode</em
      >
    </div>
  </div>
</template>

<script lang="ts">
// import { Component, Prop, Vue } from "vue-property-decorator";
import { Component, Mixins, Prop, Watch } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";
import DeckSelector from "@/components/deckSelector.vue";


@Component({
  components: {
    DeckSelector
  },
  mixins: [MathMixin],
})
export default class CardEditor extends Mixins(MathMixin) {
  @Prop({ default: "Save" })
  textButton!: string;

  @Prop({ default: false })
  isNew!: boolean;

  @Prop()
  card!: Card;
  
  @Prop({default: true})
  showAdvancedDefault!: boolean;
  
  showAdvanced = false;
  deckFilter = "";
  
  @Watch("showAdvancedDefault")
  advchgd(v){
    this.showAdvanced = v;
  }
  
  langs: any[] = [
    { id: "fr", title: "Français" },
    { id: "fa", title: "فارسی" },
  ];

  saveCard() {
    console.log("add card");
    axios
      .post("/api/add-card", { card: this.card, isNew: this.isNew })
      .then(() => {
        this.$emit("saved");
      })
      .catch((err) => {
        console.log(err.response.data.card);
        this.$emit("error", err.response.data.card);
        this.$toast.error(
          `This card already exists! ${err.response.data.card.langs
            .map((e) => e.text)
            .join(" / ")}`
        );
      });
  }

  deleteCard() {
    console.log("delete card");
    axios
      .post("/api/delete-card", this.card)
      .then(() => {
        this.$emit("deleted");
      })
      .catch(console.log);
  }

  mounted(){
    this.showAdvanced = this.showAdvancedDefault;
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
</style>
