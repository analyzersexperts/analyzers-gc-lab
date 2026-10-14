import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Analyzers Experts | Laboratório de Cromatografia Gasosa",
    page_icon="🧪",
    layout="wide",
)

# ----------------------------
# Estilo visual
# ----------------------------
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    .hero {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #0b1f33 0%, #123f59 60%, #176b72 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 {color: white; margin-bottom: .25rem;}
    .hero p {color: #e0f2f1; margin-bottom: 0;}
    .small-note {font-size: .88rem; color: #64748b;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🧪 Laboratório Virtual de Cromatografia Gasosa</h1>
      <p>Explore a separação de componentes, os tempos de retenção e a resolução do cromatograma.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Modelo didático: os parâmetros são simplificados para demonstrar tendências. "
    "Não substitui o método validado, os dados experimentais nem o modelo de um fabricante."
)

# ----------------------------
# Controles
# ----------------------------
st.sidebar.header("⚙️ Condições do experimento")
mixture = st.sidebar.selectbox(
    "Mistura de exemplo",
    ["Hidrocarbonetos leves", "Mistura com composto de retenção forte", "Separação difícil"],
)
temperature = st.sidebar.slider("Temperatura da coluna (°C)", 40, 180, 90, 5)
flow = st.sidebar.slider("Vazão relativa do gás de arraste", 0.5, 2.0, 1.0, 0.1)
selectivity = st.sidebar.slider("Seletividade didática da coluna", 0.6, 1.8, 1.0, 0.1)
efficiency = st.sidebar.slider("Eficiência da coluna (pratos teóricos relativos)", 0.5, 2.0, 1.0, 0.1)
noise = st.sidebar.slider("Ruído simulado", 0.0, 8.0, 1.0, 0.5)
show_components = st.sidebar.checkbox("Mostrar picos individuais", value=True)

# Tempos-base apenas para o modelo didático.
mixtures = {
    "Hidrocarbonetos leves": {
        "names": ["CH₄ (metano)", "C₂H₆ (etano)", "C₃H₈ (propano)", "n-C₄H₁₀ (n-butano)"],
        "base": np.array([0.85, 1.45, 2.35, 3.45]),
        "amps": np.array([0.75, 0.68, 0.62, 0.55]),
        "colors": ["#00A6A6", "#3478F6", "#E69F00", "#CC79A7"],
    },
    "Mistura com composto de retenção forte": {
        "names": ["CH₄ (metano)", "C₂H₆ (etano)", "C₃H₈ (propano)", "Componente X"],
        "base": np.array([0.85, 1.45, 2.35, 4.55]),
        "amps": np.array([0.75, 0.68, 0.62, 0.48]),
        "colors": ["#00A6A6", "#3478F6", "#E69F00", "#CC79A7"],
    },
    "Separação difícil": {
        "names": ["Componente A", "Componente B", "Componente C", "Componente D"],
        "base": np.array([1.20, 1.48, 2.35, 2.62]),
        "amps": np.array([0.72, 0.68, 0.62, 0.58]),
        "colors": ["#00A6A6", "#3478F6", "#E69F00", "#CC79A7"],
    },
}
mix = mixtures[mixture]

# Temperatura maior tende a reduzir retenção no exemplo; vazão maior reduz tempo observado.
temp_factor = np.exp(-0.006 * (temperature - 90))
flow_factor = 1.0 / flow
retention_times = mix["base"] * temp_factor * flow_factor

# A seletividade afasta os picos em torno do centro da mistura, como aproximação didática.
center = float(np.mean(retention_times))
adjusted_rt = center + (retention_times - center) * selectivity

# Largura didática: menor eficiência relativa => picos mais largos.
widths = 0.075 * (1.0 / np.sqrt(efficiency)) * (1.0 + 0.002 * abs(90 - temperature))
amps = mix["amps"]

t_end = max(6.0, float(np.max(adjusted_rt) + 1.1))
t = np.linspace(0, t_end, 2200)
rng = np.random.default_rng(7)
individual = []
total = np.zeros_like(t)
for rt, amp, color, name in zip(adjusted_rt, amps, mix["colors"], mix["names"]):
    peak = amp * np.exp(-0.5 * ((t - rt) / widths) ** 2)
    individual.append((peak, color, name, rt))
    total += peak
observed = total + rng.normal(0, noise / 100.0, size=t.size)
observed = np.clip(observed, 0, None)

# ----------------------------
# Cromatograma
# ----------------------------
fig = go.Figure()
if show_components:
    for peak, color, name, rt in individual:
        fig.add_trace(
            go.Scatter(
                x=t, y=peak, mode="lines", name=name,
                line=dict(color=color, width=1.5, dash="dot"),
                opacity=0.85,
                hovertemplate=f"{name}<br>Tempo: %{{x:.3f}} min<br>Intensidade: %{{y:.3f}}<extra></extra>",
            )
        )
fig.add_trace(
    go.Scatter(
        x=t, y=observed, mode="lines", name="Sinal total simulado",
        line=dict(color="#E4572E", width=2.5),
        hovertemplate="Tempo: %{x:.3f} min<br>Sinal: %{y:.3f}<extra></extra>",
    )
)
for i, (rt, name) in enumerate(zip(adjusted_rt, mix["names"])):
    fig.add_vline(x=float(rt), line_width=1, line_dash="dash", line_color="gray", opacity=0.55)
fig.update_layout(
    title="Cromatograma simulado",
    xaxis_title="Tempo (min, escala didática)",
    yaxis_title="Resposta relativa do detector",
    template="plotly_white",
    height=470,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(l=20, r=20, t=80, b=20),
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Indicadores e tabela
# ----------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Componentes modelados", len(mix["names"]))
c2.metric("Temperatura", f"{temperature} °C")
c3.metric("Vazão relativa", f"{flow:.1f}×")

# Resolução aproximada entre picos vizinhos:
# Rs = 2 (tR2-tR1)/(w1+w2), com largura aproximada à base = 4 sigma.
rows = []
for i, (name, rt, amp) in enumerate(zip(mix["names"], adjusted_rt, amps)):
    rows.append({
        "Componente (modelo)": name,
        "Tempo de retenção (min)": round(float(rt), 3),
        "Altura relativa": round(float(amp), 3),
        "Largura σ (min)": round(float(widths), 3),
    })
table = pd.DataFrame(rows)
st.subheader("Resultados do experimento")
st.dataframe(table, use_container_width=True, hide_index=True)

resolutions = []
for i in range(len(adjusted_rt) - 1):
    delta = adjusted_rt[i + 1] - adjusted_rt[i]
    base_width_1 = 4 * widths
    base_width_2 = 4 * widths
    rs = 2 * delta / (base_width_1 + base_width_2)
    resolutions.append((mix["names"][i], mix["names"][i + 1], float(rs)))

if resolutions:
    res_df = pd.DataFrame(
        resolutions,
        columns=["Par de picos vizinhos", "Componente seguinte", "Resolução aproximada"],
    )
    # Corrige o primeiro campo para uma representação mais legível.
    res_df["Par de picos vizinhos"] = [
        f"{a} → {b}" for a, b, _ in resolutions
    ]
    res_df = res_df.drop(columns=["Componente seguinte"])
    st.dataframe(res_df, use_container_width=True, hide_index=True)
    minimum_rs = min(r[2] for r in resolutions)
    if minimum_rs >= 1.5:
        st.success(f"Neste modelo, o menor valor de resolução é {minimum_rs:.2f}: separação visualmente boa.")
    elif minimum_rs >= 1.0:
        st.info(f"Neste modelo, o menor valor de resolução é {minimum_rs:.2f}: há risco de sobreposição parcial.")
    else:
        st.error(f"Neste modelo, o menor valor de resolução é {minimum_rs:.2f}: pelo menos um par apresenta sobreposição importante.")

# ----------------------------
# Explicação guiada
# ----------------------------
st.subheader("🧠 Explore como um engenheiro")
with st.expander("1. O que acontece quando aumento a temperatura?"):
    st.write(
        "No modelo, aumentar a temperatura reduz os tempos de retenção. "
        "Em cromatografia gasosa, a temperatura influencia o equilíbrio de partição e a volatilidade; "
        "o efeito real depende do composto, da fase estacionária e do programa de temperatura."
    )
with st.expander("2. O que acontece quando aumento a vazão?"):
    st.write(
        "A simulação reduz os tempos observados quando a vazão relativa aumenta. "
        "Na prática, a relação entre vazão, eficiência e resolução não é simplesmente inversa: "
        "a velocidade linear ótima depende da coluna, do gás de arraste e das condições de operação."
    )
with st.expander("3. O que significa resolução?"):
    st.write(
        "A resolução expressa o grau de separação entre dois picos. Aqui é estimada usando larguras "
        "simplificadas derivadas do desvio-padrão dos picos gaussianos. Não é uma integração validada "
        "de dados instrumentais e não deve ser usada para liberar resultados de processo."
    )
with st.expander("4. Por que massa molecular não determina sozinha a retenção?"):
    st.write(
        "A massa molecular pode acompanhar tendências de volatilidade em séries homólogas, como alcanos, "
        "mas não determina sozinha o tempo de retenção. O ponto de ebulição, as interações com a fase "
        "estacionária, a temperatura e as condições de fluxo também são relevantes."
    )

st.caption(
    "Analyzers Experts • Protótipo didático. Os valores, picos e relações são simulados; "
    "não representam dados de um cromatógrafo comercial específico."
)

csv = table.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Baixar tabela de resultados (CSV)",
    data=csv,
    file_name="analyzers_experts_resultados_cromatografia.csv",
    mime="text/csv",
)
