import type { Level, SearchResponse } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "";

export async function search(q: string, level: Level, k: number): Promise<SearchResponse> {
  const params = new URLSearchParams({ q, level, k: String(k) });
  const res = await fetch(`${BASE_URL}/api/v1/search?${params}`);
  if (!res.ok) throw new Error(`Search failed (${res.status})`);
  return res.json();
}
