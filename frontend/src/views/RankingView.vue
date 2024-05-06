<script setup lang="ts">
import { ref, h } from 'vue'
import { ElNotification } from 'element-plus'

import DetailCard from '@/components/DetailCard.vue'
import TaskDesc from '@/components/TaskDesc.vue'
import { fetch_metadata, fetch_qdpairs_unranked_one, fetch_query } from '@/utils/fetch'
import type { QDPair, Metadata, Query } from '@/utils/types'

interface History extends QDPair {
  rank: number
}
const query = ref<Query | null>(null)
const metadata = ref<Metadata | null>(null)
const rank = ref<number>(0)

const history = ref<History[]>([])

const refresh = (rank: number) => {
  if (rank >= 0 && metadata.value && query.value) {
    const qdpairIndex = history.value.findIndex((qdpair) => {
      return (
        qdpair.dataset_id === metadata.value?.dataset_id &&
        qdpair.query_id === query.value?.query_id
      )
    })

    if (qdpairIndex !== -1) {
      history.value[qdpairIndex].rank = rank
    } else {
      history.value.unshift({
        dataset_id: metadata.value.dataset_id,
        query_id: query.value.query_id,
        rank: rank
      })
    }
  }
  fetch_qdpairs_unranked_one().then((res) => {
    if (!res) {
      return
    }
    fetch_query(res.query_id).then((res) => (query.value = res))
    fetch_metadata(res.dataset_id).then((res) => (metadata.value = res))
  })
}

const check_history = (idx: number) => {
  const qdpair = history.value[idx]
  fetch_query(qdpair.query_id).then((res) => (query.value = res))
  fetch_metadata(qdpair.dataset_id).then((res) => (metadata.value = res))
  rank.value = qdpair.rank
}

refresh(-1)

const active_items = ref<string[]>(['任务介绍', '标注历史'])
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="350px">
        <el-collapse v-model="active_items">
          <el-collapse-item title="任务介绍" name="任务介绍">
            <TaskDesc />
          </el-collapse-item>
          <el-collapse-item title="标注历史" name="标注历史">
            <el-table :data="history" style="width: 100%; margin-top: 8px" max-height="400">
              <el-table-column prop="dataset_id" label="Dataset ID" />
              <el-table-column prop="query_id" label="Query ID" />
              <el-table-column prop="rank" label="Rank" />
              <el-table-column fixed="right" label="Check">
                <template #default="scope">
                  <el-button link type="primary" @click.prevent="check_history(scope.$index)">
                    Check
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </el-aside>
      <el-main>
        <DetailCard
          :query="query"
          :metadata="metadata"
          :last_rank="rank"
          @refresh="
            (new_rank) => {
              rank = 0
              refresh(+new_rank)

              ElNotification({
                title: '标注统计',
                message: h('i', { style: 'color: teal' }, `已标注 ${history.length} 条数据`)
              })
            }
          "
        />
      </el-main>
    </el-container>
  </div>
</template>
