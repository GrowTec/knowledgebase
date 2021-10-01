<script context="module">
    export async function load(context) {
        let slug = context.page.params.slug;  // get the slug for this page

        return { props: {slug}}
    }
</script>
<script>
    // CSS imports
    import 'carbon-components-svelte/css/white.css';
    import { Grid, Row, Column, TextInput, TextArea, TextInputSkeleton, TextAreaSkeleton, Button } from 'carbon-components-svelte';
    import Home24 from "carbon-icons-svelte/lib/Home24";


    // variables
    export let slug;
    let dataPromise = getEntry();


    // functions
    function getEntry() {
        // TODO Update this URL to be http://cphyprps01:9001/api/search when deployed
        return fetch('http://localhost:9001/api/search/' + slug).then((response) => {
            console.log(response);
            return response.json();
        })
    };

    function updateKnowledgeEntry() {
        console.log("updating entry");
    }
</script>


<Grid>
    <Row>
        <Column sm={{ span: 2, offset: 1 }} style="text-align: center; margin-top: 2em; outline: 1px solid var(--cds-interactive-04); text-decoration: underline 2px">
            <h1>Knowledge Entry</h1>
        </Column>
        <Column>
            <Button icon={Home24} style="margin-top: 2em; font-size: 18px" href="/">Home</Button>
        </Column>
    </Row>
    <Row>
        <Column sm={{ span: 2, offset: 1 }} style="margin-top: 3em">
            {#await dataPromise}
            <TextInputSkeleton labelText="Title" />
            {:then data} 
            <TextInput labelText="Title" readonly="true" value={data.title} />
            {/await}
        </Column>
    </Row>
    <Row>
        <Column sm={{ span: 2, offset: 1 }} style="margin-top: 5em">
            {#await dataPromise}
            <TextAreaSkeleton labelText="Title" />
            {:then data} 
            <TextArea labelText="Description" readonly="true" value={data.description} />
            {/await}
        </Column>
    </Row>
    <Row>
        <Column sm={{ span: 2, offset: 1 }} style="margin-top: 4em">
            {#await dataPromise}
            <TextAreaSkeleton labelText="Title" />
            {:then data}
            <TextArea labelText="Resolution" readonly="true" value={data.resolution} />
            {/await}
        </Column>
    </Row>
    {#await dataPromise}
    <TextInputSkeleton labelText="Title" />
    <!-- Wait for the API call and then, if there's an automation_link key, show the text field -->
    {:then data}
        {#if data["automation_link"] != ""}
        <Row>
            <Column sm={{ span: 2, offset: 1 }} style="margin-top: 3em">
                <TextInput labelText="Automation Link" readonly="true" value={data.automation_link} />
            </Column>
        </Row>
        {/if}
    {/await}
</Grid>
