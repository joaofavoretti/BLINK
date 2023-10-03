<template>
  <div>
    <v-card class="ma-5 pa-5">
      <v-row>
        <v-col class="text-h2">
          Statistics
        </v-col>
        <v-col cols="auto">
          <!-- Save button -->
          <v-btn
            color="blue"
            @click="save"
          >
            EXPORT CSV
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-list class="mt-5">
            <v-list-subheader>CommonCrawl</v-list-subheader>

            <v-list-item
              title="Benign"
            >
              <template v-slot:append>
                2453 (94.5%)
              </template>
            </v-list-item>

            <v-divider />

            <v-list-item
              title="Suspicious"
            >
              <template v-slot:append>
                141 (5.5%)
              </template>
            </v-list-item>
            
            <v-divider />

            <v-list-item
              title="Total"
              >
            <template v-slot:append>
              2594
            </template>
            </v-list-item>
            
          </v-list>

          <v-list class="mt-5">
            <v-list-subheader>Suspicious CommonCrawl Categories</v-list-subheader>
            
            <v-list-item
              title="Pornography"
            >
            <template v-slot:append>
              36 (39.5%)
            </template>
            </v-list-item>
            
            <v-divider />

            <v-list-item
              title="Phishing"
            >
            <template v-slot:append>
              9 (10%)
            </template>
            </v-list-item>

            <v-divider />

            <v-list-item
              title="Invalid Certificate"
            >
            <template v-slot:append>
              36 (39.5%)
            </template>
            </v-list-item>

            <v-divider />

            <v-list-item
              title="Multiple Ads"
            >
            <template v-slot:append>
              8 (9%)
            </template>
            </v-list-item>
            
            <v-divider />

            <v-list-item
              title="Casino App"
            >
            <template v-slot:append>
              1 (1%)
            </template>
            </v-list-item>
            
            <v-divider />

            <v-list-item
              title="Could not tell, but sth is wrong"
            >
            <template v-slot:append>
              1 (1%)
            </template>
            </v-list-item>
            
            <v-divider />

            <v-list-item
              title="Total"
            >
            <template v-slot:append>
              91
            </template>
            </v-list-item>

          </v-list>

          <v-list class="mt-5">
            <v-list-subheader>PhishTank</v-list-subheader>

            <v-list-item
              title="Benign"
            >
            <template v-slot:append>
              16 (7.5%)
            </template>
            </v-list-item>

            <v-divider />

            <v-list-item
              title="Suspicious"
            >
            <template v-slot:append>
              195 (92.5%)
            </template>
            </v-list-item>

            <v-divider />

            <v-list-item
              title="Total"
            >
            <template v-slot:append>
              211
            </template>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script setup>
import StatisticsService from '~/api/statisticsService';


const save = async () => {
  await StatisticsService.save();
}

</script>
