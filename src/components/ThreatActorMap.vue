<template>
    <div class="container">
        <div class="row">
            <div class="jumbotron">
                <h1 class="display-4">Threat Actor Map</h1>
                <p class="lead">This map aims to give an overview about threat actors. Information used is the MISP Threat Actor Galaxy.</p>
            </div>
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
                    <dl class="dl-horizontal left">
                        <dt>Name:</dt>
                        <dd>{{actorName}}</dd>
                        <dt>Synonyms: </dt>
                        <dd>{{actorSynonyms || 'None'}}</dd>
                        <dt>Description: </dt>
                        <dd>{{actorDescription || 'None'}}</dd>
                        <dt>References: </dt>
                        <dd>
                            <ul>
                                <li v-for="(ref, index) in actorRefs" :key="index">
                                    <a :href="ref">{{ref}}</a>
                                </li>
                            </ul>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <footer class="text-muted">
            <div class="container">
                <p class="float-right">&copy; Nils Kuhnert, 2018</p>
                <p>Thanks to everyone that shares infosec related threat information | Information based on <a href="https://github.com/MISP/misp-galaxy/blob/master/clusters/threat-actor.json">MISP-Galaxy</a></p>
            </div>
        </footer>
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
    private actorName: string = this.actors[this.selectedActor].value;
    private actorSynonyms: string = this.actors[this.selectedActor].meta.synonyms.join(', ');
    private actorDescription: string = this.actors[this.selectedActor].description;
    private actorRefs: string[] = this.actors[this.selectedActor].meta.refs;
    private actorCountry: string = this.actors[this.selectedActor].meta.country;
    private previousCountry!: string;
    private threatActorMap!: any;

    public mounted() {
        this.threatActorMap = new Datamap({
             element: document.getElementById('actor-map'),
             fills: {
                'defaultFill': '#ccc',
                'Threat Actor': '#c00',
                'Clean': '#ccc',
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
        this.actorName = this.actors[this.selectedActor].value;
        this.actorSynonyms = (this.actors[this.selectedActor].meta.synonyms || []).join(', ') || '';
        this.actorDescription = this.actors[this.selectedActor].description || '';
        this.actorRefs = this.actors[this.selectedActor].meta.refs || [];

        if (this.actorCountry !== this.actors[actorIndex].meta.country) {
            this.previousCountry = this.actorCountry;
        } else {
            this.previousCountry = '';
        }

        this.actorCountry = this.actors[actorIndex].meta.country;

        this.threatActorMap.updateChoropleth({
            [this.actorCountry]: {
                fillKey: 'Threat Actor',
            },
            [this.previousCountry]: {
                fillKey: 'Clean',
            },
        });
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#actor-map {
    height: 400px;
}
#actor-list {
    text-align: left;
    max-height: calc(100vh - 300px);
    padding: 0px;
}
.scroll {
    overflow-y: scroll;
}
.left {
    text-align: left;
}
.jumbotron {
    width: 100%;
    padding: 2em 2em;
}
footer {
    padding-top: 1.9rem;
    padding-bottom: 0.8rem;
}
</style>