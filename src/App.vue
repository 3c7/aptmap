<template>
  <div id="app">
    <ThreatActorMap></ThreatActorMap>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ThreatActorMap from './components/ThreatActorMap.vue';

@Component({
  components: {
    ThreatActorMap,
  },
})
export default class App extends Vue {}
</script>

<style>
</style>
