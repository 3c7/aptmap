<template>
    <div class="container" v-on:keydown="shortcut">
        <div class="row">
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a class="navbar-brand" href="#">Threat Actor Map</a>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item">
                            <a class="nav-link disabled" href="#">Disabled item as reminder</a>
                        </li>
                    </ul>
                    <button class="btn btn-danger" data-toggle="modal" data-target="#modal-sources">Sources</button>&nbsp;
                    <!-- Here goes the keyboard shortcuts modal -->
                    <button class="btn btn-warning" data-toggle="modal" data-target="#modal-help">?</button>
                </div>
            </nav>
        </div>
        <div class="row">
            <div id="actor-list" class="col-xl-3 scroll">
                <div class="list-group list-group-flush">
                    <input type="text" class="form-control" placeholder="🔍 Search Actor" v-model="searchActorName" v-on:keyup="filterActors">
                    <a class="list-group-item" v-bind:class="{active: index === selectedActor}" v-for="(actor, index) in filteredActors" :key="index" :href="'#' + actor.name" v-on:click="selectActor(index)">
                        {{actor.name}}
                    </a>
                </div>
            </div>
            <div class="col-xl-8">
                <div class="row">
                    <div class="actor-filter">
                        <span v-if="searchActorName !== ''" class="badge badge-danger">Name: {{searchActorName}} <span class="clickable" v-on:click="resetNameFilter()">&#215;</span></span>
                        <span v-if="searchActorCountry !== ''" class="badge badge-danger">Country: {{searchActorCountry}} <span class="clickable" v-on:click="resetCountryFilter()">&#215;</span></span>
                        <span v-if="searchActorCountry === '' && searchActorName === ''" class="badge badge-secondary">No filter</span>
                    </div>
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
                                    <a target="_blank" :href="ref">{{ref}}</a>
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

        <!-- Modals -->
        <div class="modal fade" id="modal-help" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Help</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <h5>Shortcuts</h5>
                    <dl>
                        <dt>
                            <span class="badge badge-secondary">j</span> or <span class="badge badge-secondary">&uarr;</span>
                        </dt>
                        <dd>
                            Move up
                        </dd>
                        <dt>
                            <span class="badge badge-secondary">k</span> or <span class="badge badge-secondary">&darr;</span>
                        </dt>
                        <dd>
                            Move down
                        </dd>
                    </dl>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="modal-sources" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalLabel">Sources</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>The data source for this map is the cluster 'Threat Actor' from the open source MISP Galaxy that can be found in the respective <a href="https://github.com/MISP/misp-galaxy/blob/master/clusters/threat-actor.json" target="_blank">Github</a> repository.<br />Thanks to </p>
                    <ul>
                        <li>Alexandre Dulaunoy</li>
                        <li>Florian Roth</li>
                        <li>Thomas Schreck</li>
                        <li>Timo Steffens</li>
                    </ul>
                    <p>and the other various contributors for sharing their knowledge and researches.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
        </div>
    </div>    
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Actor } from '../models/actor';
import actors from '../utils/actors';
import { constants } from 'http2';

@Component
export default class ThreatActorMap extends Vue {
    private actors: Actor[];
    private filteredActors: Actor[];
    private actor: Actor;
    private selectedActor: number = 0;
    private previousCountry!: string;
    private threatActorMap!: any;
    private searchActorName: string = '';
    private searchActorCountry: string = '';
    private DataMap: any;

    constructor() {
        super();
        this.actors = new Array();
        for (const actor of actors.values) {
            this.actors.push(new Actor(actor));
        }
        this.filteredActors = this.actors;
        this.actor = this.actors[0];
        this.DataMap = require('datamaps');
    }

    public mounted() {
        this.filterActors();
        this.threatActorMap = new this.DataMap({
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
             done: (datamap: any) => {
                datamap.svg.selectAll('.datamaps-subunit').on('click', (geography: any) => {
                    this.searchByCountry(geography.id);
                });
             },
        });
    }

    public selectActor(actorIndex: number) {
        if (this.actor.countryCode !== this.filteredActors[actorIndex].countryCode) {
            this.previousCountry = this.actor.countryCode;
        } else {
            this.previousCountry = '';
        }

        this.selectedActor = actorIndex;
        this.actor = this.filteredActors[actorIndex];
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

    public searchByName(name: string) {
        this.searchActorName = name;
        this.filterActors();
    }

    public searchByCountry(cc: string) {
        this.searchActorCountry = cc;
        this.filterActors();
    }

    public resetNameFilter() {
        this.searchByName('');
    }

    public resetCountryFilter() {
        this.searchByCountry('');
    }

    public filterActors() {
        const filteredActors = new Array<Actor>();
        if (this.searchActorName === '' && this.searchActorCountry === '') {
            this.filteredActors = this.actors;
        } else {
            for (const actor of this.actors) {
                if (actor.name.includes(this.searchActorName)
                && (this.searchActorCountry === '' || actor.countryCode === this.searchActorCountry)) {
                    filteredActors.push(actor);
                } else {
                    for (const synonym of actor.synonyms) {
                        if (synonym.includes(this.searchActorName)
                        && (this.searchActorCountry === '' || actor.countryCode === this.searchActorCountry)) {
                            filteredActors.push(actor);
                            break;
                        }
                    }
                }
            }
            this.filteredActors = filteredActors;
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
    overflow-y: auto;
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
.clickable {
    cursor: pointer;
}
.actor-filter {
    min-height: 30px;
    padding-top: 5px;
}
.actor-filter > .badge {
    margin-right: 5px;
}
</style>