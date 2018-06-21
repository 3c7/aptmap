<template>
    <div class="container">
        <h1>{{message}}</h1>
        <div id="actor-list">
        </div>
        <div id="actor-map">
        </div>
    </div>    
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class ThreatActorMap extends Vue {
    @Prop() private message!: string;
    public mounted() {
        const datamap = require('datamaps');
        const map = datamap({
            element: document.getElementById('actor-map'),
        });
    }
}
</script>
<style scoped>
#actor-map {
    width: 1200px;
    height: 650px;
}
</style>