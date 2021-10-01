<script>
    // imports
	import 'carbon-components-svelte/css/white.css';
	import { Button, Modal, TextInput, TextArea, ToastNotification } from 'carbon-components-svelte';
    import Add16 from "carbon-icons-svelte/lib/Add16";

    // variables
    let showModal = false;
    let newEntryData = {
        title: "",
        description: "",
        resolution: "",
        automation_link: ""
    };

    // error during POST request
    let errorSubmittingNewEntry = false;
    let errorMessage = "";

    // successful POST request
    let successfulSubmission = false;
    let successfulSubmissionMessage = "";

    // functions
    function launchModal() {
        showModal = true;
    }

    function closeModal() {
        newEntryData = {};
        showModal = false;
    }

    async function postNewEntry() {
        // title, description, and resolution can't be empty
        if (newEntryData.title == "" || newEntryData.description == "" || newEntryData.resolution == "") {
            errorSubmittingNewEntry = true;
            return errorMessage = "Title, description, and resolution fields cannot be empty";
        }

        // TODO Update this URL to be http://cphyprps01:9001/api/search when deployed
        const response = await fetch('http://localhost:9001/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newEntryData)
        });

        if (response.status == 201) {
            let json_response = await response.json()
            newEntryData = {};
            showModal = false;
            successfulSubmissionMessage = `Entry created: ${json_response.id}`;
            successfulSubmission = true;
        } else {
            errorMessage = response.statusText;
            errorSubmittingNewEntry = true;
        }
    }
</script>


<Button icon={Add16} on:click={launchModal}>New entry</Button>
{#if showModal}
    <Modal
        size="lg"
        open
        modalHeading="New Knowledge Entry"
        primaryButtonText="Submit"
        secondaryButtonText="Cancel"
        on:click:button--secondary={closeModal}
        on:open
        on:close={closeModal}
        on:submit={postNewEntry}
    >
        {#if errorSubmittingNewEntry}
        <p style="color: red; font-size: 20px">** {errorMessage}</p>
        {/if}

        <TextInput labelText="Title" placeholder="Entry title" bind:value="{newEntryData.title}" required=true />
        <TextArea labelText="Description" placeholder="Description of the error or issue and any error messages" bind:value="{newEntryData.description}" required=true />
        <TextArea labelText="Resolution" placeholder="Resolution for the error or issue" bind:value="{newEntryData.resolution}" required=true />
        <TextInput labelText="Automation Link [optional]" placeholder="Link to an automated resolution" bind:value="{newEntryData.automation_link}" />
    </Modal>
{/if}

{#if successfulSubmission}
	<ToastNotification
        kind="success"
        timeout=5000
		title="Entry created successfully!"
		subtitle={successfulSubmissionMessage}
		caption={new Date().toLocaleString()}
	/>
{/if}
