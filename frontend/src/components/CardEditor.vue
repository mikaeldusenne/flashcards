<template>
  <div class="container-fluid form" @keyup.enter="saveCard" v-on:submit.prevent>
    <div v-for="l in card.langs" :key="l.id">
      <div class="row mb-3">
        <label :for="'searchform-'+l.lang" style="" class="col-sm-4 col-xl-3 col-form-label">{{prettyLang(l.lang)}}</label>
        <div class="col-sm-8 col-xl-9">
          <input
            :id="'searchform-'+l.lang"
            type="text"
            maxlength="75"
            class="form-control"
            :placeholder="'translation in ' + prettyLang(l.lang)" 
            v-model="l.text"
          />
        </div>
      </div>
      <div class="row mb-3" v-show="showAdvanced">
        <label :for="'commentform-'+l.lang" style="" class="col-sm-4 col-xl-3 col-form-label">comment ({{prettyLang(l.lang)}})</label>
        <div class="col-sm-8 col-xl-9">
          <input
            :id="'commentform-'+l.lang"
            type="text"
            maxlength="75"
            class="form-control"
            :placeholder="'comment for ' + prettyLang(l.lang)" 
            v-model="l.comment"
          />
        </div>
      </div>
      <hr v-if="showAdvanced">
    </div>
    <div class="" style="display: flex; justify-content: center;">
      <div style="display: flex; justify-content: center; margin: 0 0.5rem;">
        <button
          @click="saveCard"
          class="btn btn-outline-secondary"
          type="button"
        >
          {{textButton}} Card
        </button>
      </div>
      <div style="display: flex; justify-content: center; margin: 0 0.5rem;" v-if="card.id">
        <button
          @click="deleteCard"
          class="btn btn-outline-danger"
          type="button"
        >
          Delete Card
        </button>
      </div>
    </div>
    <div style="display: flex; justify-content: end;"><em style="text-decoration: underline; cursor: pointer; color: #888;" @click="showAdvanced=!showAdvanced">show {{showAdvanced?'basic':'advanced'}} mode</em></div>
  </div>
</template>


<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import axios from 'axios'

import {Card} from "@/types";


@Component
export default class CardEditor extends Vue {
  @Prop({default: "Save"})
  textButton!: string;

  @Prop()
  card!: Card;
  
  showAdvanced = false;
  
  
  langs: any[] = [
    {id: "fr", title:"Français"},
    {id: "fa", title:"فارسی"},
  ];

  
  prettyLang(e){
    const pretty = this.langs.find(ee => ee.id==e)
    if(!pretty){
      console.log('pretty not found for:')
      console.log(e)
      console.log(this.langs)
    }
    return pretty ? pretty.title : e;
  }
  
  setupCard(){
    this.langs.forEach(lang => {
      if(this.card.langs.find(e => e.lang == lang.id) == undefined){
        this.card.langs.push({
          lang: lang.id, 
          text: "",
          comment: "",
          // examples: [],
        })
      }
    })
  }
  
  saveCard(){
    console.log("add card")
    axios.post("/api/add-card", this.card)
    .then(() => {
      this.$emit('saved')
    })
    .catch(console.log)
  }
  
  deleteCard(){
    console.log("delete card")
    axios.post("/api/delete-card", this.card)
    .then(() => {
      this.$emit('deleted')
    })
    .catch(console.log)
  }
  
  mounted(){    
    // axios.get('/api/langs')
    // .then(resp => {
    //   this.langs = resp.data;
    //   this.setupCard();
    // })
    // .catch(console.log)
  }
  
}
</script>

<style>
body{
  background: #f9f9f9;
}
.nav-tabs .nav-link.active{
  background: #f9f9f9;
}
.cardlangtitle{
  padding: 0 1rem;
}

</style>
