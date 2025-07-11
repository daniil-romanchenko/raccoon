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
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 3. Set your OpenAI key (or adjust for local LLM)

```bash
export OPENAI_API_KEY=sk-...
```

### 4. Run Raccoon on a target

```bash
python main.py --url https://juice-shop.herokuapp.com
```

---

## 🧩 Components

| File         | Purpose                                          |
| ------------ | ------------------------------------------------ |
| `main.py`    | CLI runner for Raccoon                           |
| `browser.py` | Headless Chromium browser using Playwright       |
| `agent.py`   | LLM-powered planner built on Rigging             |
| `sink.py`    | Captures traffic as HAR or streams into ZAP/Burp |
| `prompts/`   | Customizable system prompts for the agent        |

---

## 🔌 Integrations

* ✅ **Burp Suite** – Launch Burp in headless mode and capture traffic via its extender API.
* ✅ **OWASP ZAP** – Use ZAP in daemon mode with proxy settings for live passive scanning.
* ✅ **HAR Export** – Save session traffic for replay or offline analysis.

---

## 🧠 How It Works

1. Playwright opens the target app and renders the page.
2. Raccoon's LLM agent analyzes the DOM and decides what to click or fill next.
3. The browser executes the action and captures all resulting requests/responses.
4. Traffic is forwarded to Burp/ZAP or written to a `.har` file.

---

## ⚠️ Legal

Only use Raccoon on applications you own or are authorized to test. Unauthorized use may be illegal and unethical.

---

## 👨‍💻 Author

Created by Daniil Romanchenko
AppSec Engineer, LLM Hacker, OSWE/OSCP/CSSLP
[LinkedIn](https://linkedin.com/in/daniil-romanchenko) | [HackTheBox](https://app.hackthebox.com/profile/759740)

---

## 📜 License

MIT

