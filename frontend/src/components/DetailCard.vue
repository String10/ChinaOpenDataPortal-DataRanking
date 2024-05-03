<script setup lang="ts">
import { ref, computed } from 'vue'

import { update_qdpairs_ranking } from '@/utils/fetch'
import type { Metadata, Query, RequestState } from '@/utils/types'

const props = defineProps<{
  query: Query | null
  metadata: Metadata | null
}>()

const rate = ref<number>(0)

const request_state = ref<RequestState | null>(null)
const button_type = computed<string>(() => {
  if (request_state.value === null) {
    return ''
  }
  return request_state.value.state === 0 ? 'success' : 'danger'
})
const updateRanking = () => {
  update_qdpairs_ranking(props.query!.query_id, props.metadata!.dataset_id, rate.value).then(
    (res) => {
      request_state.value = res
    }
  )
}
</script>

<template>
  <el-card>
    <h3>{{ query?.query_text }}</h3>
    <span
      ><p>{{ metadata?.origin_metadata }}</p></span
    >
    <div class="flex items-center text-sm">
      <el-radio-group v-model="rate" class="ml-4">
        <el-radio-button label="不相关" value="0" />
        <el-radio-button label="部分相关" value="1" />
        <el-radio-button label="高度相关" value="2" />
      </el-radio-group>
      <el-button style="margin-left: 20px" :type="button_type" @click="updateRanking">{{
        request_state && request_state.state > 0 ? '请重试' : '确定'
      }}</el-button>
    </div>
  </el-card>
</template>

<style scoped>
.el-radio-group {
  font-size: unset;
}
</style>
