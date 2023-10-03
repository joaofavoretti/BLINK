// plugins/vuetify.js

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import { VDataTable } from 'vuetify/labs/VDataTable'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin((nuxtApp) => {
    const vuetify = createVuetify({
        ssr: true,
        components: {
            ...components,
            VDataTable,
        },
        directives,
        theme: {
            defaultTheme: 'dark',
        }
    })
    
    nuxtApp.vueApp.use(vuetify)
})
