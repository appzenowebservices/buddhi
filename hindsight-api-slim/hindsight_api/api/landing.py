"""The HTML page served at the API root.

A browser hitting the API's origin is usually a person checking that the server
is up, so ``/`` answers with a small status page instead of FastAPI's JSON 404:
the brand mark, the live health of the API and its database, the configured
model providers, and links to the docs and the Control Plane.

The styling mirrors the Control Plane's design system (light and dark tokens
from ``hindsight-control-plane/src/app/globals.css``), and the logo is served
by the API itself so the page pulls in nothing external.
"""

from __future__ import annotations

from html import escape

_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hindsight</title>
<style>
:root {
  color-scheme: light;
  --bg: #F3F5F9;
  --card: #FFFFFF;
  --fg: #0D1117;
  --muted: #525866;
  --border: rgba(0, 0, 0, .08);
  --subtle: rgba(0, 0, 0, .05);
  --primary: #0074D9;
  --gradient: linear-gradient(135deg, #0074d9 0%, #009296 100%);
  --success: #00BC7D;
  --danger: #D4183D;
  --warn: #F59E0B;
  --shadow: 0 20px 50px rgba(2, 8, 20, .12);
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --bg: #080C17;
    --card: #0F1724;
    --fg: #DCE8FF;
    --muted: #94A8C9;
    --border: rgba(100, 160, 255, .10);
    --subtle: rgba(100, 160, 255, .06);
    --primary: #5BB0FF;
    --success: #00D492;
    --shadow: 0 20px 60px rgba(0, 0, 0, .55);
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(720px 480px at 12% -5%, rgba(0, 116, 217, .16), transparent 60%),
    radial-gradient(720px 480px at 92% 105%, rgba(0, 146, 150, .16), transparent 60%),
    var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}
.card {
  width: 100%;
  max-width: 640px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  box-shadow: var(--shadow);
}
.brand { display: flex; flex-direction: column; align-items: center; gap: 14px; margin-bottom: 30px; }
.brand img { height: 84px; width: 84px; display: block; }
.wordmark {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -.02em;
  background: var(--gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
h1 {
  font-size: 32px;
  text-align: center;
  margin: 0 0 10px;
  letter-spacing: -.02em;
  background: var(--gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.sub { text-align: center; color: var(--muted); margin: 0 0 30px; }
.status { border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 13px 18px;
  border-top: 1px solid var(--subtle);
}
.row:first-child { border-top: 0; }
.label { color: var(--muted); font-size: 14px; }
.value { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: 14px; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight: 500; }
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--warn);
  display: inline-block;
  animation: pulse 1.6s infinite;
}
.dot.ok { background: var(--success); animation: none; box-shadow: 0 0 8px var(--success); }
.dot.bad { background: var(--danger); animation: none; box-shadow: 0 0 8px var(--danger); }
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, .5); }
  70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
  100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}
.actions { display: flex; gap: 12px; margin-top: 28px; flex-wrap: wrap; justify-content: center; }
a.btn {
  text-decoration: none;
  padding: 10px 18px;
  border-radius: 10px;
  border: 1px solid var(--border);
  color: var(--fg);
  font-weight: 600;
  font-size: 14px;
  transition: background .15s, border-color .15s, transform .15s;
}
a.btn:hover { background: var(--subtle); border-color: var(--primary); transform: translateY(-1px); }
a.btn.primary { background: var(--gradient); border: 0; color: #fff; }
.foot { text-align: center; color: var(--muted); font-size: 12px; margin: 22px 0 0; }
</style>
</head>
<body>
<main class="card">
  <div class="brand">
    <img src="__BASE_PATH__/logo.png" alt="Hindsight" onerror="this.style.display='none'">
    <span class="wordmark">Hindsight</span>
  </div>
  <h1>Welcome to your brain.</h1>
  <p class="sub">Agent memory that learns &mdash; up and ready to remember.</p>
  <section class="status">
    <div class="row">
      <span class="label">API Server</span>
      <span class="value"><span class="dot" id="api-dot"></span><span id="api-status">Checking&hellip;</span></span>
    </div>
    <div class="row">
      <span class="label">Database</span>
      <span class="value"><span class="dot" id="db-dot"></span><span id="db-status">Checking&hellip;</span></span>
    </div>
    <div class="row"><span class="label">LLM</span><span class="value mono">__LLM__</span></div>
    <div class="row"><span class="label">Embeddings</span><span class="value mono">__EMBEDDINGS__</span></div>
    <div class="row"><span class="label">Reranker</span><span class="value mono">__RERANKER__</span></div>
    <div class="row"><span class="label">Version</span><span class="value mono">v__VERSION__</span></div>
  </section>
  <div class="actions">
    <a class="btn primary" href="__BASE_PATH__/docs">API Docs</a>
    <a class="btn" id="ui-link" href="__BASE_PATH__/docs">Control Plane UI</a>
    <a class="btn" href="__BASE_PATH__/health">Health</a>
  </div>
  <p class="foot">Hindsight &middot; Agent Memory That Learns</p>
</main>
<script>
const BASE = "__BASE_PATH__";
function setStatus(id, ok, text) {
  const dot = document.getElementById(id + "-dot");
  const label = document.getElementById(id + "-status");
  if (dot) dot.className = "dot " + (ok ? "ok" : "bad");
  if (label && text) label.textContent = text;
}
async function refresh() {
  try {
    const res = await fetch(BASE + "/health", { cache: "no-store" });
    const body = await res.json();
    setStatus("api", true, "Running");
    const dbOk = body.database === "connected";
    setStatus("db", dbOk, dbOk ? "Connected" : (body.error || "Unavailable"));
  } catch (err) {
    setStatus("api", false, "Unreachable");
    setStatus("db", false, "Unknown");
  }
}
const ui = document.getElementById("ui-link");
if (ui) ui.href = location.protocol + "//" + location.hostname + ":9999";
refresh();
setInterval(refresh, 5000);
</script>
</body>
</html>
"""


def render_landing_page(
    *,
    version: str,
    base_path: str,
    llm_provider: str,
    llm_model: str,
    embeddings_provider: str,
    reranker_provider: str,
) -> str:
    """Fill the landing page template with the deployment's identity."""
    llm = f"{llm_provider} / {llm_model}" if llm_model else llm_provider
    return (
        _TEMPLATE.replace("__VERSION__", escape(version))
        .replace("__BASE_PATH__", escape(base_path, quote=True))
        .replace("__LLM__", escape(llm))
        .replace("__EMBEDDINGS__", escape(embeddings_provider))
        .replace("__RERANKER__", escape(reranker_provider))
    )
