<template>
  <div class="card card-viewer">
    <div class="card-body" style="text-align: center; padding: 0.5rem">
      <div
        class="card-viewer-title"
        style="margin: 0.5rem"
        :class="{ editable: editable }"
        @click="toggleEditing"
        v-if="!detailed"
      >
        <strong>
          {{ displayLangs.map((e) => e.text).join(" / ") }}
        </strong>
      </div>
      <div
        v-else
        style="margin-top: 0.5rem; text-align: center"
        @click="toggleEditing"
      >
        <div v-for="(l, i) in displayLangs" :key="i">
          <h2>
            <strong>{{ l.text }}</strong>
          </h2>
        </div>
        <hr v-if="allComments.length > 0" />
        <div v-for="(comment, i) in allComments" :key="`comments${i}`">
          <div>
            <h6><pre>{{ comment }}</pre></h6>
          </div>
          <!-- <div v-for="e in l.examples" :key="`${e}`">{{ e }}</div> -->
        </div>
      </div>
      <!-- <div><strong>created: </strong>{{new Date(card.created).toLocaleDateString()}} {{new Date(card.created).toLocaleTimeString()}}</div>
           <div><strong>modified: </strong>{{new Date(card.modified).toLocaleDateString()}} {{new Date(card.modified).toLocaleTimeString()}}</div> -->
      <div v-if="editable && editing">
        <CardEditor
          :card="card"
          @saved="toggleEditing(false)"
          @deleted="$emit('deleted')"
        ></CardEditor>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from "vue-property-decorator";
import MathMixin from "@/MathMixin";

import { Card } from "@/types";

import CardEditor from "@/components/CardEditor.vue";

@Component({
  components: { CardEditor },
  mixins: [MathMixin],
})
export default class CardViewer extends Mixins(MathMixin) {
  editing = false;
  
  @Prop()
  card!: Card;

  @Prop({ default: true })
  editable!: boolean;

  @Prop({ default: false })
  detailed!: boolean;

  @Prop({ default: () => [] })
  langs!: string[];

  get displayLangs() {
    return this.card.langs.filter(
      (e) => !this.langs.length || ~this.langs.indexOf(e.lang)
    );
  }

  get allComments(){
    return this.card.langs.map(e => e.comment).filter(e => e)
  }

  toggleEditing(v){
    
    this.editing = v==undefined ? !this.editing : v
    console.log("CARDVIEWER EDITING IS NOW:")
    console.log(this.editing)
    this.$emit('editing', this.card.id, this.editing)
  }
  
}
</script>

<style>
.cardlangtitle {
  padding: 0 1rem;
}

.card-viewer-title.editable {
  cursor: pointer;
}
pre{
  font-family: Avenir, Helvetica, Arial, sans-serif !important;
}
</style>
