export type Level = "chapter" | "heading" | "subheading" | "hkhs";

export interface SearchResult {
  code: string;
  hierarchy: string[];
}

export interface SearchResponse {
  query: string;
  level: Level;
  results: SearchResult[];
}
