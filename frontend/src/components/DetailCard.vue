<script setup lang="ts">
import type { Query, Metadata } from '@/utils/types';

defineProps<{
  query: Query | null,
  metadata: Metadata | null
}>()
</script>

<template>
  <el-card>
    <h3>{{ query?.query_text }}</h3>
    <span
      ><p>{{ metadata?.origin_metadata }}</p></span
    >
  </el-card>
</template>
