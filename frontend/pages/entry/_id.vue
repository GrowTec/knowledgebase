<template>
    <div id="knowledgeEntryPage" class="container mt-5">
        <b-alert :show="alertStatus" variant="warning">You are editing this entry</b-alert>
        <div class="row">
            <b-col>
                <div class="row">
                    <b-col class="col-auto" offset-md="2">
                        <h3>Title:</h3>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-8 mb-5" offset-md="2">
                        <b-form-input id="issue-title" :readonly="!editable" v-model="title"></b-form-input>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-auto" offset-md="2">
                        <h3>Description:</h3>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-8 mb-5" offset-md="2">
                        <b-form-textarea id="issue-description" :readonly="!editable" v-model="description"></b-form-textarea>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-auto" offset-md="2">
                        <h3>Resolution:</h3>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-8 mb-5" offset-md="2">
                        <b-form-textarea id="issue-resolution" :readonly="!editable" v-model="resolution"></b-form-textarea>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-auto" offset-md="2">
                        <h4>Automation to resolve this issue:</h4>
                    </b-col>
                </div>
                <div class="row">
                    <b-col class="col-8 mb-5" offset-md="2">
                        <b-form-input id="issue-automation" :readonly="!editable" v-model="automation_link"></b-form-input>
                    </b-col>
                </div>
            </b-col>
        </div>
        <div class="row">
            <b-col offset-md="2">
                <b-button-group>
                    <b-button variant="primary" size="lg" :disabled="editable" @click="editEntry()" v-if="this.editable == false">
                        <b-icon icon="pencil-square" aria-hidden="true" class="pr-1"></b-icon>
                        Edit
                    </b-button>
                    <b-button variant="danger" size="lg" @click="stopEditing()" v-if="this.editable == true">
                        <b-icon icon="pencil-square" aria-hidden="true" class="pr-1"></b-icon>
                        Stop Editing
                    </b-button>
                    <b-button variant="success" size="lg" class="ml-1" :disabled="!editable" @click="updateDocumentPatch()">
                        <b-icon icon="check-square" aria-hidden="true" class="pr-1" ></b-icon>
                        Save
                    </b-button>
                </b-button-group>
            </b-col>
        </div>
        <div class="row mt-5">
            <b-col offset-md="2">
                <h5><b-icon icon="person" aria-hidden="true" class="mr-1"></b-icon> Created by: {{ this.created_by }}</h5>
                <h5><b-icon icon="clock" aria-hidden="true" class="mr-1"></b-icon> Last updated by: {{ this.last_updated_by }} </h5>
            </b-col>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            editable: false,  // is the page currently being edited
            alertStatus: false,  // should the 'editing' alert be shown
            title: '',
            description: '',
            resolution: '',
            automation_link: '',
            created_by: '',
            last_updated_by: '',
        }
    },
    methods: {
        editEntry() {
            // make the input forms editable and show the alert, at the top of the page, to remind the person that they're editing the page
            this.editable = true;
            this.alertStatus = true;
        },
        stopEditing() {
            // Cancel editing the page. Make the input forms readonly and dismiss the alert at the top of the page.
            this.editable = false;
            this.alertStatus = false;
        },
        updateDocumentPatch() {
            // send the PATCH API call to update the document with the new values
            const options = {
                method: 'PATCH',
                url: 'http://localhost:9001/api/search/' + this.$route.params.id,  // TODO update this hostname in production
                data: {
                    id: this.$route.params.id,
                    title: this.title,
                    description: this.description,
                    resolution: this.resolution,
                    automation_link: this.automation_link,
                    created_by: this.created_by,
                    last_updated_by: 'Andrew Guest (ag043542)'  // TODO replace this with the current user or remove this functionality entirely
                }
            }
            this.$axios.request(options).then(
                response => {
                    console.log(response);
                    if (response.data.result == 'updated' || response.status == 200) {
                        this.$bvToast.toast("Document updated successfully", {
                            title: "Document updated",
                            toaster: "b-toaster-top-right",
                            variant: "success",
                            solid: true,
                            appendToast: true,
                            "auto-hide-delay": 5000
                        })
                        return this.editable = false;
                    } else {
                        this.$bvToast.toast("Error updating document", {
                            title: "Error updating document",
                            toaster: "b-toaster-top-right",
                            variant: "danger",
                            solid: true,
                            appendToast: true,
                            "auto-hide-delay": 5000
                        })
                    }
                    
                }
            )
        }
    },
    beforeCreate() {
        const options = {
        method: 'GET',
        url: 'http://localhost:9001/api/search/' + this.$route.params.id,  // TODO update this hostname in production
      }
      this.$axios.request(options).then(
        response => {
            this.title = response.data.title,
            this.description = response.data.description,
            this.resolution = response.data.resolution,
            this.automation_link = response.data.automation_link,
            this.created_by = response.data.created_by,
            this.last_updated_by = response.data.last_updated_by
        }
      )
    }
}
</script>
