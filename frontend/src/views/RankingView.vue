<script setup lang="ts">
import { ref } from 'vue'

import DetailCard from '@/components/DetailCard.vue'
import TaskCard from '@/components/TaskCard.vue'
import { fetch_metadata, fetch_qdpairs_unranked_one, fetch_query } from '@/utils/fetch'
import type { Metadata, Query } from '@/utils/types'

const query = ref<Query | null>(null)
const metadata = ref<Metadata | null>(null)
fetch_qdpairs_unranked_one().then((res) => {
  if (!res) {
    return
  }
  fetch_query(res.query_id).then((res) => {
    query.value = res
  })
  fetch_metadata(res.dataset_id).then((res) => {
    metadata.value = res
  })
})
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="300px"> <TaskCard></TaskCard></el-aside>
      <el-main><DetailCard :query="query" :metadata="metadata"></DetailCard></el-main>
    </el-container>
  </div>
</template>
