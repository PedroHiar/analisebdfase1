"""
frontend.py — Camada de Apresentação / View

Módulo "burro" de apresentação: não processa dados, apenas recebe
dicionários e DataFrames já prontos e os renderiza no terminal
(painel textual) e via matplotlib (gráficos).

Hierarquia: MENOR DOMINÂNCIA — depende de dados já tratados.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Union


def imprimir_painel_estatistico(
    titulo: str,
    indicadores: Dict[str, Union[float, List[float]]],
) -> None:
    """Imprime um painel formatado de indicadores estatísticos no terminal.

    O painel apresenta as Medidas de Posição (Média, Mediana, Moda)
    e as Medidas de Dispersão (Desvio Padrão, Coeficiente de Variação)
    de forma organizada e visualmente clara.

    Args:
        titulo: Título descritivo do painel (ex.: "Expectativa de Vida").
        indicadores: Dicionário retornado por estatistica.gerar_painel_estatistico().
    """
    largura = 56
    separador = "=" * largura

    print(f"\n+{separador}+")
    print(f"|{'PAINEL ESTATISTICO':^{largura}}|")
    print(f"|{titulo:^{largura}}|")
    print(f"+{separador}+")

    print(f"|{'':^{largura}}|")
    print(f"|{'-- Medidas de Posicao --':^{largura}}|")
    print(f"|  {'Media:':<28}{indicadores['media']:>22.4f}  |")
    print(f"|  {'Mediana:':<28}{indicadores['mediana']:>22.4f}  |")

    modas_str = ", ".join(f"{m:.2f}" for m in indicadores["moda"])
    print(f"|  {'Moda:':<28}{modas_str:>22}  |")

    print(f"|{'':^{largura}}|")
    print(f"|{'-- Medidas de Dispersao --':^{largura}}|")
    print(f"|  {'Desvio Padrao:':<28}{indicadores['desvio_padrao']:>22.4f}  |")
    print(f"|  {'Coef. de Variacao (CV%):':<28}{indicadores['coeficiente_variacao']:>22.4f}  |")

    print(f"+{separador}+\n")


def renderizar_graficos(
    df_life_exp: pd.DataFrame,
    df_pop_continente: pd.DataFrame,
) -> None:
    """Renderiza uma figura com dois subplots: gráfico de linha e gráfico de pizza.

    Subplot 1 (esquerda): Evolução da Expectativa de Vida média global ao
    longo dos anos — gráfico de linha.

    Subplot 2 (direita): Distribuição da população mundial por continente
    no ano de 2007 — gráfico de pizza.

    Args:
        df_life_exp: DataFrame com colunas ['year', 'lifeExp'].
        df_pop_continente: DataFrame com colunas ['continent', 'pop'].
    """
    # ---- Configuração geral da figura ----
    fig, (ax_linha, ax_pizza) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(16, 7),
    )
    fig.suptitle(
        "Análise de Dados — Gapminder",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )

    # ---- Subplot 1: Gráfico de Linha ----
    ax_linha.plot(
        df_life_exp["year"],
        df_life_exp["lifeExp"],
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#2196F3",
        markerfacecolor="#0D47A1",
        markeredgecolor="white",
        markeredgewidth=1.5,
    )
    ax_linha.set_title("Evolução da Expectativa de Vida Média Global", fontsize=13, pad=12)
    ax_linha.set_xlabel("Ano", fontsize=11)
    ax_linha.set_ylabel("Expectativa de Vida (anos)", fontsize=11)
    ax_linha.grid(True, linestyle="--", alpha=0.5)
    ax_linha.set_facecolor("#F5F5F5")

    # Anotar cada ponto com seu valor
    for _, row in df_life_exp.iterrows():
        ax_linha.annotate(
            f"{row['lifeExp']:.1f}",
            xy=(row["year"], row["lifeExp"]),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=8,
            color="#333333",
        )

    # ---- Subplot 2: Gráfico de Pizza ----
    cores_pizza = ["#FF7043", "#66BB6A", "#42A5F5", "#AB47BC", "#FFA726"]
    explode = [0.04] * len(df_pop_continente)

    wedges, texts, autotexts = ax_pizza.pie(
        df_pop_continente["pop"],
        labels=df_pop_continente["continent"],
        autopct="%1.1f%%",
        startangle=140,
        colors=cores_pizza,
        explode=explode,
        textprops={"fontsize": 11},
        pctdistance=0.75,
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    ax_pizza.set_title("População por Continente — 2007", fontsize=13, pad=12)

    # ---- Layout final ----
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()
