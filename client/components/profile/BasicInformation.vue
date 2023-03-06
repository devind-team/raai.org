<template lang="pug">
apollo-mutation(
  v-if="canChange"
  v-slot="{ mutate, loading, error }"
  :mutation="require('~/gql/core/mutations/user/change_user_props.graphql')"
  :variables="{ userId: user.id, email, firstName, lastName, sirName, birthday }"
  tag
  @done="changeUserDone"
)
  validation-observer(v-slot="{ handleSubmit, invalid }")
    form(@submit.prevent="handleSubmit(mutate)")
      v-row
        v-col(cols="12" md="3") {{ $t('profile.information') }}
        v-col(cols="12" md="9")
          v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
          v-alert(type="error" :value="!!error" dismissible) {{$t('mutationBusinessLogicError', { error: error})}}
          v-text-field(
            :value="personalLink"
            :label="$t('profile.personalLink')"
            readonly
          )
            template(#append-outer)
              v-tooltip(bottom)
                template(#activator="{ on }")
                  v-btn(v-on="on" @click="copy(personalLink)" icon)
                    v-icon mdi-content-copy
                span {{ $t('copy') }}
          v-text-field(:value="user.username" :label="$t('profile.username')" readonly)
          validation-provider(:name="String($t('profile.email'))" rules="required|email" v-slot="{ errors, valid }")
            v-text-field(v-model="email" :label="$t('profile.email')" :error-messages="errors" :success="valid")
          validation-provider(
            :name="String($t('profile.lastName'))"
            rules="required|min:2|max:30"
            v-slot="{ errors, valid }"
          )
            v-text-field(v-model="lastName" :label="$t('profile.lastName')" :error-messages="errors" :success="valid")
          validation-provider(
            :name="String($t('profile.firstName'))"
            rules="required|min:2|max:30"
            v-slot="{ errors, valid }"
          )
            v-text-field(v-model="firstName" :label="$t('profile.firstName')" :error-messages="errors" :success="valid")
          validation-provider(
            :name="String($t('profile.sirName'))"
            rules="required|min:2|max:30"
            v-slot="{ errors, valid }"
          )
            v-text-field(v-model="sirName" :label="$t('profile.sirName')" :error-messages="errors" :success="valid")
          v-menu(
            v-model="menu"
            :close-on-content-click="false"
            bottom max-width="290px"
            transition="scale-transition"
            min-width="290px"
          )
            template(v-slot:activator="{ on }")
              validation-provider(
                :name="String($t('profile.birthday'))"
                v-slot="{ errors, valid }"
                tag="div"
              )
                v-text-field(
                  v-on="on"
                  v-model="birthday"
                  :error-messages="errors"
                  :success="valid"
                  :label="$t('profile.birthday')"
                  readonly
                )
            v-date-picker(v-model="birthday" @input="menu = false")
      v-row
        v-col.text-right
          v-btn.mb-1(:disabled="invalid" :loading="loading" type="submit" color="success") {{ $t('save') }}
v-row(v-else)
  v-col.pt-6(cols="12" md="3") {{ $t('profile.information') }}
  v-col(cols="12" md="9")
    v-data-table(:headers="readonlyHeaders" :items="readOnlyItems" hide-default-footer disable-pagination)
      template(#item.value="{ item }")
        template(v-if="item.value")
          a(v-if="item.key === 'personalLink'" :href="item.value") {{ item.value }}
          span(v-else-if="item.key === 'birthday'") {{ dateTimeHM(item.value) }}
          span(v-else) {{ item.value }}
        span.font-italic(v-else) {{ $t('notFilled') }}
</template>

<script lang="ts">
import { promiseTimeout, useClipboard } from '@vueuse/core'
import type { PropType } from '#app'
import { computed, defineComponent, ref, toRef } from '#app'
import { DataTableHeader } from 'vuetify'
import { ChangeUserPropsMutationPayload, UserType } from '~/types/graphql'
import { useAuthStore } from '~/store'
import { useFilters, useI18n } from '~/composables'

type ChangeUserPropsResultMutation = { data: { changeUserProps: ChangeUserPropsMutationPayload } }

export default defineComponent({
  props: {
    user: { type: Object as PropType<UserType>, required: true },
    canChange: { type: Boolean, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()

    const { copy } = useClipboard()
    const userStore = useAuthStore()
    const user = toRef(userStore, 'user')

    const successUpdate = ref<boolean>(false)
    const menu = ref<boolean>(false)
    const lastName = ref<string>(props.user.lastName)
    const firstName = ref<string>(props.user.firstName)
    const sirName = ref<string>(props.user.sirName)
    const email = ref<string>(props.user.email)
    const birthday = ref<string>(props.user.birthday)

    const personalLink = computed<string>(() => {
      const param: string = `/users/${props.user.id}`
      return process.client ? `${window.location.protocol}//${window.location.host}${param}` : param
    })

    const changeUserDone = (
      { data: { changeUserProps: { success, user: updatedUser } } }: ChangeUserPropsResultMutation
    ) => {
      if (success) {
        user.value = Object.assign(user.value, updatedUser)
        successUpdate.value = true
        promiseTimeout(2000).then(() => (successUpdate.value = false))
      }
    }

    const readonlyHeaders = computed<DataTableHeader[]>(() => ([
      { text: t('profile.tableHeaders.name') as string, value: 'name', width: '45%' },
      { text: t('profile.tableHeaders.value') as string, value: 'value', width: '55%' }
    ]))
    const readOnlyItems = computed<{ key: string, name: string, value: string }[]>(() => [
      { key: 'personalLink', name: t('profile.personalLink') as string, value: personalLink.value },
      { key: 'username', name: t('profile.username') as string, value: props.user.username },
      { key: 'lastName', name: t('profile.lastName') as string, value: props.user.lastName },
      { key: 'firstName', name: t('profile.firstName') as string, value: props.user.firstName },
      { key: 'sirName', name: t('profile.sirName') as string, value: props.user.sirName },
      { key: 'birthday', name: t('profile.birthday') as string, value: props.user.birthday }
    ])

    return {
      dateTimeHM,
      successUpdate,
      menu,
      lastName,
      firstName,
      sirName,
      email,
      birthday,
      copy,
      personalLink,
      changeUserDone,
      readonlyHeaders,
      readOnlyItems
    }
  }
})

</script>
