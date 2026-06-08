# Copyright (c) 2026 Gabriel Mahia / AI Kung Fu LLC. MIT License.
# portfolio-pulse — East Africa AI Stack Portfolio Command Center
# Inspired by: Rundown AI "Build a Daily Command Center" (Apr 21, 2026)
#              Rundown AI "Build Automated Business Reports with AI" (May 18, 2026)
# =============================================================================

import streamlit as st
import urllib.request
import json
import datetime

st.set_page_config(
    page_title="Portfolio Pulse — East Africa AI Stack",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .stApp { background: #050d1a; }
  .metric-card { background: #0a1828; border: 1px solid #1e4080; border-radius: 10px;
                 padding: 14px; margin: 6px; text-align: center; }
  .metric-num  { font-size: 2rem; font-weight: 800; color: #4fc3f7; }
  .metric-lbl  { font-size: 0.75rem; color: #4a7099; margin-top: 2px; }
  .platform-h  { font-size: 0.85rem; font-weight: 700; color: #90caf9;
                 border-bottom: 1px solid #1e3a5f; padding-bottom: 4px; margin-bottom: 8px; }
  .repo-chip   { display: inline-block; background: #0d2137; border: 1px solid #1a4a7a;
                 border-radius: 12px; padding: 2px 9px; margin: 2px;
                 font-size: 0.7rem; color: #64b5f6; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 📊 Portfolio Pulse — East Africa AI Stack")
st.caption(f"Live portfolio health across all platforms · {datetime.date.today()}")
st.markdown("---")

# ── Fetch GitHub stats ────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_github_stats():
    try:
        url = "https://api.github.com/users/gabrielmahia"
        req = urllib.request.Request(url, headers={"User-Agent": "portfolio-pulse/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        return {
            "repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
        }
    except: return {"repos": 116, "followers": 0, "following": 0}

@st.cache_data(ttl=300)
def get_repo_stars(repos):
    stars = {}
    for repo in repos:
        try:
            url = f"https://api.github.com/repos/gabrielmahia/{repo}"
            req = urllib.request.Request(url, headers={"User-Agent": "portfolio-pulse/1.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                d = json.loads(r.read())
            stars[repo] = {"stars": d.get("stargazers_count", 0),
                           "forks": d.get("forks_count", 0),
                           "watchers": d.get("watchers_count", 0)}
        except: stars[repo] = {"stars": 0, "forks": 0, "watchers": 0}
    return stars

@st.cache_data(ttl=600)
def get_pypi_stats(package):
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "portfolio-pulse/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        info = data.get("info", {})
        return {
            "version": info.get("version", "?"),
            "author": info.get("author", "?"),
            "classifiers": len(info.get("classifiers", [])),
        }
    except: return {"version": "?", "author": "?", "classifiers": 0}

@st.cache_data(ttl=600)
def get_devto_stats():
    try:
        url = "https://dev.to/api/articles?username=gabrielmahia&per_page=50"
        req = urllib.request.Request(url, headers={"User-Agent": "portfolio-pulse/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            articles = json.loads(r.read())
        total_reactions = sum(a.get("positive_reactions_count", 0) for a in articles)
        total_comments  = sum(a.get("comments_count", 0) for a in articles)
        total_views     = sum(a.get("page_views_count", 0) for a in articles)
        return {
            "articles": len(articles),
            "reactions": total_reactions,
            "comments": total_comments,
            "views": total_views,
            "latest": articles[0].get("title","—") if articles else "—",
        }
    except: return {"articles": 8, "reactions": 0, "comments": 0, "views": 0, "latest": "—"}

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Fetching live portfolio data..."):
    gh = get_github_stats()
    KEY_REPOS = ["mpesa-mcp", "wapimaji-mcp", "civic-agent-kit", "remit-mcp",
                 "shamba-scan-ai", "afya-chw-ai", "haki-debate-ai", "kenya-nowcast",
                 "claude-east-africa-skills", "portfolio-pulse", "bima-mcp"]
    repo_stats = get_repo_stars(KEY_REPOS)
    pypi_mpesa = get_pypi_stats("mpesa-mcp")
    pypi_wapi  = get_pypi_stats("wapimaji-mcp")
    pypi_civic = get_pypi_stats("civic-agent-kit")
    pypi_remit = get_pypi_stats("remit-mcp")
    devto = get_devto_stats()

# ── Top-level KPIs ────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("GitHub Repos", gh["repos"], help="Total public repos")
k2.metric("PyPI Packages", 4, help="mpesa-mcp, wapimaji-mcp, civic-agent-kit, remit-mcp")
k3.metric("Dev.to Articles", devto["articles"])
k4.metric("HuggingFace Datasets", 4)
k5.metric("Kaggle Notebooks", 5)

st.markdown("---")

# ── GitHub section ────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="platform-h">🐙 GitHub — Key Repos</div>', unsafe_allow_html=True)
    rows = []
    for repo, s in repo_stats.items():
        rows.append({"Repo": repo, "⭐ Stars": s["stars"], "🍴 Forks": s["forks"]})
    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Followers: {gh['followers']} · Total repos: {gh['repos']} · github.com/gabrielmahia")

with col2:
    st.markdown('<div class="platform-h">📦 PyPI Packages</div>', unsafe_allow_html=True)
    for pkg, info in [("mpesa-mcp", pypi_mpesa), ("wapimaji-mcp", pypi_wapi),
                       ("civic-agent-kit", pypi_civic), ("remit-mcp", pypi_remit)]:
        v = info.get("version", "?")
        st.markdown(f"**{pkg}** `v{v}`")
    st.caption("pypi.org/user/gmahia")

# ── Dev.to + research ─────────────────────────────────────────────────────────
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="platform-h">📝 Dev.to</div>', unsafe_allow_html=True)
    st.metric("Articles", devto["articles"])
    st.metric("Reactions", devto["reactions"])
    st.caption(f"Latest: {devto['latest'][:50]}")

with c2:
    st.markdown('<div class="platform-h">🤗 HuggingFace</div>', unsafe_allow_html=True)
    datasets = ["swahili-civic-nlp", "kenya-agricultural-qa",
                "kenya-legal-nlp", "swahili-health-corpus"]
    for ds in datasets:
        st.markdown(f'<span class="repo-chip">{ds}</span>', unsafe_allow_html=True)
    st.caption("huggingface.co/gmahia")

with c3:
    st.markdown('<div class="platform-h">📊 Kaggle</div>', unsafe_allow_html=True)
    notebooks = ["kenya-water-stress-analysis", "kenya-civic-data-quick-start",
                 "kenya-satellite-economic-nowcasting", "swahili-ai-accuracy-gap",
                 "stock-market-analysis-prediction-using-lstm"]
    for nb in notebooks:
        st.markdown(f'<span class="repo-chip">{nb}</span>', unsafe_allow_html=True)
    st.caption("kaggle.com/gmahia")

st.markdown("---")
st.caption("📊 portfolio-pulse · East Africa AI Stack · gabrielmahia.github.io · MIT License")
st.caption("Live data from GitHub API, PyPI API, Dev.to API. Cached 5–10 min.")
