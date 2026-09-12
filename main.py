"""
main.py — Orquestrador / Controller

Ponto de entrada da aplicação. Importa os três módulos (dados,
estatistica, frontend) e orquestra o fluxo completo:

    1. Extrai os dados brutos via camada de dados.
    2. Prepara as transformações necessárias (DataFrames por ano/continente).
    3. Envia os valores puros para o módulo de estatísticas.
    4. Encaminha os resultados e DataFrames para a camada de apresentação.

Hierarquia: CONTROLLER — conhece todos os módulos, mas não contém
lógica de negócio nem de apresentação.
"""

import dados
import estatistica
import frontend


def executar() -> None:
    """Fluxo principal da aplicação.

    Orquestra as etapas de extração, processamento estatístico
    e apresentação dos resultados de forma sequencial.
    """

    # ------------------------------------------------------------------
    # 1. CAMADA DE DADOS — Extração e Preparação
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  INICIANDO ANALISE DE DADOS - GAPMINDER")
    print("=" * 60)

    try:
        df_bruto = dados.carregar_dados_brutos()
    except (ConnectionError, RuntimeError) as erro:
        print(f"\n[AVISO] Erro fatal ao carregar os dados:\n   {erro}")
        print("   Verifique sua conexao com a internet e tente novamente.")
        return

    # Preparar DataFrames para os gráficos
    df_life_exp_por_ano = dados.preparar_life_exp_por_ano(df_bruto)
    df_pop_continente = dados.preparar_populacao_por_continente(df_bruto, ano=2007)

    # Extrair lista pura de expectativa de vida (para funções estatísticas)
    lista_life_exp = dados.extrair_lista_life_exp(df_bruto)

    # ------------------------------------------------------------------
    # 2. CAMADA CORE — Cálculos Estatísticos
    # ------------------------------------------------------------------
    indicadores = estatistica.gerar_painel_estatistico(lista_life_exp)

    # ------------------------------------------------------------------
    # 3. CAMADA DE APRESENTAÇÃO — Exibição dos Resultados
    # ------------------------------------------------------------------

    # 3a. Painel de indicadores no terminal
    frontend.imprimir_painel_estatistico(
        titulo="Expectativa de Vida (lifeExp) — Todos os Registros",
        indicadores=indicadores,
    )

    # 3b. Gráficos (linha + pizza)
    frontend.renderizar_graficos(
        df_life_exp=df_life_exp_por_ano,
        df_pop_continente=df_pop_continente,
    )

    print("=" * 60)
    print("  ANALISE CONCLUIDA COM SUCESSO [OK]")
    print("=" * 60)


# ----------------------------------------------------------------------
# Ponto de entrada
# ----------------------------------------------------------------------
if __name__ == "__main__":
    executar()
