export type Query = {
  query_id: string
  query_text: string
}

export type Metadata = {
  dataset_id: string
  description: string
  document: string
  origin_metadata: string
  title: string
  url: string
}

export type DataFilePath = {
  dataset_id: string
  path: string
}

export type QDPair = {
  query_id: string
  dataset_id: string
}

export type RequestState = {
  state: number
}
