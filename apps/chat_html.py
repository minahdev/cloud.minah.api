from __future__ import annotations

import html

from chat_mirror import LastChatSnapshot


def _esc(text: str) -> str:
    return html.escape(text)


def render_chat_page(snapshot: LastChatSnapshot | None) -> str:
    if snapshot is None:
        body = """
        <p class="empty">아직 대화가 없습니다.</p>
        <p class="hint">프론트(3000) 홈에서 Gemini 채팅으로 질문하면 여기에 답변이 표시됩니다.</p>
        """
    else:
        model_label = (
            f'<span class="model-tag">{_esc(snapshot.model_name)}</span>'
            if snapshot.model_name
            else ""
        )
        body = f"""
        <article class="bubble user">
          <p class="role">질문</p>
          <p class="text">{_esc(snapshot.user_text)}</p>
        </article>
        <article class="bubble model">
          <p class="role">Gemini 답변 {model_label}</p>
          <div class="text answer">{_esc(snapshot.model_text).replace(chr(10), "<br />")}</div>
        </article>
        <p class="updated">갱신: {_esc(snapshot.updated_at)}</p>
        """

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Pace · Gemini 채팅 미러</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0a0f0d;
      --card: rgba(18, 28, 24, 0.95);
      --border: rgba(74, 222, 128, 0.2);
      --text: #e8f0ec;
      --muted: #8fa89a;
      --primary: #4ade80;
      --user-bg: rgba(74, 222, 128, 0.12);
      --model-bg: rgba(255, 255, 255, 0.05);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 1.5rem;
    }}
    .wrap {{ max-width: 40rem; margin: 0 auto; }}
    h1 {{ font-size: 1.1rem; margin: 0 0 0.25rem; }}
    .sub {{ font-size: 0.8rem; color: var(--muted); margin: 0 0 1.25rem; }}
    .panel {{
      border: 1px solid var(--border);
      border-radius: 1rem;
      background: var(--card);
      padding: 1.25rem;
      min-height: 12rem;
    }}
    .bubble {{
      border-radius: 0.75rem;
      padding: 0.85rem 1rem;
      margin-bottom: 0.75rem;
    }}
    .bubble.user {{ background: var(--user-bg); border: 1px solid var(--border); }}
    .bubble.model {{ background: var(--model-bg); }}
    .role {{
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--primary);
      margin: 0 0 0.35rem;
    }}
    .bubble.model .role {{ color: var(--muted); }}
    .text {{ margin: 0; font-size: 0.95rem; line-height: 1.55; white-space: pre-wrap; }}
    .answer {{ color: var(--text); }}
    .model-tag {{
      font-size: 0.65rem;
      font-weight: normal;
      color: var(--muted);
      margin-left: 0.35rem;
    }}
    .updated {{ font-size: 0.7rem; color: var(--muted); margin: 0.5rem 0 0; }}
    .empty {{ margin: 0; font-size: 1rem; }}
    .hint {{ margin: 0.5rem 0 0; font-size: 0.85rem; color: var(--muted); line-height: 1.5; }}
    nav {{ margin-top: 1rem; font-size: 0.8rem; }}
    nav a {{ color: var(--primary); margin-right: 1rem; }}
    .live {{ font-size: 0.7rem; color: var(--muted); margin-top: 0.75rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Gemini · 최근 대화</h1>
    <p class="sub">프론트 메인 채팅과 동기화됩니다 (2초마다 자동 갱신)</p>
    <div class="panel" id="chat-panel">{body}</div>
    <p class="live" id="live-status">동기화 중…</p>
    <nav>
      <a href="/">홈</a>
      <a href="/docs">API 문서</a>
      <a href="http://localhost:3000">프론트 (3000)</a>
    </nav>
  </div>
  <script>
    async function refresh() {{
      try {{
        const res = await fetch("/chat/last", {{ headers: {{ Accept: "application/json" }} }});
        const data = await res.json();
        const panel = document.getElementById("chat-panel");
        const status = document.getElementById("live-status");
        if (!data || !data.user_text) {{
          panel.innerHTML = `
            <p class="empty">아직 대화가 없습니다.</p>
            <p class="hint">프론트(3000) 홈에서 Gemini 채팅으로 질문하면 여기에 답변이 표시됩니다.</p>`;
          status.textContent = "대기 중 · " + new Date().toLocaleTimeString("ko-KR");
          return;
        }}
        const modelTag = data.model_name
          ? `<span class="model-tag">${{escapeHtml(data.model_name)}}</span>`
          : "";
        const answer = escapeHtml(data.model_text).replace(/\\n/g, "<br />");
        panel.innerHTML = `
          <article class="bubble user">
            <p class="role">질문</p>
            <p class="text">${{escapeHtml(data.user_text)}}</p>
          </article>
          <article class="bubble model">
            <p class="role">Gemini 답변 ${{modelTag}}</p>
            <div class="text answer">${{answer}}</div>
          </article>
          <p class="updated">갱신: ${{escapeHtml(data.updated_at || "")}}</p>`;
        status.textContent = "동기화됨 · " + new Date().toLocaleTimeString("ko-KR");
      }} catch (e) {{
        document.getElementById("live-status").textContent = "동기화 실패";
      }}
    }}
    function escapeHtml(s) {{
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }}
    refresh();
    setInterval(refresh, 2000);
  </script>
</body>
</html>"""
