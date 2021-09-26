<template>
  <div class="">
    <div class="row">
      <div class="col-6">
        <input v-model="deckFilter" class="" style="width: 100%" placeholder="filter decks...">
      </div>
      <div class="col-6" style="display: flex; justify-content: flex-start; align-items: center;">
        <b-form-checkbox
          v-model="decksOnlySelected"
          size="sm"
        >
          View only active
        </b-form-checkbox>
      </div>
    </div>
    <b-form-select
      multiple
      v-model="selectedDecks"
      :options="deckOptsFiltered"
      class="form-control form-control"
    />
  </div>
  </div>
</template>

<script lang="ts">
// import { Component, Prop, Vue } from "vue-property-decorator";
import { Component, Mixins, Prop, Watch } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import axios from "axios";
import { Card } from "@/types";

@Component({
  mixins: [MathMixin],
})
export default class DeckSelector extends Mixins(MathMixin) {
  @Prop({ default: () => [] })
  value!: string[];
  
  selectedDecks : string[] = [];
  decksOnlySelected = false;
  
  arraysIdentical(a, b){
    return (a||[]).every(e => ~(b||[]).indexOf(e)) && (b||[]).every(e => ~(a||[]).indexOf(e))
  }
  
  @Watch("value")
  valuechgd(v){
    if(!this.arraysIdentical(this.selectedDecks, v)){
      this.selectedDecks = v;
    }
  }
      
  @Watch("selectedDecks")
  sdkchgd(v){
    if(!this.arraysIdentical(this.value, v)){
      this.$emit('input', v);
    }
  }
      
  deckFilter = "";
  
  get deckFacette(){
    return new RegExp('.*' + (this.deckFilter||"").split(' ').join('.*') + '.*', 'i');
  }
  
  get deckOptsFiltered(){
    return this.deckOpts.filter(e => e.text.match(this.deckFacette) && (!this.decksOnlySelected || ~this.selectedDecks.indexOf(e.value)))
  }
  
  mounted(){
    this.selectedDecks = this.value;
  }
}
</script>

<style>
</style>
