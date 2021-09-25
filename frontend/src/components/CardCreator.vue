<template>
  <div class="container-fluid">
    <div class="row card border-dark" style="margin-bottom: 1rem">
      <div class="card-header">
        <strong>Create a new card:</strong>
      </div>
      <div class="card-body">
        <CardEditor
          :isNew="true"
          :showAdvancedDefault="true"
          :card="newCard"
          textButton="Create"
          @saved="resetCard"
        />
      </div>
    </div>
    <div class="row card border-dark" style="margin-bottom: 1rem">
      <div class="card-header">
        <strong>Create a new deck:</strong>
      </div>
      <div class="card-body">
        <div class="row mb-3">
          <label class="col-sm-4 col-xl-3 col-form-label">New Deck:</label>
          <div class="input-group col-sm-8 col-xl-9">
            <input
              type="text"
              maxlength="75"
              class="form-control"
              placeholder="deck title"
              v-model="newDeck.title"
            />
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="addNewDeck"
            >
              Add
            </button>
          </div>
        </div>
      </div>

      <b-row style="margin: 1rem 0;">
        
        <div class="col-12" v-for="(e, i) in decks" :key="i">
            <div class="input-group">
              <input
                type="text"
                maxlength="75"
                class="form-control"
                v-model="e.title"
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="addDeck(e)"
              >
                Save
              </button>
              <button
                class="btn btn-outline-danger"
                type="button"
                @click="deleteDeck(e)"
              >
                Delete
              </button>
            </div>
        </div>
      </b-row>
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
  newCard: Card = { id: "", langs: [], decks: [] };

  decks: any[] = [];
  newDeck: any = { title: "" };

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

  resetCard() {
    this.$toast.success(
      `card ${this.newCard.langs.map((e) => e.text).join(" / ")} created!`
    );
    this.newCard.langs = this.newCard.langs.map((e) => {
      e.text = "";
      e.comment = "";
      return e;
    });
  }

  @Watch("getLangs")
  lgschgd() {
    this.setupNewCard();
  }

  fetchDecks() {
    axios
      .get("/api/decks")
      .then((resp) => {
        this.decks = resp.data;
      })
      .catch(console.log);
  }

  addDeck(e) {
    return axios
    .post("/api/decks", e)
    .then((resp) => {
      console.log(resp);
      this.fetchDecks();
      
      axios
      .get("/api/decks")
      .then((respp) => {
        this.$store
        .dispatch("setDecks", respp.data)
        .then(console.log)
        .catch(console.error);
      })
      .catch(console.log);

    })
    .catch(console.log);
  }

  addNewDeck() {
    this.addDeck(this.newDeck).then(() => {
      this.newDeck.title = "";
    });
  }

  deleteDeck(e) {
    axios
      .delete("/api/decks", { data: { id: e._id } })
      .then((resp) => {
        console.log(resp);
        this.fetchDecks();
      })
      .catch(console.log);
  }

  mounted() {
    this.setupNewCard();
    this.fetchDecks();
  }
}
</script>

<style></style>
