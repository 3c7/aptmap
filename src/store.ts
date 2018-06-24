import Vue from 'vue';
import Vuex from 'vuex';
import { Actor } from './models/actor';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    actors: new Array(),
    currentSelectedActor: 0,
    filter: {
      actorName: null,
      actorCountry: null,

    },
  },
  mutations: {
    addActor(state, data) {
      state.actors.push(data.actor);
    },
    selectActor(state, actorNumber) {
      if (actorNumber <= state.actors.length) {
        state.currentSelectedActor = actorNumber;
      } else {
        state.currentSelectedActor = 0;
      }
    },
    resetFilter(state) {
      state.filter.actorName = null;
      state.filter.actorCountry = null;
    },
    setFilter(state, filter) {
      state.filter.actorName = filter.actorName;
      state.filter.actorCountry = filter.actorCountry;
    },
  },
  actions: {

  },
  getters: {
    getActors: (state) => {
      return state.actors;
    },
    getFilteredActors: (state) => {
      const filtered = new Array();

      for (const actor of state.actors) {
        // Filter here
      }

      return filtered;
    },
  },
});
