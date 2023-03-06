<template lang="pug">
v-progress-circular.mx-auto(v-if="userInformationLoading" indeterminate color="primary")
v-container(v-else)
  template(v-if="userInformation")
    v-card
      v-card-title {{ $getUserFullName(userInformation) }}
      v-card-subtitle
        a(:href="`mailto: ${userInformation.email}`") {{ userInformation.email }}
      v-card-text
        v-row
          v-col(cols="12" md="3") {{ $t('profile.me.avatar') }}
          v-col(cols="12" md="9" align="center")
            avatar-dialog(:item="userInformation" size="300")
        profile-information(:user="userInformation")
    v-card.mt-5
      v-card-title {{ $t('articles.name') }}
      v-card-text
        v-row(align="center")
          v-col(cols="12" md="9")
            items-data-filter(
              v-model="selectedYears"
              v-bind="getFilterMessages('yearsFilter')"
              :items="articlesYears.map(e => ({ id: e }))"
              message-container-class="mr-1 my-1"
              multiple
              has-select-all
            )
        articles-view(:articles="articles" :delete-article-update="deleteArticleUpdate" :totalCount="totalCount")
  v-row(v-else)
    v-col
      v-alert(type="warning") {{ $t('user.userPage.isHidden') }}
</template>

<script lang="ts">
import { defineComponent, ref, computed, useRoute, useNuxt2Meta } from '#app'
import { useI18n, useCommonQuery, useQueryRelay, useCursorPagination, useFilters } from '~/composables'
import {
  ArticlesYearsQuery,
  ArticlesYearsQueryVariables,
  UserQuery,
  UserQueryVariables,
  ArticlesQuery,
  ArticlesQueryVariables, UserType
} from '~/types/graphql'
import { FilterMessages } from '~/types/filters'
import articlesYearsQuery from '~/gql/eleden/queries/article/articles_years.graphql'
import userQuery from '~/gql/users/queries/user.graphql'
import articlesQuery from '~/gql/eleden/queries/article/articles.graphql'
import ArticlesView from '~/components/eleden/articles/ArticlesView.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import ProfileInformation from '~/components/profile/ProfileInformation.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

export default defineComponent({
  components: { ArticlesView, AvatarDialog, ProfileInformation, ItemsDataFilter },
  props: {
    search: { type: String, default: '' }
  },
  setup (props) {
    const route = useRoute()

    const { t, tc } = useI18n()
    const { getUserFullName } = useFilters()

    const selectedYears = ref<{ id: number }[]>([])

    const articlesVariables = computed<ArticlesQueryVariables>(() => ({
      users: [route.params.user_id],
      search: props.search,
      years: selectedYears.value.map(year => year.id)
    }))

    const { data: articlesYearsData } = useCommonQuery<ArticlesYearsQuery, ArticlesYearsQueryVariables>({
      document: articlesYearsQuery
    })
    const articlesYears = computed<number[]>(
      () => articlesYearsData.value ? articlesYearsData.value.articlesYears : []
    )
    const {
      data: userInformation,
      loading: userInformationLoading
    } = useCommonQuery<UserQuery, UserQueryVariables>({
      document: userQuery,
      variables: () => ({ userId: route.params.user_id })
    })
    const {
      data: articles,
      pagination: { totalCount },
      deleteUpdate: deleteArticleUpdate
    } = useQueryRelay<ArticlesQuery, ArticlesQueryVariables>({
      document: articlesQuery,
      variables: articlesVariables
    }, {
      pagination: useCursorPagination({ pageSize: 15 })
    })

    useNuxt2Meta(() => ({
      title: userInformation.value
        ? getUserFullName(userInformation.value as UserType)
        : t('user.userPage.isHiddenTitle') as string
    }))

    const getFilterMessages = (filterName: string, multiple: boolean = false): FilterMessages => {
      return {
        title: t(`articles.filters.${filterName}.title`) as string,
        noFiltrationMessage: t(`articles.filters.${filterName}.noFiltrationMessage`) as string,
        multipleMessageFunction: multiple
          ? (name, restLength) =>
              tc(`general.${filterName}.multipleMessage`, restLength, { name, restLength })
          : undefined
      }
    }

    return {
      selectedYears,
      articlesYears,
      userInformation,
      userInformationLoading,
      articles,
      totalCount,
      deleteArticleUpdate,
      getFilterMessages
    }
  }
})
</script>
