<template>
  <b-container>
    <div v-if="!showReset">
      <b-row style="margin-bottom: 1rem;">
        <div class="alert alert-info" v-if="infomsg" style="max-height: 5rem; overflow: auto;">{{ infomsg }}</div>
      </b-row>
      <form class="row g-3" v-on:submit.prevent>
        <div class="col-12" @keyup.enter="loginOrRegister">
          <label for="inputEmail">Email</label>
          <input
            type="email"
            class="form-control"
            id="inputEmail"
            v-model="loginForm.email"
            placeholder="email"
          />
        </div>
        <div class="col-12" @keyup.enter="loginOrRegister">
          <label for="inputPassword">Password</label>
          <input
            type="password"
            class="form-control"
            id="inputPassword"
            v-model="loginForm.password"
            placeholder=""
          />
        </div>
        <div class="col-12" v-if="showRegister" @keyup.enter="loginOrRegister">
          <label for="inputPassword2">Confirm Password</label>
          <input
            type="password"
            class="form-control"
            id="inputPassword2"
            v-model="password2"
            placeholder=""
          />
        </div>
        <div class="col-xs-12" :class="{'col-xl-6': !showRegister}">
          <button
            type="button"
            @click="loginOrRegister"
            class="btn btn-primary"
            style="width: 100%"
            :disabled="!loginForm.email || !loginForm.password || (showRegister && !registerIsValid)"
          >
            {{showRegister?'Register':'Login'}}
          </button>
        </div>
        <div class="col-xl-6 col-xs-12" v-if="!showRegister">
          <button
            type="button"
            @click="setShowReset(true)"
            class="btn btn-outline-secondary"
            style="width: 100%"
          >
            Forgot your password?
          </button>
        </div>
        <!-- <hr style="margin-top: 2rem; margin-bottom: 0;" /> -->
        
        <div v-if="!showRegister" class="col-12" style="justify-content: center; text-align: center; margin: 1rem 0 0rem 0;">
          or
        </div>
        <!-- <div class="col-xl-12 col-xs-12">
             <em></em>
             </div> -->
        <div class="col-xl-12 col-xs-12" v-if="!showRegister">
          <button
            type="button"
            @click="showRegister = !showRegister"
            class="btn btn-success"
            style="width: 100%"
            id="1"
          >
            Register
          </button>
        </div>
        <div class="col-xl-12 col-xs-12" v-else>
          <button
            type="button"
            @click="showRegister = !showRegister"
            class="btn btn-outline-secondary"
            style="width: 100%"
            id="2"
          >
            Back to login
          </button>
        </div>
      </form>
    </div>
    <div v-else>
      <b-row>
        <p>
          Enter your email in the field below. If an account exists with this email, you will receive an email allowing you to restore your password.
        </p>
        <div class="alert alert-info" v-if="infomsg">{{ infomsg }}</div>
      </b-row>
      <form class="row g-3" v-on:submit.prevent>
        <div class="col-12">
          <div class="form-group">
            <label for="inputResetEmail">Email</label>
            <input
              type="email"
              class="form-control"
              id="inputResetEmail"
              v-model="emailReset"
              placeholder="email"
            />
          </div>
        </div>
        <div class="col-xl-6 col-xs-12">
          <button
            @click="resetPassword"
            :disabled="!emailReset"
            class="btn btn-primary"
            style="width: 100%"
          >
            Reset password
          </button>
        </div>
        <div class="col-xl-6 col-xs-12">
          <button
            @click="setShowReset(false)"
            class="btn btn-outline-secondary"
            style="margin-left: 0.5rem; width: 100%"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </b-container>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { mapGetters } from "vuex";

import axios from "axios";
axios.defaults.baseURL = process.env.BASE_URL;

@Component({
  components: {},
  computed: mapGetters(["getId"])
})
export default class Login extends Vue {
  loggedin: boolean | null = null;
  showReset = false;
  showRegister = false;
  
  emailReset = "";
  infomsg = "";
  loginForm = {
    id: "",
    password: ""
  };

  get registerIsValid(){
    return this.password2 && (this.password2 == this.loginForm.password)
  }

  password2 = "";
  
  setShowReset(b){
    this.infomsg = "";
    this.showReset = b;
  }
  
  resetPassword() {
    if (this.emailReset.length) {
      axios
      .get("/api/reset-password-send-link", { params: { email: this.emailReset } })
      .then(ans => {
        console.log(ans);
        this.infomsg =
          "Please check your emails to reset your account password.";
      })
      .catch(console.log);
    }
  }

  tryLogin() {
    this.infomsg = ""

    return axios
    .post("/login", this.loginForm)
    .then(resp => {
      this.loggedin = true;
      console.log((resp as any).id);
      const u = resp.data;
    })
    .catch(e => {
      this.$emit("err", e.response.data);
      this.loggedin = false;
      this.infomsg = e.response.data;
    });
  }
  
  loginOrRegister(){
    if(this.showRegister){this.register()}else{this.login()}
  }
  
  login() {
    this.tryLogin()
    .then(() => {
      this.$router.go(0)
    })
    .catch(console.log);
  }
  
  register() {
    this.infomsg = ""
    
    return axios
    .post("/register", this.loginForm)
    .then(resp => {
      this.loggedin = true;
      console.log((resp as any).id);
      this.infomsg = "Congratulations, You are registered! Please confirm your email by clicking on the link that was sent to you."
      this.showRegister = false;
      const u = resp.data;
    })
    .catch(e => {
      this.$emit("err", e.response.data);
      this.loggedin = false;
      this.infomsg = e.response.data;
    });
  }

  @Watch("loginForm.id")
  @Watch("loginForm.password")
  changed() {
    this.$emit("err", "");
  }
}
</script>

<style></style>
