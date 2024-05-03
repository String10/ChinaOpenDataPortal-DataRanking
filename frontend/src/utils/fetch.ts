import type { Metadata, QDPair, Query, RequestState } from '@/utils/types'
import axios from 'axios'

export async function fetch_query(query_id: string) {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.get<Query>(`${backend_host}/query/${query_id}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}

export async function fetch_metadata(dataset_id: string) {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.get<Metadata>(`${backend_host}/metadata/${dataset_id}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}

export async function fetch_qdpairs_unranked_one() {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.get<QDPair>(`${backend_host}/qdpairs/unranked/one`)
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}

export async function update_qdpairs_ranking(
  dataset_id: string,
  query_id: string,
  ranking: number
) {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.post<RequestState>(`${backend_host}/qdpairs/ranking`, {
      dataset_id,
      query_id,
      ranking
    })
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}
