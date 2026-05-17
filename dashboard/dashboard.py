import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ─────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ERP Closing Automation",
    page_icon="🏦",
    layout="wide"
)

# ─────────────────────────────────────────
#  ESTILO CUSTOMIZADO
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .main { background-color: #0f1117; }

    .metric-card {
        background: #1a1d27;
        border: 1px solid #2a2d3e;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .metric-card h2 {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2rem;
        margin: 0;
    }
    .metric-card p {
        color: #888;
        font-size: 0.85rem;
        margin: 4px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .ok    { color: #00d68f; }
    .warn  { color: #ffaa00; }
    .error { color: #ff4d6d; }

    .section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 8px;
    }
    .badge-ok    { background:#003d2a; color:#00d68f; padding:2px 10px; border-radius:20px; font-size:0.78rem; }
    .badge-warn  { background:#3d2e00; color:#ffaa00; padding:2px 10px; border-radius:20px; font-size:0.78rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  CARREGAR E VALIDAR DADOS
# ─────────────────────────────────────────
ARQUIVO = "data/lancamentos_contabeis_fake.xlsx"

@st.cache_data(show_spinner="Carregando lançamentos...")
def carregar_dados():
    df = pd.read_excel(ARQUIVO)
    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"])
    return df

@st.cache_data(show_spinner=False)
def rodar_validacoes(_df):
    hoje = pd.Timestamp(datetime.today().date())
    limite_suspeito = 40000
    return {
        "Débito e crédito zerados":         _df[(_df["debito"] == 0) & (_df["credito"] == 0)],
        "Débito e crédito simultâneos":     _df[(_df["debito"] > 0)  & (_df["credito"] > 0)],
        "Valores negativos":                _df[(_df["debito"] < 0)  | (_df["credito"] < 0)],
        "Datas futuras":                    _df[_df["data_lancamento"] > hoje],
        "Conta contábil inválida":          _df[(_df["conta_contabil"] < 10000) | (_df["conta_contabil"] > 99999)],
        f"Suspeitos (> R$ {limite_suspeito:,})": _df[(_df["debito"] > limite_suspeito) | (_df["credito"] > limite_suspeito)],
        "Documentos duplicados":            _df[_df.duplicated(subset=["documento_seq", "empresa"], keep=False)],
    }

if not os.path.exists(ARQUIVO):
    st.error(f"Arquivo não encontrado: `{ARQUIVO}`")
    st.info("Rode primeiro: `python src/generate_dataset.py`")
    st.stop()

df = carregar_dados()
inconsistencias = rodar_validacoes(df)

total           = len(df)
total_debitos   = df["debito"].sum()
total_creditos  = df["credito"].sum()
diferenca       = round(total_debitos - total_creditos, 2)
total_inc       = sum(len(v) for v in inconsistencias.values())

# ─────────────────────────────────────────
#  CABEÇALHO
# ─────────────────────────────────────────
st.markdown("## 🏦 ERP Closing Automation")
st.markdown(
    f"<span class='section-title'>Validação contábil · {datetime.now().strftime('%d/%m/%Y %H:%M')}</span>",
    unsafe_allow_html=True
)
st.divider()

# ─────────────────────────────────────────
#  KPIs
# ─────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color:#4d9fff">{total:,}</h2>
        <p>Lançamentos</p>
    </div>""", unsafe_allow_html=True)

with c2:
    cor = "error" if total_inc > 0 else "ok"
    st.markdown(f"""
    <div class="metric-card">
        <h2 class="{cor}">{total_inc:,}</h2>
        <p>Inconsistências</p>
    </div>""", unsafe_allow_html=True)

with c3:
    cor = "error" if diferenca != 0 else "ok"
    st.markdown(f"""
    <div class="metric-card">
        <h2 class="{cor}">R$ {diferenca:,.2f}</h2>
        <p>Diferença D/C</p>
    </div>""", unsafe_allow_html=True)

with c4:
    pct = round((total_inc / total) * 100, 1) if total > 0 else 0
    cor = "ok" if pct == 0 else "warn" if pct < 5 else "error"
    st.markdown(f"""
    <div class="metric-card">
        <h2 class="{cor}">{pct}%</h2>
        <p>Taxa de erro</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  LAYOUT PRINCIPAL
# ─────────────────────────────────────────
col_esq, col_dir = st.columns([1, 1], gap="large")

# ── CHECKLIST DE VALIDAÇÕES ──────────────
with col_esq:
    st.markdown("<p class='section-title'>Checklist de validações</p>", unsafe_allow_html=True)

    for nome, df_inc in inconsistencias.items():
        qtd = len(df_inc)
        badge = f"<span class='badge-ok'>✓ OK</span>" if qtd == 0 else f"<span class='badge-warn'>⚠ {qtd:,}</span>"
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:10px 14px;margin-bottom:6px;background:#1a1d27;"
            f"border-radius:6px;border-left:3px solid {'#00d68f' if qtd==0 else '#ffaa00'}'>"
            f"<span style='font-size:0.9rem'>{nome}</span>{badge}</div>",
            unsafe_allow_html=True
        )

# ── GRÁFICO DE BARRAS — INCONSISTÊNCIAS ──
with col_dir:
    st.markdown("<p class='section-title'>Inconsistências por tipo</p>", unsafe_allow_html=True)

    nomes = list(inconsistencias.keys())
    qtds  = [len(v) for v in inconsistencias.values()]
    cores = ["#00d68f" if q == 0 else "#ffaa00" for q in qtds]

    fig = go.Figure(go.Bar(
        x=qtds, y=nomes, orientation="h",
        marker_color=cores,
        text=[f"{q:,}" for q in qtds],
        textposition="outside",
        textfont=dict(color="#aaa", size=11)
    ))
    fig.update_layout(
        plot_bgcolor="#1a1d27", paper_bgcolor="#1a1d27",
        font=dict(color="#ccc", size=11),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=60, t=10, b=10),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─────────────────────────────────────────
#  GRÁFICOS DE ANÁLISE
# ─────────────────────────────────────────
col_a, col_b = st.columns(2, gap="large")

# ── LANÇAMENTOS POR ORIGEM ───────────────
with col_a:
    st.markdown("<p class='section-title'>Lançamentos por origem</p>", unsafe_allow_html=True)
    por_origem = df.groupby("origem").size().reset_index(name="total")
    fig2 = px.pie(
        por_origem, values="total", names="origem",
        color_discrete_sequence=["#4d9fff","#00d68f","#ffaa00","#ff4d6d","#b44dff"]
    )
    fig2.update_layout(
        plot_bgcolor="#1a1d27", paper_bgcolor="#1a1d27",
        font=dict(color="#ccc"), margin=dict(t=10, b=10),
        legend=dict(font=dict(size=11)), height=280
    )
    fig2.update_traces(textinfo="percent+label", textfont_size=11)
    st.plotly_chart(fig2, use_container_width=True)

# ── VOLUME POR MÊS ───────────────────────
with col_b:
    st.markdown("<p class='section-title'>Volume de lançamentos por mês</p>", unsafe_allow_html=True)
    df["mes"] = df["data_lancamento"].dt.to_period("M").astype(str)
    por_mes = df.groupby("mes").size().reset_index(name="total").sort_values("mes")
    fig3 = px.area(
        por_mes, x="mes", y="total",
        color_discrete_sequence=["#4d9fff"]
    )
    fig3.update_traces(fill="tozeroy", fillcolor="rgba(77,159,255,0.15)", line_width=2)
    fig3.update_layout(
        plot_bgcolor="#1a1d27", paper_bgcolor="#1a1d27",
        font=dict(color="#ccc"), margin=dict(t=10, b=10),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#2a2d3e", title=""),
        height=280
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ─────────────────────────────────────────
#  EQUILÍBRIO D/C
# ─────────────────────────────────────────
st.markdown("<p class='section-title'>Equilíbrio débitos × créditos</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Total Débitos",  f"R$ {total_debitos:,.2f}")
c2.metric("Total Créditos", f"R$ {total_creditos:,.2f}")
c3.metric("Diferença",      f"R$ {diferenca:,.2f}",
          delta="Equilibrado ✓" if diferenca == 0 else "Desequilibrado ⚠",
          delta_color="normal" if diferenca == 0 else "inverse")

st.divider()

# ─────────────────────────────────────────
#  TABELA DE DETALHES
# ─────────────────────────────────────────
st.markdown("<p class='section-title'>Detalhar inconsistência</p>", unsafe_allow_html=True)

opcoes_com_problema = {k: v for k, v in inconsistencias.items() if len(v) > 0}

if opcoes_com_problema:
    escolha = st.selectbox("Selecione uma validação para inspecionar:", list(opcoes_com_problema.keys()))
    df_selecionado = opcoes_com_problema[escolha]
    st.caption(f"{len(df_selecionado):,} registros encontrados")
    st.dataframe(
        df_selecionado.head(500),
        use_container_width=True,
        height=300
    )
else:
    st.success("✅ Nenhuma inconsistência encontrada — lançamentos estão todos válidos!")
