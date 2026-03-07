<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&family=Inter:wght@300;400&display=swap" rel="stylesheet">
<style>
  .sf-card {
    width: 100%;
    max-width: 680px;
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-top: 2px solid #f0c040;
    position: relative;
    margin-bottom: 2rem;
  }
  .sf-card::before, .sf-card::after {
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    border-color: #f0c040;
    border-style: solid;
  }
  .sf-card::before { bottom: -1px; left: -1px; border-width: 0 0 2px 2px; }
  .sf-card::after  { bottom: -1px; right: -1px; border-width: 0 2px 2px 0; }

  .sf-terminal-bar {
    background: #111820;
    border-bottom: 1px solid #1e2d3d;
    padding: 0.55rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .sf-dot { width: 10px; height: 10px; border-radius: 50%; }
  .sf-dot-r { background: #ff5f57; }
  .sf-dot-y { background: #febc2e; }
  .sf-dot-g { background: #28c840; }
  .sf-terminal-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #5a6a7a;
    margin-left: auto;
    letter-spacing: 0.05em;
  }

  .sf-body { padding: 2.5rem 2.5rem 2rem; }

  .sf-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #b8922e;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }
  .sf-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 10vw, 5.5rem);
    line-height: 0.9;
    letter-spacing: 0.04em;
    color: #fff;
    margin: 0 0 0.15em;
  }
  .sf-title .sf-accent { color: #f0c040; }

  .sf-tagline {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #c9d1d9;
    line-height: 1.6;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #1e2d3d;
    max-width: 480px;
  }
  .sf-tagline strong { color: #f0c040; font-weight: 400; }

  .sf-divider {
    height: 1px;
    background: linear-gradient(90deg, #1e2d3d, transparent);
    margin: 1.75rem 0;
  }

  .sf-meta { display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center; }

  .sf-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 0.3rem 0.7rem;
    border: 1px solid #1e2d3d;
    background: #111820;
    color: #5a6a7a;
    letter-spacing: 0.05em;
  }
  .sf-status {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #28c840;
    box-shadow: 0 0 6px #28c840;
    animation: sf-pulse 2s ease-in-out infinite;
  }
  @keyframes sf-pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
  }

  .sf-link {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: #f0c040;
    text-decoration: none;
    letter-spacing: 0.04em;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    transition: color 0.2s;
  }
  .sf-link::before { content: '→'; color: #b8922e; }
  .sf-link:hover { color: #fff; }

  .sf-prompt {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #5a6a7a;
    margin-top: 1.75rem;
    padding: 0.85rem 1rem;
    background: rgba(0,0,0,0.3);
    border-left: 2px solid #f0c040;
  }
  .sf-prompt .sf-prefix { color: #f0c040; }
  .sf-cursor {
    display: inline-block;
    width: 8px;
    height: 1em;
    background: #f0c040;
    vertical-align: text-bottom;
    animation: sf-blink 1.1s step-end infinite;
    margin-left: 2px;
  }
  @keyframes sf-blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
  }
</style>

<div class="sf-card">
  <div class="sf-terminal-bar">
    <div class="sf-dot sf-dot-r"></div>
    <div class="sf-dot sf-dot-y"></div>
    <div class="sf-dot sf-dot-g"></div>
    <span class="sf-terminal-label">deathlabs / swordfish</span>
  </div>
  <div class="sf-body">
    <div class="sf-eyebrow">artificial intelligence · v0.0.1</div>
    <div class="sf-title"><span class="sf-accent">//</span> SWORD<span class="sf-accent">FISH</span></div>
    <p class="sf-tagline">
      An AI-powered interface for cutting through security data with speed and precision.
    </p>
    <div class="sf-divider"></div>
    <div class="sf-meta">
      <span class="sf-badge"><span class="sf-status"></span> active development</span>
      <a class="sf-link" href="https://deathlabs.github.io/swordfish/" target="_blank">
        deathlabs.github.io/swordfish
      </a>
    </div>
    <div class="sf-prompt">
      <span class="sf-prefix">$ </span>swordfish ask "show me all failed auth attempts in the last 24h"<span class="sf-cursor"></span>
    </div>
  </div>
</div>
