# 🦝 Raccoon — LLM-Powered Application Reconnaissance Agent

**Raccoon** is a browser automation tool that uses an LLM to simulate human-like exploration of web applications. It renders modern JavaScript-heavy apps and intelligently interacts with UI elements to trigger as many different API calls and client-side behaviors as possible.

Captured network traffic is exported as HAR files or streamed into Burp Suite / OWASP ZAP for deeper analysis.

---

## 🎯 Features

- 🧠 **LLM Agent**: Plans actions like `click`, `fill`, `scroll` using OpenAI or local models via [Rigging](https://github.com/dreadnode/rigging).
- 🕸️ **Browser-based**: Uses Playwright to fully render SPAs and intercept all HTTP(S) traffic.
- 🔬 **Deep Coverage**: Finds and interacts with buttons, forms, modals, and dynamic routes missed by traditional scanners.
- 🛡️ **Plug into Burp or ZAP**: Send traffic directly into security tools for passive/active scanning.
- 🧰 **Modular Architecture**: Easy to extend with custom actions, prompts, or output formats.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/youruser/raccoon.git
cd raccoon
