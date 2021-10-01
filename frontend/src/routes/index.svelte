<script>
    // imports
	import 'carbon-components-svelte/css/white.css';
	import { Grid, Row, Column, Button, Search } from 'carbon-components-svelte';

    // custom components imports
    import SearchResultsTable from "../components/SearchResultsTable.svelte";
    import NewKnowledgeEntryModal from "../components/NewKnowledgeEntryModal.svelte";


    // variables
	let searchInput = "";
    let searchResults = [];

    // functions
    function search() {
        // TODO Update this URL to be http://cphyprps01:9001/api/search when deployed
        let url = new URL('http://localhost:9001/api/search');
        url.search = new URLSearchParams({
            query_string: searchInput
        })

        fetch(url)
            .then( response => response.json())
            .then((response) => {
                searchResults = response.results;
            });
    }

    function clear() {
        searchInput = "";
        searchResults = "";
    }

</script>

<style>
	@font-face {
        font-family: 'Press Start 2P';
        src: url('./PressStart2P-Regular.ttf') format('truetype');
    }

	h1 {
		font-family: 'Press Start 2P', cursive;
		text-decoration: underline 3px;
		margin-top: 1em;
	}
</style>


<Grid>
    <Row>
        <Column sm={{ span: 1, offset: 1}} style="outline: 1px solid var(--cds-interactive-04)">
            <h1>KnowledgeBase</h1>
        </Column>
    </Row>
    <Row>
        <Column sm={{ span: 2, offset: 1 }} style="margin-top: 3em">
            <Search light bind:value={searchInput} on:keyup={search} /> <!-- Search bar -->
        </Column>
        <Column>
            <Button kind="secondary" on:click={search} style="margin-top: 3em">Search</Button>  <!-- Search button -->
        </Column>
        <Column>
            <Button kind="danger" on:click={clear} style="margin-top: 3em; margin-left: -4em">Clear</Button>
        </Column>

    </Row>
    <Row>
        <Column sm={{ span: 1, offset: 3 }} style="margin-top: 3em">
            <NewKnowledgeEntryModal />
        </Column>
    </Row>
    <Row style="margin-top: 8em">
        {#if searchResults.length != 0}
        <Column sm={{ span: 4 }}>
            <SearchResultsTable resultsList={searchResults} />
        </Column>
        {/if}
        
    </Row>
</Grid>