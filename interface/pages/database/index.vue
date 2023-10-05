<template>
  <div>
    <v-card class="ma-5 pa-5">
      <v-row>
        <v-col>
          <div class="text-h2">Database</div>
        </v-col>
        <v-spacer />
        <v-col cols="auto">
          <v-btn
            color="blue"
            @click="showAddDialog = true"
          >
            Add
          </v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <div class="text-subtitle-1">This page should allow you to manipulate all the available URLs stored in the database.</div>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-data-table
            items-per-page="10"
            v-model:page = "page"
            :headers="headers"
            :items="urls"
            :loading="loading"
          >
            <template v-slot:[`item.url`]="{ item }">
              <p class="truncate">{{ item.raw.url }}</p>
            </template>
            <template v-slot:[`item.validated`]="{ item }">
              <v-chip
                :color="item.raw.validated ? 'green' : 'red'"
                dark
                small
              >
                {{ item.raw.validated ? 'Yes' : 'No' }}
              </v-chip>
            </template>
            <template v-slot:[`item.network_status`]="{ item }">
              <v-chip
                :color="item.raw.network_status == 'ONLINE' ? 'green' : 'red'"
                dark
                small
              >
                {{ item.raw.network_status}}
              </v-chip>
            </template>
            <template v-slot:[`item.id`]="{ item }">
              <v-btn
                icon
                flat
                :to="`/databse/id/${item.raw.id}`"
                small
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-card>

    <v-dialog width="500" v-model="showAddDialog" persistent>
      <v-card class="pa-5">
        <v-row>
          <v-col cols="auto">
            <div class="text-h4">Add More URLs</div>
          </v-col>
          <v-spacer />
          <v-col cols="auto">
            <v-btn
              icon
              flat
              @click="closeAddDialog"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        
        <v-row>
          <v-col>
            <div class="text-subtitle-1">This is a form to add more URLs to the database using different formats</div>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-select
              :items="['Common Crawl']"
              label="Source"
              v-model="URLSource"
            />
          </v-col>
        </v-row>

        <v-row v-if="URLSource == 'CSV' || URLSource == 'JSON'">
          <v-col>
            <v-file-input
              v-model="file"
              label="File Input"
              accept=".csv, .warc, .json"
              prepend-icon=""
            />
          </v-col>
        </v-row>
        <v-row v-else-if="URLSource == 'Common Crawl'">
          <v-col>
            <v-checkbox
              v-for="option in commonCrawlOptions"
              v-model="commonCrawlSelectedOptions"
              :value="option"
              hide-details
              :key="option"
              :label="option"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-spacer />
          <v-col cols="auto">
            <v-btn
              color="blue"
              @click="confirmURLAdd"
            >
              Confirm
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>
<script setup>
import UrlsService from '~/api/urlsService';

const route = useRoute()
const router = useRouter()

const page = ref(parseInt(route.query.page) || 1)
const headers = ref([
  { title: 'URL', align: 'start', sortable: false, key: 'url' },
  { title: 'Classification', align: 'center', key: 'classification' },
  { title: 'Category', align: 'center', key: 'content_category' },
  { title: 'Status', align: 'center', key: 'network_status' },
  { title: 'Details', align: 'end', key: 'id'}
])
const urls = ref([])
const loading = ref(false)
const showAddDialog = ref(false)
const URLSource = ref('')
const showFileInput = ref(false)
const commonCrawlOptions = ref([])
const commonCrawlSelectedOptions = ref([])

onMounted(async () => {
  await fetchUrls()
})

async function fetchUrls() {
  try {
    loading.value = true;
    const { data: res } = await UrlsService.getList();
    urls.value = res;
  } finally {
    loading.value = false;
  }
}

function closeAddDialog() {
  URLSource.value = ''
  showAddDialog.value = false
}

async function fetchCommonCrawlChoices() {
  if (commonCrawlOptions.value.length > 0) {
    return
  }
  const amount = 5
  const { data: res } = await UrlsService.getAvailableCommoncrawlFiles(amount);
  commonCrawlOptions.value = res.available_fnames
}

async function fetchPhishTankChoices() {
  return
}

async function confirmURLAdd() {
  return
}

watch(
  () => page.value,
  (newPage) => {
    router.push({ query: { page: newPage } });
  }
)

watch(
  () => URLSource.value,
  (newURLSource) => {
    if (newURLSource == 'CSV' || newURLSource == 'JSON') {
      showFileInput.value = true
    } else {
      showFileInput.value = false
    }

    if (newURLSource == 'Common Crawl') {
      fetchCommonCrawlChoices()
    }

    if (newURLSource == 'PhishTank') {
      fetchPhishTankChoices()
    }
  }
)

</script>

<style>
.truncate {
  width: 35rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>