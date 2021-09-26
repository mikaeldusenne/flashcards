import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import Toast from "vue-toastification";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import {
    BootstrapVue,
    BootstrapVueIcons,
    BIconHeart,
    BIconHeartFill,
    BIconGear,
    BIconGearFill,
    // BIconGem,
    // BIconGemFill,
    BIconJournal,
    BIconJournalText,
    BIconJournalMinus,
    BIconLightning,
    BIconLightningFill,
    BIconPatchCheck,
    BIconPatchCheckFill,
    BIconPen,
    BIconPenFill,
    BIconPencil,
    BIconPencilFill,
    BIconChat,
    BIconChatText,
    BIconChatTextFill,
    // BIconLightbulb,
} from 'bootstrap-vue'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faEdit } from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faMinusSquare } from "@fortawesome/free-solid-svg-icons";
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import "vue-toastification/dist/index.css";

Vue.use(Toast, {});
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons)

Vue.component("BIconHeart", BIconHeart)
Vue.component("BIconHeartFill", BIconHeartFill)
Vue.component("BIconGear", BIconGear)
Vue.component("BIconGearFill", BIconGearFill)
Vue.component("BIconJournal", BIconJournal)
Vue.component("BIconJournalMinus", BIconJournalMinus)
Vue.component("BIconJournalText", BIconJournalText)
Vue.component("BIconLightning", BIconLightning)
Vue.component("BIconLightningFill", BIconLightningFill)
Vue.component("BIconPatchCheck", BIconPatchCheck)
Vue.component("BIconPatchCheckFill", BIconPatchCheckFill)
Vue.component("BIconPen", BIconPen)
Vue.component("BIconPenFill", BIconPenFill)
Vue.component("BIconPencil", BIconPencil)
Vue.component("BIconPencilFill", BIconPencilFill)
Vue.component("BIconChat", BIconChat)
Vue.component("BIconChatTextFill", BIconChatTextFill)
Vue.component("BIconChatText", BIconChatText)



// Vue.use(IconsPlugin);

library.add(faEdit);
library.add(faUser);
library.add(faMinusSquare);
library.add(faPlusSquare);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.component("v-select", vSelect);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
