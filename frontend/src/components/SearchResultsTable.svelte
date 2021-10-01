<script>
    // imports
    import 'carbon-components-svelte/css/white.css';
	import { DataTable, Link } from 'carbon-components-svelte';
    import Launch16 from "carbon-icons-svelte/lib/Launch16";

    // variables
    export let resultsList;
</script>

<DataTable
	headers={[
        { key: 'title', value: 'Title' },
		{ key: 'description', value: 'Description' },
		{ key: 'id', value: "Go to entry" }
	]}
	rows={resultsList}
>

	<span slot="cell" let:cell>
		{#if cell.key === 'id'}
			<Link icon={Launch16} href="/entry/{cell.value}" target="_blank">
				Open entry page
			</Link>
		{:else}
            {cell.value}
        {/if}
	</span>
</DataTable>
