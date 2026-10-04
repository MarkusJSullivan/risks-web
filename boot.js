// Plain script, runs before the game page's own code: starts Pyodide in the background and answers the page's
// fetch('/api/...') calls from the Python rules (bridge.py). Everything else goes to the real fetch.
(function () {
  const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.2/full/";
  const realFetch = window.fetch.bind(window);

  const ready = (async () => {
    const { loadPyodide } = await import(PYODIDE + "pyodide.mjs");
    const py = await loadPyodide({ indexURL: PYODIDE });
    py.unpackArchive(await (await realFetch("dpia_tabletop.zip")).arrayBuffer(), "zip", { extractDir: "/home/pyodide" });
    py.FS.writeFile("/home/pyodide/bridge.py", await (await realFetch("bridge.py")).text());
    py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
    return py.pyimport("bridge");
  })();

  window.fetch = function (url, opts) {
    const path = new URL(url, location.href).pathname;
    const at = path.indexOf("/api/");
    if (at < 0) return realFetch(url, opts);
    return ready.then((bridge) => {
      const [status, text] = bridge.handle(path.slice(at), (opts && opts.body) || "{}").toJs();
      return new Response(text, { status, headers: { "Content-Type": "application/json" } });
    });
  };
})();
