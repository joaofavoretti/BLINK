<template>
  <div>
    <v-card class="ma-5 pa-5">
      <v-row>
        <v-col class="text-h2">
          Details
        </v-col>
        <v-col cols="auto">
         
          <v-btn
            v-if="!url.manual_inspection"
            dark
            fab
            small
            color="orange"
            class="ml-2"
            @click="url.manual_inspection = { triggered: false, comments: ''}"
          >
            <v-icon>mdi-magnify</v-icon> 
            <span class="ml-2">Inspect</span>
          </v-btn>
          <v-btn
            v-else
            :color="url.manual_inspection.triggered ? 'red' : 'green'"
            dark
            fab
            small
            class="ml-2"
            @click="url.manual_inspection.triggered = !url.manual_inspection.triggered"
          >
            <v-icon>{{ url.manual_inspection.triggered ? 'mdi-virus' : 'mdi-virus-off' }}</v-icon>
            <span class="ml-2">{{ url.manual_inspection.triggered ? 'Malicious' : 'Benign' }}</span>
          </v-btn>
          
          <v-btn
            v-if="next_id"
            fab
            dark
            small
            color="blue"
            @click="nextDocument"
            class="ml-2"
          >
            <v-icon>mdi-arrow-right</v-icon>
          </v-btn>

          <v-btn
            :color="url.online ? 'blue' : 'grey'"
            dark
            fab
            small
            class="ml-2"
            @click="url.online = !url.online"
          >
            <v-icon>{{ url.online ? 'mdi-power' : 'mdi-power-off' }}</v-icon>
            <span class="ml-2">{{ url.online ? 'Online' : 'Offline' }}</span>
          </v-btn>

          <v-btn
            icon
            flat
            small
            class="ml-2"
            @click="assistance = !assistance"
          >
            <v-icon>{{ assistance ? 'mdi-help-circle' : 'mdi-help-circle-outline' }}</v-icon>
          </v-btn>

          <v-btn
            icon
            flat
            small
            class="ml-2"
            :loading="loading"
            @click="save"
          >
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
          
          <v-btn
            icon
            flat
            @click="$router.go(-1)"
            small
            class="ml-2"
          >
            <v-icon>mdi-close</v-icon>
        </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          
          <v-list>
            <v-list-item
              title="URL"
            >
              <template v-slot:append>
                <a :href="url.url" target="_blank">{{  url.url }}</a>
              </template>
            </v-list-item>
          </v-list>
    
          <v-expansion-panels>
            <v-expansion-panel
              title="PhishTank Inspection"
              v-if="assistance && url.phishtank_inspection"
            >
              <v-expansion-panel-text>
                <v-row>
                  <v-col>
                    <v-list>
                      <v-list-item
                        title="Triggered"
                      >
                        <template v-slot:append>
                          <v-chip
                            :color="url.phishtank_inspection.triggered ? 'red' : 'green'"
                            dark
                            small
                          >
                            {{ url.phishtank_inspection.triggered ? 'Yes' : 'No' }}
                          </v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
            <v-expansion-panel
              title="Google Safe Browsing Inspection"
              v-if="assistance && url.gsb_inspection"
            >
              <v-expansion-panel-text>
                <v-row>
                  <v-col>
                    <v-list>
                      <v-list-item
                        title="Triggered"
                      >
                        <template v-slot:append>
                          <v-chip
                            :color="url.gsb_inspection.triggered ? 'red' : 'green'"
                            dark
                            small
                          >
                            {{ url.gsb_inspection.triggered ? 'Yes' : 'No' }}
                          </v-chip>
                        </template>  
                      </v-list-item>
                      <div v-if="url.gsb_inspection.comments">
                        <v-divider />
                        <v-list-item
                          title="Threat Type"
                        >
                          <template v-slot:append>
                            {{ url.gsb_inspection.comments.threatType }}
                          </template>
                        </v-list-item>
                        <v-divider />
                        <v-list-item
                          title="Platform Type"
                        >
                          <template v-slot:append>
                            {{ url.gsb_inspection.comments.platformType }}
                          </template>
                        </v-list-item>
                        <v-divider />
                        <v-list-item
                          title="Threat"
                        >
                          <template v-slot:append>
                            <a :href="url.gsb_inspection.comments.threat.url">{{ url.gsb_inspection.comments.threat.url }}</a>
                          </template>
                        </v-list-item>
                        <v-divider />
                        <v-list-item
                          title="Cache Duration"
                        >
                          <template v-slot:append>
                            {{ url.gsb_inspection.comments.cacheDuration }}
                          </template>
                        </v-list-item>
                        <v-divider />
                        <v-list-item
                          title="Threat Entry Type"
                        >
                          <template v-slot:append>
                            {{ url.gsb_inspection.comments.threatEntryType }}
                          </template>
                        </v-list-item>
                      </div>
                    </v-list>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
            <v-expansion-panel
              title="Manual Inspection"
              v-if="url.manual_inspection"
            >
              <v-expansion-panel-text>
                <v-row>
                  <v-col>
                    <v-list>
                      <v-list-item
                        title="Triggered"
                      >
                        <template v-slot:append>
                          <v-chip
                            :color="url.manual_inspection.triggered ? 'red' : 'green'"
                            dark
                            small
                          >
                            {{ url.manual_inspection.triggered ? 'Yes' : 'No' }}
                          </v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                    <v-textarea
                      v-model="url.manual_inspection.comments"
                      label="Comments"
                      outlined
                      rows="5"
                    >
                    </v-textarea>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script setup>
import ValidationService from '~/api/validationService'

const route = useRoute()
const router = useRouter()

const { data: resDocument } = await ValidationService.getDocument(route.params.id)
let url = ref(resDocument)
window.open(url.value.url, '_blank')

const { data: resNextDocument } = await ValidationService.getNextDocument(route.params.id)
const next_id = ref(resNextDocument.id)

let assistance = ref(false)

let loading = ref(false)

const save = async () => {
  // Change the ref object to a normal object
  try {
    loading.value = true
    const data = JSON.parse(JSON.stringify(url.value))
    const { data: res } = await ValidationService.updateDocument(route.params.id, data)
  } finally {
    loading.value = false
  }
}

const nextDocument = async () => {
  try {
    await save();
  } finally {
    router.replace(`/validation/id/${next_id.value}`)
  }
}

</script>

