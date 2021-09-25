<template>
  <b-container>
    <b-row v-if="errormsg">
      <div class="alert alert-danger" style="text-align: center; width: 100%;" v-html="errormsg"></div>
    </b-row>
    <b-row style="justify-content: center;" v-else>
      <b-col xs="12" md="10" lg="8" xl="6">
        <strong>Reset password for user <{{email}}></strong>
        <div>
          <b-row style="margin-bottom: 1rem;">
            <div class="alert alert-info" v-if="infomsg" style="text-align: center; width: 100%; max-height: 8rem; overflow: auto;margin: 1rem;">
              <div>{{ infomsg }}</div>
              <div><router-link style="text-decoration: underline;" to="/login">Login</router-link></div>
            </div>
          </b-row>
          <form class="row g-3" v-on:submit.prevent autocomplete="off">
            <div class="col-12" @keyup.enter="resetPassword">
              <label for="inputPassword">Password</label>
              <input
                type="password"
                class="form-control"
                id="inputPassword"
                v-model="password"
                placeholder=""
                required
              />
            </div>
            <div class="col-12" @keyup.enter="resetPassword">
              <label for="inputPassword2">Confirm Password</label>
              <input
                required
                type="password"
                class="form-control"
                id="inputPassword2"
                v-model="password2"
                placeholder=""
              />
            </div>
            <div class="col-12">
              <button
                type="button"
                @click="resetPassword"
                class="btn btn-outline-primary"
                style="width: 100%; margin-top: 1rem;"
                :disabled="!registerIsValid"
              >
                Reset Password
              </button>
            </div>
          </form>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

import axios from "axios";
axios.defaults.baseURL = process.env.BASE_URL;

import { mapGetters } from "vuex";
@Component({
  components: {},
  computed: mapGetters(["getLoggedIn"])
})
export default class ResetPassword extends Vue {
  email: string | null = null;
  password = "";
  password2 = "";
  errormsg = "";
  infomsg = "";
  
  get registerIsValid(){
    return this.password2 && (this.password2 == this.password)
  }
  
  resetPassword() {
    if (this.registerIsValid) {
      axios
      .post("/api/user/reset-password/" + this.$route.params.activationLink, {password: this.password})
      .then(ans => {
        console.log(ans);
        this.infomsg =
          "Password successfuly restored.";
      })
      .catch(console.log);
    }
  }

  mounted(){
    console.log('RESET PASSWORD')
    axios.get('/api/mail-from-activation-link', {params: {link: this.$route.params.activationLink}})
    .then(resp => {
      this.email = resp.data;
    })
    .catch(err => {
      this.errormsg = err.response.data;
    })
  }
}
</script>

<style>
form > div{
  margin-bottom: 0.75rem;
}
</style>
