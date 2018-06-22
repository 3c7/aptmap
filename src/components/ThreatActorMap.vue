<template>
    <div class="container">
        <div class="row">
            <h1>Threat Actor Map (currently displaying: {{actors[selectedActor].value}})</h1>
        </div>
            <div class="row">
            <div id="actor-list" class="col-xl-3 scroll">
                <div class="list-group list-group-flush">
                    <a class="list-group-item" v-bind:class="{active: index === selectedActor}" v-for="(actor, index) in actors" :key="index" :href="'#' + actor.value" v-on:click="selectActor(index)">
                        {{actor.value}}
                    </a>
                </div>
            </div>
            <div class="col-xl-9">
                <div class="row">
                    <div id="actor-map">
                    </div>
                </div>
                <div class="row">
                    <dl>
                        <dt>Synonyms: </dt>
                        <dd></dd>
                    </dl>
                </div>
            </div>
        </div>
    </div>    
</template>

<script lang="ts">
import Datamap from 'datamaps';
import { Component, Prop, Vue } from 'vue-property-decorator';
import actors from '../utils/actors';


@Component
export default class ThreatActorMap extends Vue {
    private actors: any[] = actors.values;
    private selectedActor: number = 0;
    private actorName!: string;
    private actorSynonyms!: string;
    private actorDescription!: string;
    private actorRefs!: string[];

    public mounted() {
        // Using datamaps this way crashed. Don't know why.
        const map = new Datamap({
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
        this.actorName = this.actors[actorIndex].value;
        this.actorSynonyms = this.actors[actorIndex].meta.synonyms.join(', ') || '';
        this.actorDescription = this.actors[actorIndex].description || '';
        this.actorRefs = this.actors[actorIndex].meta.refs || [];
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#actor-map {
    width: 1200px;
    height: 400px;
}
#actor-list {
    text-align: left;
    max-height: calc(100vh - 200px);
}
.scroll {
    overflow-y: scroll;
}
</style>