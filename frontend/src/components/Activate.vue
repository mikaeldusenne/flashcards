<template>
  <b-container>
    <b-row style="justify-content: center;">
      <b-col xs="12" md="10" lg="8" xl="6">
        <div class="alert alert-info" v-if="infomsg" v-html="infomsg" style="text-align: center;"></div>
      </b-col>
    </b-row>

  </b-container>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

import axios from "axios";
axios.defaults.baseURL = process.env.BASE_URL;

import { mapGetters } from "vuex";
@Component({
  components: {},
  computed: mapGetters(["getLoggedIn"])
})
export default class Activate extends Vue {
  infomsg = "";

  login() {
    this.infomsg = ""

    return axios
    .post("/api/user/activate/" + this.$route.params.activationLink)
    .then(resp => {
      this.infomsg="You successfully activated your account.<br>You will be redirected shortly...";
      // setTimeout(() => {
      //   this.$router.push('/');
      // }, 2500)
    })
    .catch(e => {
      this.$emit("err", e.response.data);
      this.infomsg = e.response.data;
    });
  }

  mounted(){
    console.log("-----------------------------------")
    console.log(this.$route)
    this.login()
  }
}
</script>

<style></style>
