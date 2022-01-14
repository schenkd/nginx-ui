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
        >
          <template v-slot:item.endpoint="{item}">
            <label>{{ item.endpoint }}
            </label>
            <v-chip class="ma-2" v-if="item.tag.length !== 0">{{
                item.tag
              }}
            </v-chip>
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
                    item-text="instance_id"
                    item-value="endpoint"
                    return-object
                    label="Please choose enpoint"
                    outlined
                    dense
                ></v-autocomplete>
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
      {text: "Endpoint", value: "endpoint", sortable: false},
      {text: "Action", value: "action", sortable: false},
    ],

    search: '',
    items: [
      {
        service_name: 'wishpost',
        endpoint: '',
        tag: '',
        all_endpoints: [
          {
            instance_id: 'conan-wishpost',
            endpoint: '1',
          },
          {
            instance_id: 'dan-wishpost',
            endpoint: '2',
          },
          {
            instance_id: 'frank-wishpost',
            endpoint: '3',
          },
        ]
      },
      {
        service_name: 'wishwms',
        endpoint: 'www.wishwms.com',
        tag: 'eks-prod',
        all_endpoints: [
          {
            instance_id: 'conan-wishpost',
            endpoint: '1',
          },
          {
            instance_id: 'dan-wishpost',
            endpoint: '2',
          },
          {
            instance_id: 'frank-wishpost',
            endpoint: '3',
          },
        ]
      },
      {
        service_name: 'wishrms',
        endpoint: 'www.wishrms.com',
        tag: 'eks-dev',
        all_endpoints: [
          {
            instance_id: 'conan-wishpost',
            endpoint: '1',
          },
          {
            instance_id: 'dan-wishpost',
            endpoint: '2',
          },
          {
            instance_id: 'frank-wishpost',
            endpoint: '3',
          },
        ]
      }
    ],

    edit_service_switch: false,
    edit_info: {
      service_name: '',
      endpoint: '',
      all_endpoints: [],
    }

  }),
  methods: {
    resetEditInfo(service_name, all_endpoints) {
      this.edit_info.service_name = service_name;
      this.edit_info.endpoint = '';
      this.edit_info.all_endpoints = all_endpoints;
    },

    edit(item) {
      this.resetEditInfo(item.service_name, item.all_endpoints);
      this.edit_service_switch = true;
    },

    saveEdit() {
      const path = 'http://localhost:8080/api/service';
      let params = {};
      params.service_name = this.edit_info.service_name;
      params.endpoint = this.edit_info.endpoint;
      axios.post(path, params).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })

      this.edit_service_switch = false;
    },
    cancelEdit() {
      this.edit_service_switch = false;
    }
  },
}
</script>
