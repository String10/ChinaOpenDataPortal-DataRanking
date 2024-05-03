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
}

export type QDPair = {
  query_id: string
  dataset_id: string
}
