<template>
  <div v-if="!getLoggedIn">
    <div style="text-align: center">
      <p>
        In order to access all features, please <router-link to="/login">login</router-link>.
      </p>
    </div>
  </div>
  <div v-else>
    <slot/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { mapGetters } from "vuex";

@Component({
  components: {},
  computed: mapGetters(["getLoggedIn"]),
})
export default class Train extends Vue {
  getLoggedIn!: boolean;
}
</script>

<style scoped></style>
