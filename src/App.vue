<template>
  <div id="app">
    <img src="./assets/logo.png">
    <ThreatActorMap message="TLP:WHITE Threat Actor Map"></ThreatActorMap>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from './components/HelloWorld.vue';
import ThreatActorMap from './components/ThreatActorMap.vue';

@Component({
  components: {
    ThreatActorMap,
  },
})
export default class App extends Vue {}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
