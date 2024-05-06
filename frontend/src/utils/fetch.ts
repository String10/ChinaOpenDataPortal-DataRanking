import type { Metadata, DataFilePath, QDPair, Query, RequestState } from '@/utils/types'
import axios from 'axios'

const axios_config = {
  withCredentials: true
}

const fetch_factory = (fetch_fn: Function) => async (param: string) => {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    return fetch_fn(backend_host, param)
  } catch (error) {
    console.error(error)
  }
  return null
}

export const fetch_query = fetch_factory(
  async (backend_host: string, query_id: string) =>
    (await axios.get<Query>(`${backend_host}/query/${query_id}`, axios_config)).data
)

export const fetch_metadata = fetch_factory(
  async (backend_host: string, dataset_id: string) =>
    (await axios.get<Metadata>(`${backend_host}/metadata/${dataset_id}`, axios_config)).data
)

export const fetch_datafile_path = fetch_factory(
  async (backend_host: string, dataset_id: string) =>
    (
      await axios.get<DataFilePath[]>(
        `${backend_host}/metadata/datafilepath/${dataset_id}`,
        axios_config
      )
    ).data
)

export async function fetch_qdpairs_unranked_one() {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.get<QDPair>(`${backend_host}/qdpairs/unranked/one`, axios_config)
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
    const response = await axios.post<RequestState>(
      `${backend_host}/qdpairs/ranking`,
      {
        dataset_id,
        query_id,
        ranking
      },
      axios_config
    )
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}

export async function fetch_datafile_content(path: string) {
  const backend_host = import.meta.env.VITE_BACKEND_HOST
  if (!backend_host) {
    console.error('VUE_APP_BACKEND_HOST is not set')
    return null
  }
  try {
    const response = await axios.get<string[]>(
      `${backend_host}/datafile?path=${path}`,
      axios_config
    )
    return response.data
  } catch (error) {
    console.error(error)
  }
  return null
}
