import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

# URL pública do dataset Pima Indians Diabetes (espelho do Plotly)
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"

df = pd.read_csv(url)

# Limpar dados: valores 0 em Glucose e BMI geralmente indicam dados ausentes neste dataset
df_clean = df[(df['Glucose'] > 0) & (df['BMI'] > 0) & (df['Age'] > 0)].copy()

# Mapear outcome para rótulos legíveis
df_clean['Diagnóstico'] = df_clean['Outcome'].map({0: 'Não diabético', 1: 'Diabético'})

# Criar scatter plot interativo
fig = px.scatter(
    df_clean,
    x='Glucose',
    y='BMI',
    color='Diagnóstico',
    color_discrete_map={'Não diabético': '#1f77b4', 'Diabético': '#d62728'},
    title='Diagnóstico de Diabetes: Glicose vs IMC',
    labels={'Glucose': 'Nível de Glicose no Sangue (mg/dL)', 'BMI': 'Índice de Massa Corporal (IMC)'},
    opacity=0.7,
    width=800,
    height=600
)

fig.update_traces(
    hovertemplate='<b>Glicose:</b> %{x} mg/dL<br><b>IMC:</b> %{y}<extra></extra>'
)

fig.update_layout(
    legend_title_text='Resultado',
    template='plotly_white',
    margin=dict(l=60, r=40, t=60, b=60)
)

# Salvar como HTML self-contained
output_dir = Path(__file__).resolve().parents[1] / "assets" / "plots"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "diabetes_scatter.html"
pio.write_html(fig, file=str(output_path), full_html=True, include_plotlyjs='cdn')

print(f"Gráfico salvo em: {output_path}")
print(f"Pontos plotados: {len(df_clean)}")
