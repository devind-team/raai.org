<template lang="pug">
v-row(v-if="user.jobs.length > 0")
  v-col.pt-6(cols="12" sm="3") {{ $t('ac.users.profile.tableHeaders.jobs') }}
  v-col(cols="12" sm="9")
    v-data-table(:headers="headers" :items="user.jobs" disable-pagination hide-default-footer)
      template(#item.team="{ item }")
        v-tooltip(bottom)
          template(#activator="{ on }")
            span(v-on="on") {{ item.team.shortName }}
          span {{ item.team.name }}
      template(#item.post="{ item }")
        template(v-if="item.jobPosts")
          template(v-for="(jobPost, i) in item.jobPosts") {{ jobPost.post.name }}
            span(v-if="i !== item.jobPosts.length - 1") ,#{' '}
        strong(v-else) &mdash;
</template>

<script lang="ts">
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { UserType } from '~/types/graphql'
import { useI18n } from '~/composables'

export default defineComponent({
  props: {
    user: { required: true, type: Object as PropType<UserType> }
  },
  setup () {
    const { t } = useI18n()

    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('ac.users.profile.jobs.tableHeaders.team') as string, value: 'team', width: '45%' },
      { text: t('ac.users.profile.jobs.tableHeaders.post') as string, value: 'post', width: '55%' }
    ]))

    return { headers }
  }
})
</script>
