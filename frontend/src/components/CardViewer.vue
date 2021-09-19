<template>
  <div class="card card-viewer">
    <div class="card-body" style="text-align: center; padding: 0.5rem">
      <div class="card-viewer-title" style="margin: 0.5rem;" :class="{editable: editable}" @click="editing=!editing"
           v-if="!detailed"
      >
        <strong><span v-for="l, i in displayLangs"> {{l.text}}{{i < displayLangs.length-1?' / ':''}} </span></strong>
      </div>
      <div v-else style="margin-top: 0.5rem; text-align: center;" @click="editing=!editing">
        <div v-for="l, i in displayLangs">
          <h2><strong>{{l.text}}</strong></h2>
        </div>
        <div v-for="l, i in card.langs">
          <div><h6>{{l.comment}}</h6></div>
          <div v-for="e in l.examples">{{e}}</div>
          <hr v-if="i < displayLangs.length - 1">
        </div>
      </div>
      <!-- <div><strong>created: </strong>{{new Date(card.created).toLocaleDateString()}} {{new Date(card.created).toLocaleTimeString()}}</div>
           <div><strong>modified: </strong>{{new Date(card.modified).toLocaleDateString()}} {{new Date(card.modified).toLocaleTimeString()}}</div> -->
      <div v-if="editable && editing">
        <CardEditor :card="card" @saved="editing=false" @deleted="$emit('deleted')"></CardEditor>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import axios from 'axios'

import {Card} from "@/types";

import CardEditor from "@/components/CardEditor.vue"


@Component({
  components: {CardEditor},
})
export default class CardViewer extends Vue {
  
  @Prop()
  card!: Card;
  
  @Prop({default: true})
  editable!: boolean;
  
  @Prop({default: false})
  detailed!: boolean;
  
  @Prop({default: () => []})
  langs!: string[];
  
  get displayLangs(){
    return this.card.langs.filter(e => ~this.langs.indexOf(e.lang))
  }
  
  editing = false;
  
}
</script>

<style>
.cardlangtitle{
  padding: 0 1rem;
}

.card-viewer-title.editable{
  cursor: pointer;
}
</style>
