<template>
    <div class="container">
        <div class="row" @keydown="shortcut">
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a class="navbar-brand" href="#">Threat Actor Map</a>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item">
                            <a class="nav-link disabled" href="#">Disabled item as reminder</a>
                        </li>
                    </ul>
                    <a class="btn btn-danger" href="#">Sources</a>&nbsp;
                    <!-- Here goes the keyboard shortcuts modal -->
                    <a class="btn btn-warning" href="#">?</a>
                </div>
            </nav>
        </div>
        <div class="row" @keydown="shortcut">
            <div id="actor-list" class="col-xl-3 scroll">
                <div class="list-group list-group-flush">
                    <a class="list-group-item" v-bind:class="{active: index === selectedActor}" v-for="(actor, index) in actors" :key="index" :href="'#' + actor.name" v-on:click="selectActor(index)">
                        {{actor.name}}
                    </a>
                </div>
            </div>
            <div class="col-xl-8" @keydown="shortcut">
                <div class="row">
                    <div id="actor-map">
                    </div>
                </div>
                <div class="row">
                    <dl class="dl-horizontal left">
                        <dt>Name:</dt>
                        <dd>{{actor.name}}</dd>
                        <dt>Synonyms: </dt>
                        <dd>{{actor.synonymsString() || 'None'}}</dd>
                        <dt>Operating from: </dt>
                        <dd>{{actor.countryCode || 'Unknown'}}</dd>
                        <dt>Description: </dt>
                        <dd>{{actor.description || 'None'}}</dd>
                        <dt>References: </dt>
                        <dd>
                            <ul>
                                <li v-for="(ref, index) in actor.references" :key="index">
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
import { Actor } from '../models/actor';
import actors from '../utils/actors';

@Component
export default class ThreatActorMap extends Vue {
    private actors: Actor[];
    private actor: Actor;
    private selectedActor: number = 0;
    private previousCountry!: string;
    private threatActorMap!: any;

    constructor() {
        super();
        this.actors = new Array();
        for (const actor of actors.values) {
            this.actors.push(new Actor(actor));
        }
        this.actor = this.actors[0];
    }

    public mounted() {
        this.threatActorMap = new Datamap({
             element: document.getElementById('actor-map'),
             fills: {
                'defaultFill': '#ccc',
                'Threat Actor': '#c00',
                'Clean': '#ccc',
             },
             data: {
                 [this.actors[this.selectedActor].countryCode || '']: {
                     fillKey: 'Threat Actor',
                 },
             },
        });
    }

    public selectActor(actorIndex: number) {
        if (this.actor.countryCode !== this.actors[actorIndex].countryCode) {
            this.previousCountry = this.actor.countryCode;
        } else {
            this.previousCountry = '';
        }

        this.selectedActor = actorIndex;
        this.actor = this.actors[actorIndex];
        this.threatActorMap.updateChoropleth({
            [this.actor.countryCode]: {
                fillKey: 'Threat Actor',
            },
            [this.previousCountry]: {
                fillKey: 'Clean',
            },
        });
    }

    public shortcut(event: KeyboardEvent) {
        switch (event.key) {
            case 'j':
            case 'ArrowUp':
                if (this.selectedActor === 0) {
                    this.selectActor(this.actors.length - 1);
                } else {
                    this.selectActor((this.selectedActor - 1) % this.actors.length);
                }
                break;
            case 'k':
            case 'ArrowDown':
                this.selectActor((this.selectedActor + 1) % this.actors.length);
        }
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
    max-height: calc(100vh - 150px);
    margin-right: 15px;
    padding: 0;
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
    margin: 0;
}
footer {
    padding-top: 1.9rem;
    padding-bottom: 0.8rem;
}
.navbar {
    width: 100%;
}
.list-group-item.active {
    background-color: #dc3545;
    border-color: #dc3545;
}
a.list-group-item {
    color: #dc3545;
}
a.list-group-item.active {
    color: #fff;
}

</style>