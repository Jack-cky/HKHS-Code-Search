export function typewriter(input: HTMLInputElement, examples: string[], { type = 55, erase = 25, hold = 1800 } = {}): void {
  let i = 0, n = 0, deleting = false;

  const tick = () => {
    if (input.value || document.activeElement === input) {
      input.placeholder = ""; n = 0; deleting = false;
      return setTimeout(tick, 400);
    }
    const text = examples[i];
    n += deleting ? -1 : 1;
    input.placeholder = text.slice(0, n);
    let delay = deleting ? erase : type;
    if (!deleting && n === text.length) { deleting = true; delay = hold; }
    else if (deleting && n === 0) { deleting = false; i = (i + 1) % examples.length; delay = 300; }
    setTimeout(tick, delay);
  };
  input.addEventListener("focus", () => { input.placeholder = ""; });
  tick();
}
