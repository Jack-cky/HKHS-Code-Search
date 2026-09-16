import type { SearchResponse, SearchResult } from "../api/types";
import { escapeHtml } from "../utils";

const LEVEL_NAME = { 2: "Chapter", 4: "Heading", 6: "Subheading", 8: "HKHS" } as const;

const SECTIONS: [number, string, string][] = [
  [5, "🐄", "Live animals; animal products"],
  [14, "🥦", "Vegetable products"],
  [15, "🫒", "Fats & oils"],
  [24, "🍱", "Prepared foodstuffs; beverages; tobacco"],
  [27, "⛏️", "Mineral products"],
  [38, "🧪", "Chemical products"],
  [40, "🧴", "Plastics & rubber"],
  [43, "👜", "Hides, leather & furskins; travel goods"],
  [46, "🪵", "Wood & articles of wood"],
  [49, "📄", "Wood pulp; paper"],
  [63, "🧵", "Textiles & textile articles"],
  [67, "👟", "Footwear & headgear"],
  [70, "🏺", "Stone, ceramic & glassware"],
  [71, "💎", "Pearls, precious stones & metals; jewellery"],
  [83, "🔩", "Base metals & articles thereof"],
  [85, "⚙️", "Machinery & electrical equipment"],
  [89, "🚗", "Transport equipment"],
  [92, "🔬", "Precision & medical instruments; clocks; musical instruments"],
  [93, "🔫", "Arms & ammunition"],
  [96, "🛋️", "Furniture; toys & games; miscellaneous"],
  [97, "🖼️", "Works of art, collectors' pieces & antiques"],
  [99, "📦", "Commodities not classified according to kind"],
];

function sectionChip(code: string): string {
  const [, emoji, name] = SECTIONS.find(([end]) => Number(code.slice(0, 2)) <= end)!;
  return `<span class="dot" title="${name}">${emoji}</span>`;
}

function crumbs(code: string): string {
  const parts = [2, 4, 6].filter((d) => d < code.length).map((d) => `${LEVEL_NAME[d as 2 | 4 | 6]} ${code.slice(0, d)}`);
  return parts.join(`<span class="sep">›</span>`) || `${LEVEL_NAME[code.length as 2]}`;
}

function renderItem(r: SearchResult): string {
  const parents = r.hierarchy.slice(0, -1);
  const tree = parents
    .map((d, i) => {
      const digits = (2 * (i + 1)) as 2 | 4 | 6;
      return `<b>${LEVEL_NAME[digits]}</b><span>${escapeHtml(d)}</span>`;
    })
    .join("");
  const snippet = escapeHtml(r.hierarchy.at(-1) ?? "");
  return `<li>
    <div class="crumb">${sectionChip(r.code)}${crumbs(r.code)}</div>
    <button type="button" class="code" data-code="${r.code}" title="Copy code">${r.code}</button>
    ${parents.length ? `<details class="snippet"><summary>${snippet}</summary><div class="tree">${tree}</div></details>` : `<p class="snippet">${snippet}</p>`}
  </li>`;
}

export function renderResults(el: HTMLElement, r: SearchResponse, seconds: number, shown: number): void {
  if (!r.results.length) {
    el.innerHTML = `<p class="meta">No ${r.level} results for “${escapeHtml(r.query)}”. Try fewer or more generic words.</p>`;
    return;
  }
  const more = r.results.length - shown;
  el.innerHTML =
    `<p class="meta">About ${r.results.length} results (${seconds.toFixed(2)} seconds)</p>` +
    `<ol>${r.results.slice(0, shown).map(renderItem).join("")}</ol>` +
    (more > 0 ? `<button type="button" class="more">More results <small>(${more})</small></button>` : "");
}

export function renderStatus(el: HTMLElement, message: string, isError = false): void {
  el.innerHTML = `<p class="meta${isError ? " error" : ""}">${escapeHtml(message)}</p>`;
}

export function enableCopy(el: HTMLElement): void {
  el.addEventListener("click", async (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(".code");
    if (!btn) return;
    try {
      await navigator.clipboard.writeText(btn.dataset.code!);
      btn.dataset.copied = "";
      setTimeout(() => delete btn.dataset.copied, 1200);
    } catch { /* silently ignore */ }
  });
}
