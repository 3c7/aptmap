<template>
    <div class="container">
        <h1>Map for {{actors[selectedActor].value}}</h1>
        <div id="actor-list">
            <span v-for="(actor, index) in actors" :key="index">
                <a :href="'#' + actor.value" v-on:click="selectActor(index)">{{actor.value}}</a> <br />
            </span> 
        </div>
        <div id="actor-map">
        </div>
    </div>    
</template>

<script lang="ts">
import datamap from 'datamaps';
import { Component, Prop, Vue } from 'vue-property-decorator';
import actors from '../utils/actors';


@Component
export default class ThreatActorMap extends Vue {
    private actors = actors.values;
    private selectedActor: number = 0;
    public mounted() {
        // Using datamaps this way crashed. Don't know why.
        const map = new datamap({
             element: document.getElementById('actor-map'),
             fills: {
                'defaultFill': '#ccc',
                'Threat Actor': '#c00',
             },
             data: {
                 [this.actors[this.selectedActor].meta.country || '']: {
                     fillKey: 'Threat Actor',
                 },
             },
        });
    }
    public selectActor(actorIndex: number) {
        this.selectedActor = actorIndex;
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#actor-map {
    width: 1200px;
    height: 650px;
}
#actor-list {
    text-align: left;
}
</style>