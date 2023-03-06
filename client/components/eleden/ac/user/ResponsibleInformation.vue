<template lang="pug">
v-row(v-if="user.responsibleTeams.length > 0")
  v-col.pt-8(cols="12" sm="3") {{ $t('ac.users.profile.tableHeaders.responsible') }}
  v-col(cols="12" sm="9")
    v-list
      v-list-item(v-for="team in user.responsibleTeams" :key="team.id" @click="")
        v-list-item-content
          v-list-item-title {{ team.name }} ({{ team.shortName }})
          v-list-item-subtitle {{ $t('ac.users.profile.responsible.admission') }} {{ team.admission }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { UserType } from '~/types/graphql'

export default defineComponent({
  props: {
    user: { required: true, type: Object as PropType<UserType> }
  }
})
</script>
