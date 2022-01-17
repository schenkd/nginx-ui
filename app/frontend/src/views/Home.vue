<template>
  <div style="margin-top:32px;">
    <v-container>
      <v-card
          elevation="2"
          outlined
      >
        <v-card-title>
          Service
          <v-spacer></v-spacer>
          <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table
            hide-default-footer
            :headers="headers"
            :items="items"
            :search="search"
            :items-per-page=-1
        >
          <template v-slot:item.instance_id="{item}">
            <label>{{ item.instance_id }}
            </label>
            <v-chip class="ma-2" v-for="val in item.tags" :key="val" v-show="item.tags.length !== 0">{{ val }}</v-chip>
          </template>
          <template v-slot:item.action="{item}">
            <v-btn
                @click="edit(item)"
                icon
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>

      <v-dialog
          v-model="edit_service_switch"
          max-width="440"
      >
        <v-card>
          <v-card-title>
            <span class="headline">{{ edit_info.service_name }}</span>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <v-autocomplete
                    v-model="edit_info.endpoint"
                    :items="edit_info.all_endpoints"
                    key="endpoint"
                    item-text="endpoint"
                    return-object
                    label="Please choose enpoint"
                    outlined
                    dense
                >
                  <template v-slot:item="{item}">
                    <label>{{ item.instance_id + "(" + item.endpoint + ")" }} </label>
                    <v-chip class="ma-2" v-for="val in item.tags" :key="val" v-show="item.tags.length !== 0">{{ val }}
                    </v-chip>
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  class="ma-1"
                  color="grey"
                  plain
                  @click="cancelEdit"
              >Cancel
              </v-btn>
              <v-btn
                  class="ma-1"
                  color="primary"
                  plain
                  @click="saveEdit"
              >Save
              </v-btn>

            </v-card-actions>

          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>
<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

import axios from 'axios'

export default {
  name: 'Home',
  components: {},
  // HelloWorld
  data: () => ({
    drawer: true,
    group: null,
    headers: [
      {text: "ServiceName", value: "service_name", sortable: false},
      {text: "Endpoint", value: "instance_id", sortable: false},
      {text: "Action", value: "action", sortable: false},
    ],

    search: '',
    items: [],

    edit_service_switch: false,
    edit_info: {
      service_name: '',
      endpoint: '',
      all_endpoints: [],
    }

  }),

  mounted() {
    this.getService()
  },


  methods: {

    getService() {
      const path = `http://wish-nginx-ui.com/api/services`;
      axios.get(path).then(response => {
        this.items = response.data.data;
      }).catch(error => {
        console.log(error);
      })
    },

    /******************************************************/
    // ALL API
    getAllEndpoints(service_name) {
      const path = `http://wish-nginx-ui.com/api/services/` + service_name;
      axios.get(path).then(response => {
        console.log(response.data.endpoints)
        this.edit_info.all_endpoints = response.data.endpoints
      }).catch(error => {
        console.log(error);
      })
    },

    /******************************************************/


    resetEditInfo(service_name) {
      this.edit_info.service_name = service_name;
      this.edit_info.endpoint = '';
      this.getAllEndpoints(service_name);
    },

    edit(item) {
      this.resetEditInfo(item.service_name);
      this.edit_service_switch = true;
    },

    saveEdit() {
      const path = 'http://wish-nginx-ui.com/api/services/' + this.edit_info.service_name;
      let params = {};
      params.endpoint = this.edit_info.endpoint;
      axios.put(path, params).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.getService()
      this.edit_service_switch = false;
    },
    cancelEdit() {
      this.edit_service_switch = false;
    }
  },
}
</script>
