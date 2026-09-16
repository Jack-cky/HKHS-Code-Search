import { search } from "./api/client";
import type { Level, SearchResponse } from "./api/types";
import { enableCopy, renderResults, renderStatus } from "./components/results";
import { typewriter } from "./components/typewriter";

const FETCH = 20;
const PAGE = 5;

const EXAMPLES = [
  "cotton t-shirt, knitted",
  "frozen shrimp and prawns",
  "lithium-ion battery for laptop",
  "live horses for racing",
  "takoyaki cooking grill",
];

const logo = document.querySelector<HTMLAnchorElement>(".logo")!;
const form = document.querySelector<HTMLFormElement>("#search")!;
const input = document.querySelector<HTMLInputElement>("#q")!;
const clear = document.querySelector<HTMLButtonElement>("#clear")!;
const level = document.querySelector<HTMLSelectElement>("#level")!;
const results = document.querySelector<HTMLElement>("#results")!;
const footer = document.querySelector<HTMLElement>(".footer")!;

let seq = 0;
let last: { r: SearchResponse; seconds: number; shown: number } | null = null;

async function run(): Promise<void> {
  const q = input.value.trim();
  if (!q) { input.focus(); return; }
  const id = ++seq;
  const lvl = level.value as Level;
  if (document.body.classList.contains("home")) {
    footer.classList.add("leaving");
    setTimeout(() => footer.classList.remove("leaving"), 350); // matches --ease
  }
  document.body.classList.remove("home");
  document.title = `${q} - HS Code Search`;
  renderStatus(results, "Searching…");
  const t0 = performance.now();
  try {
    const r = await search(q, lvl, FETCH);
    if (id !== seq) return;
    last = { r, seconds: (performance.now() - t0) / 1000, shown: PAGE };
    renderResults(results, r, last.seconds, last.shown);
  } catch (e) {
    if (id === seq) renderStatus(results, (e as Error).message, true);
  }
}

function reset(): void {
  seq++;
  input.value = "";
  clear.hidden = true;
  results.innerHTML = "";
  document.body.classList.add("home");
  document.title = "HS Code Search";
}

form.addEventListener("submit", (e) => { e.preventDefault(); run(); });
input.addEventListener("input", () => { clear.hidden = !input.value; });
clear.addEventListener("click", () => { reset(); input.focus(); });
logo.addEventListener("click", (e) => { e.preventDefault(); reset(); });
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && document.activeElement === input) { e.preventDefault(); return input.blur(); }
  if (e.ctrlKey || e.metaKey || e.altKey || (e.target as HTMLElement).matches("input, select, textarea, button, a")) return;
  if (e.key === "/") { e.preventDefault(); input.focus(); }
  else if (e.key === "Enter") run();
});
enableCopy(results);
results.addEventListener("click", (e) => {
  if (!(e.target as HTMLElement).closest(".more") || !last) return;
  last.shown += PAGE;
  renderResults(results, last.r, last.seconds, last.shown);
});
typewriter(input, EXAMPLES);
