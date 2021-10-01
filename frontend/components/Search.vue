<template>
  <div id="searchbox">
    <div class="row mt-5" id="searchbox">
      <div class="col-2"></div>
      <div class="col-8">
        <input
          v-model="search_query"
          @keyup.enter="search()"
          @keyup="search()"
          class="form-control form-control-lg"
          id="searchbox-input"
          placeholder="What are you looking for?"
        >
      </div>
      <div class="col-2">
        <button type="button" class="btn btn-primary btn-lg" @click="search()">
          <b-icon icon="search" aria-hidden="true" class="pr-1 mr-1"></b-icon>
          Search
        </button>
      </div>
    </div>

    <div class="row" id="search-results" v-if="show_results">
      <b-col offset-md="2" class="col-auto mt-5">
        <b-list-group v-for="(result, i) in search_results" :key="i">
          <b-list-group-item class="px-4 mb-1" :href="'/entry/' + result.id" target="_blank">{{ result.title }}</b-list-group-item>
        </b-list-group>
      </b-col>
    </div>

  </div>
</template>


<script>
export default {
  data() {
    return {
      search_query: '',
      search_results: [],
      show_results: false,
    }
  },
  methods: {
    search() {
      const options = {
        method: 'GET',
        url: 'http://localhost:9001/api/search',
        params: {query_string: this.search_query}
      }
      // TODO update this hostname in production
      this.$axios.request(options).then(
        response => {
          this.search_results = response.data.results
        }
      )
      this.show_results = true;  // make the results component visible
    },
  },
  mounted() {
    const searchbox = document.getElementById('searchbox-input');
    searchbox.focus();
  }
}
</script>

<style scoped>
a.list-group-item:hover {
  background: #007bff;
  color: white;
  cursor: pointer;
}


</style>