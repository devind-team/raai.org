<template lang="pug">
apollo-query(
  v-slot="{ result: { loading, error, data } }"
  :query="require('~/gql/core/queries/profile_information.graphql')"
  :variables="{ userId: user.id }"
  tag
)
  v-progress-circular.ma-auto(v-if="loading" indeterminate color="primary")
  v-alert(v-else-if="error" type="error") {{ error }}
  template(v-else-if="data")
    v-row(v-for="profile in data.profileInformation.filter(p => p.available.length)" :key="profile.id")
      v-col.pt-6(cols="12" md="3") {{ profile.name }}
      v-col(cols="12" md="9")
        v-data-table(
          :headers="headers"
          :items="profile.available"
          hide-default-footer
          disable-pagination
        )
          template(#item.value="{ item }")
            template(v-if="kindTypes[item.kind] === 'bool'")
              | {{ item.value.value === 'true' ? $t('yes') : $t('no') }}
            template(v-else-if="kindTypes[item.kind] === 'choice'")
              | {{ choicesTypes[item.code].find(x => x.value === item.value.value).text }}
            span(v-else) {{ item.value.value }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { DataTableHeader } from 'vuetify'
import { useI18n } from '~/composables'
import { UserType } from '~/types/graphql'

export default defineComponent({
  props: {
    user: { type: Object as PropType<UserType>, required: true }
  },
  setup () {
    const { t } = useI18n()
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.tableHeaders.name') as string, value: 'name', width: '45%' },
      { text: t('profile.tableHeaders.value') as string, value: 'value', width: '55%' }
    ]))
    const kindTypes: ComputedRef<{ [key: string]: string }> = computed<{ [key: string]: string }>(() => ({
      A_0: 'text',
      A_1: 'date',
      A_2: 'bool',
      A_3: 'file',
      A_4: 'choice'
    }))
    const boolTypes: ComputedRef = computed(() => ([
      { text: t('yes') as string, value: 'true' },
      { text: t('no') as string, value: 'false' }
    ]))
    const choicesTypes: ComputedRef = computed(() => ({
      gender: [
        { text: t('profile.male') as string, value: '0' },
        { text: t('profile.female') as string, value: '1' }
      ]
    }))
    return { headers, kindTypes, boolTypes, choicesTypes }
  }
})
</script>

<style lang="sass">
.profile-information__expansion-panel-content
  .v-expansion-panel-content__wrap
    padding-left: 0
    padding-right: 0
</style>
