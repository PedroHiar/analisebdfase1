"""
dados.py — Camada de Dados / Repositório

Módulo responsável pela extração e preparação dos dados a partir
da base pública do Gapminder. Utiliza pandas para leitura e
transformação dos DataFrames.

Hierarquia: INTERMEDIÁRIA — depende apenas de bibliotecas de dados,
nunca de módulos de apresentação ou lógica de negócio.
"""

import pandas as pd
from typing import List

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
GAPMINDER_URL: str = (
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)


def carregar_dados_brutos(url: str = GAPMINDER_URL) -> pd.DataFrame:
    """Carrega o dataset completo do Gapminder a partir de uma URL.

    Realiza a leitura do arquivo CSV remoto e retorna o DataFrame
    bruto, sem nenhuma transformação.

    Args:
        url: Endereço HTTP/HTTPS do arquivo CSV.

    Returns:
        DataFrame com os dados brutos do Gapminder.

    Raises:
        ConnectionError: Se não for possível acessar a URL.
        RuntimeError: Para qualquer erro inesperado durante a leitura.
    """
    try:
        df = pd.read_csv(url)
        print(f"[dados] [OK] Dataset carregado com sucesso - {len(df)} registros.")
        return df
    except Exception as erro:
        if "urlopen" in str(erro).lower() or "connection" in str(erro).lower():
            raise ConnectionError(
                f"[dados] [ERRO] Falha de conexao ao acessar a URL:\n  {url}\n  Erro: {erro}"
            ) from erro
        raise RuntimeError(
            f"[dados] [ERRO] Erro inesperado ao carregar os dados:\n  {erro}"
        ) from erro


def extrair_lista_life_exp(df: pd.DataFrame) -> List[float]:
    """Extrai a coluna 'lifeExp' do DataFrame como uma lista Python.

    Útil para alimentar o módulo de estatísticas (funções puras que
    recebem listas, sem acoplamento com pandas).

    Args:
        df: DataFrame contendo a coluna 'lifeExp'.

    Returns:
        Lista de floats com todos os valores de expectativa de vida.
    """
    return df["lifeExp"].dropna().tolist()


def preparar_life_exp_por_ano(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara a média da expectativa de vida agrupada por ano.

    Gera o DataFrame necessário para o gráfico de linha
    (Evolução da Expectativa de Vida ao longo do tempo).

    Args:
        df: DataFrame bruto do Gapminder.

    Returns:
        DataFrame com colunas ['year', 'lifeExp'], onde 'lifeExp'
        representa a média global por ano.
    """
    agrupado = (
        df.groupby("year")["lifeExp"]
        .mean()
        .reset_index()
    )
    agrupado.columns = ["year", "lifeExp"]
    return agrupado


def preparar_populacao_por_continente(df: pd.DataFrame, ano: int = 2007) -> pd.DataFrame:
    """Prepara a soma populacional por continente para um ano específico.

    Gera o DataFrame necessário para o gráfico de pizza
    (População por Continente).

    Args:
        df: DataFrame bruto do Gapminder.
        ano: Ano de referência para o filtro (padrão: 2007).

    Returns:
        DataFrame com colunas ['continent', 'pop'], onde 'pop'
        é a soma da população de todos os países do continente.
    """
    filtrado = df[df["year"] == ano]
    agrupado = (
        filtrado.groupby("continent")["pop"]
        .sum()
        .reset_index()
    )
    agrupado.columns = ["continent", "pop"]
    return agrupado
