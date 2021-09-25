import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../components/Login.vue";
import Activate from "../components/Activate.vue";
import ResetPassword from "../components/ResetPassword.vue";
import Train from "../views/Train.vue";
import Explore from "../views/Explore.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/train",
    name: "Train",
    component: Train,
  },
  {
    path: "/explore",
    name: "Explore",
    component: Explore,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/user/activate/:activationLink",
    name: "Activate",
    component: Activate,
  },
  {
    path: "/user/reset-password/:activationLink",
    name: "ResetPassword",
    component: ResetPassword,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
