import { Component, Vue } from "vue-property-decorator";
import { mapGetters } from "vuex";

@Component({
  computed: mapGetters(["getLangs", "getDecks"]),
})
export default class MathMixin extends Vue {
  getLangs!: any[];
  getDecks!: any[];


    flatten(l){
        return (!l || l.length == 0) ? [] : l.length == 1 ? l[0] : l.reduce((acc, e) => acc.concat(e))
    }
    
  prettyN(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  sum(l) {
    return !l || !l.length ? 0 : l.reduce((a, b) => a + b);
  }

  mean(l) {
    if (!l || l.length == 0) {
      return NaN;
    } else {
      return this.sum(l) / l.length;
    }
  }

  variance(l) {
    if (!l || l.length == 0) {
      return NaN;
    } else {
      return this.mean(l.map((e) => e * e)) - this.mean(l) ** 2;
    }
  }

  sd(l) {
    return Math.sqrt(this.variance(l));
  }

  decimalPrecision(k, n) {
    return k == 0
      ? k
      : k.toFixed(Math.max(0, -Math.floor(Math.log10(k)) + (n - 1)));
  }

  prettyLang(e) {
    const pretty = this.getLangs.find((ee) => ee.id == e);
    if (!pretty) {
      console.log("pretty not found for:");
      console.log(e);
      console.log(this.getLangs);
    }
    return pretty ? pretty.title : e;
  }

    get deckOpts() {
        const firstopt: any = { text: "Select a deck...", value: null};
      return [firstopt].concat(
      this.getDecks.map((e) => {
        return {
          text: `${e.title} (${e.n_cards} card${e.n_cards>1?'s':''})`,
          value: e._id,
        };
      })
    );
  }

    prettyCardTitle(c){
        return c.langs.map(e => e.text).join(' / ')
    }
}
