<template>
  <v-app>
    <v-navigation-drawer v-model="drawer">
      <v-list>
        <v-list-item to="/">
          <template v-slot:prepend>
            <v-icon>mdi-home</v-icon>
          </template>
          Home
        </v-list-item>
        <v-list-item to="/validation">
          <template v-slot:prepend>
            <v-icon>mdi-check-circle</v-icon>
          </template>
          Manual Validation
        </v-list-item>
        <v-list-item to="/share">
          <template v-slot:prepend>
            <v-icon>mdi-share-variant</v-icon>
          </template>
          Share
        </v-list-item>
        <v-list-item to="/statistics">
          <template v-slot:prepend>
            <v-icon>mdi-chart-bar</v-icon>
          </template>
          Statistics
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>

    <v-main>
      <NuxtPage />
    </v-main>
  </v-app>
</template>

<script setup>
  import { ref } from 'vue'

  const drawer = ref(null)
</script>

<script>
  export default {
    data: () => ({ drawer: null }),
  }
</script>
