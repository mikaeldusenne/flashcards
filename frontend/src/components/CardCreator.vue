<template>
  <div class="row card border-dark" style="margin-bottom: 1rem">
    <div class="card-header">
      <strong>Create a new card:</strong>
    </div>
    <div class="card-body">
      <CardEditor
        :isNew="true"
        :card="newCard"
        textButton="Create"
        @saved="resetCard"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Watch } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";

import { Card } from "@/types";
import CardEditor from "@/components/CardEditor.vue";

@Component({
  components: {
    CardEditor,
  },
  mixins: [MathMixin],
})
export default class CardCreator extends Mixins(MathMixin) {
  newCard: Card = { id: "", langs: [] };

  setupNewCard() {
    this.getLangs.forEach((lang) => {
      if (this.newCard.langs.find((e) => e.lang == lang.id) == undefined) {
        this.newCard.langs.push({
          lang: lang.id,
          text: "",
          comment: "",
          // examples: [],
        });
      }
    });
  }
  
  resetCard(){
    this.$toast.success(`card ${this.newCard.langs.map(e => e.text).join(' / ')} created!`)
    this.newCard.langs = this.newCard.langs.map(e => {
      e.text = "";
      return e;
    })
  }
  
  @Watch("getLangs")
  lgschgd() {
    this.setupNewCard();
  }
  
  mounted(){
    this.setupNewCard();
  }
  
}
</script>

<style></style>
