<template>
  <div>
    <v-card class="ma-5 pa-5">
      <div class="text-h2">Validation</div>
      <div class="text-subtitle-1">This page should allow you to manipulate all the available URLs stored in the database.</div>
      <v-data-table
        items-per-page="10"
        v-model:page = "page"
        :headers="headers"
        :items="urls"
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
        <template v-slot:[`item.online`]="{ item }">
          <v-chip
            :color="item.raw.online ? 'green' : 'red'"
            dark
            small
          >
            {{ item.raw.online ? 'Online' : 'Offline' }}
          </v-chip>
        </template>
        <template v-slot:[`item.id`]="{ item }">
          <!-- Button to details -->
          <v-btn
            icon
            flat
            :to="`/validation/id/${item.raw.id}`"
            small
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
    </v-data-table>
    </v-card>
  </div>
</template>
<script setup>
import ValidationService from '~/api/validationService';

const route = useRoute()
const router = useRouter()

const page = ref(parseInt(route.query.page) || 1)
const headers = ref([
  { title: 'Validated', align: 'center', key: 'validated' },
  { title: 'URL', align: 'start', sortable: false, key: 'url' },
  { title: 'Status', align: 'center', key: 'online' },
  { title: 'Action', align: 'end', key: 'id'}
])
const urls = ref([])

const { data: res } = await ValidationService.getList();
urls.value = res;

watch(
  () => page.value,
  (newPage) => {
    router.push({ query: { page: newPage } });
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