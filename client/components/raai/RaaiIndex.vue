<template lang="pug">
v-container
  slot
  raai-goals
</template>

<script lang="ts">
import RaaiGoals from '~/components/raai/RaaiGoals.vue'

export default defineComponent({
  components: { RaaiGoals }
})
</script>
