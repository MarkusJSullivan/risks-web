// Loads Pyodide, unpacks the dpia_tabletop package and renders the card overview.
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.2/full/";

const status = document.getElementById("status");
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

async function main() {
  const { loadPyodide } = await import(PYODIDE + "pyodide.mjs");
  const py = await loadPyodide({ indexURL: PYODIDE });

  status.textContent = "Loading card data...";
  const zip = await (await fetch("dpia_tabletop.zip")).arrayBuffer();
  py.unpackArchive(zip, "zip", { extractDir: "/home/pyodide" });
  py.FS.writeFile("/home/pyodide/bridge.py", await (await fetch("bridge.py")).text());

  const overview = JSON.parse(py.runPython(`
import sys
sys.path.insert(0, "/home/pyodide")
import bridge
bridge.cards_overview("en")
`));
  render(overview);
}

function render(o) {
  document.getElementById("title").textContent = o.title;
  document.getElementById("scenario").textContent = o.scenario;
  const groups = {};
  for (const c of o.cards) (groups[c.kind || "other"] ??= []).push(c);
  document.getElementById("cards").innerHTML = Object.entries(groups)
    .map(([kind, cards]) => `<h2>${esc(kind)} (${cards.length})</h2><ul>` +
      cards.map((c) => `<li><strong>${esc(c.name)}</strong> <code>${esc(c.id)}</code>` +
        (c.family ? ` <em>${esc(c.family)}</em>` : "") + (c.text ? `<br>${esc(c.text)}` : "") + "</li>").join("") +
      "</ul>").join("");
  document.getElementById("sources").innerHTML =
    `${esc(o.sources.attribution)} <a href="${esc(o.sources.url)}">${esc(o.sources.primary)}</a>`;
  status.textContent = `Card set v${o.version}, ${o.cards.length} cards, rules running in Python (Pyodide).`;
}

main().catch((e) => { status.textContent = "Failed to load: " + e; console.error(e); });
