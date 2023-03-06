<template lang="pug">
v-card
  v-card-title {{ $t('ac.users.profile.name') }}
  v-card-subtitle {{ $t('ac.users.profile.createdAt') }} {{ dateTimeHM(viewUser.createdAt) }}
  v-card-text
    v-row
      v-col(cols="12" sm="3") {{ $t('ac.users.profile.avatar') }}
      v-col(cols="12" sm="9")
        avatar-view(:user="viewUser" :update="updateAvatar")
    basic-information(:user="viewUser" :can-change="viewUser.change")
    jobs-information(:user="viewUser")
    responsible-information(:user="viewUser")
    additional-information(
      v-if="hasPerm('core.view_user') || viewUser.id === user.id"
      :user="viewUser"
      :can-change="viewUser.change"
    )
    profile-information(v-else :user="viewUser")
    v-row(v-if="hasPerm('core.delete_user') && viewUser.id !== user.id")
      v-col(cols="12" sm="3") {{ $t('ac.users.profile.tableHeaders.blocking') }}
      v-col(cols="12" sm="9")
        v-btn(v-if="viewUser.isActive" color="error" @click="") {{ $t('ac.users.profile.buttons.blockUser') }}
        v-btn(v-else @click="" color="success") {{ $t('ac.users.profile.buttons.unblockUser') }}
        .caption.mt-2 {{ $t('ac.users.profile.blockingWarning') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent, computed, ref, useNuxtApp, inject, toRefs } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { ChangeAvatarMutationPayload, ProfileType, UserType } from '~/types/graphql'
import { useAuthStore } from '~/store'
import { useI18n, useFilters } from '~/composables'
import AvatarView from '~/components/eleden/ac/user/AvatarView.vue'
import BasicInformation from '~/components/profile/BasicInformation.vue'
import JobsInformation from '~/components/eleden/ac/user/JobsInformation.vue'
import ResponsibleInformation from '~/components/eleden/ac/user/ResponsibleInformation.vue'
import AdditionalInformation from '~/components/profile/AdditionalInformation.vue'
import ProfileInformation from '~/components/profile/ProfileInformation.vue'

type ChangeAvatarMutationType = { data: { changeAvatar: ChangeAvatarMutationPayload } }

export default defineComponent({
  components: {
    AvatarView,
    BasicInformation,
    JobsInformation,
    ResponsibleInformation,
    AdditionalInformation,
    ProfileInformation
  },
  middleware: 'auth',
  props: {
    viewUser: { type: Object as PropType<UserType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const authStore = useAuthStore()
    const { hasPerm, user } = toRefs(authStore)
    const { $store } = useNuxtApp()

    const { dateTimeHM } = useFilters()

    const section = ref<{ [key: string]: { [key: string]: string }[] }>()
    const profile = ref<ProfileType>()

    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('ac.users.profile.tableHeaders.name') as string, value: 'name' },
      { text: t('ac.users.profile.tableHeaders.value') as string, value: 'value' }
    ]))

    const userUpdate: any = inject('userUpdate')
    const updateAvatar = (cache: DataProxy, result: ChangeAvatarMutationType) => {
      userUpdate(cache, result, (dataCache, { data: { changeAvatar: { avatar, success } } }) => {
        if (success) {
          dataCache.user.avatar = avatar
          if (user.value.id === props.viewUser.id) {
            $store.dispatch('auth/changeUserAvatar', avatar)
          }
        }
        return dataCache
      })
    }

    return { hasPerm, user, dateTimeHM, section, profile, headers, updateAvatar }
  }
})
</script>
