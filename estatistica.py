"""
estatistica.py — Camada Core / Lógica de Negócio

Módulo de funções estatísticas puras. Não possui dependência de
bibliotecas externas nem conhecimento sobre a origem dos dados.
Recebe apenas listas de números e retorna os resultados calculados.

Hierarquia: MAIOR DOMINÂNCIA — totalmente independente.
"""

from typing import List, Dict, Union
from collections import Counter
import math


def calcular_media(valores: List[float]) -> float:
    """Calcula a média aritmética de uma lista de valores.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Média aritmética dos valores.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")
    return sum(valores) / len(valores)


def calcular_mediana(valores: List[float]) -> float:
    """Calcula a mediana de uma lista de valores.

    A mediana é o valor central quando os dados estão ordenados.
    Para listas de tamanho par, retorna a média dos dois valores centrais.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Mediana dos valores.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    ordenados = sorted(valores)
    n = len(ordenados)
    meio = n // 2

    if n % 2 == 0:
        return (ordenados[meio - 1] + ordenados[meio]) / 2
    return ordenados[meio]


def calcular_moda(valores: List[float]) -> List[float]:
    """Calcula a moda (valor mais frequente) de uma lista de valores.

    Pode retornar múltiplos valores em caso de distribuição multimodal.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Lista contendo o(s) valor(es) mais frequente(s).

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    contagem = Counter(valores)
    frequencia_maxima = max(contagem.values())
    modas = [valor for valor, freq in contagem.items() if freq == frequencia_maxima]
    return sorted(modas)


def calcular_desvio_padrao(valores: List[float]) -> float:
    """Calcula o desvio padrão populacional de uma lista de valores.

    Utiliza a fórmula do desvio padrão populacional (σ), ou seja,
    divide pela quantidade total de elementos N.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Desvio padrão populacional dos valores.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    media = calcular_media(valores)
    soma_quadrados = sum((x - media) ** 2 for x in valores)
    return math.sqrt(soma_quadrados / len(valores))


def calcular_coeficiente_variacao(valores: List[float]) -> float:
    """Calcula o Coeficiente de Variação (CV%) de uma lista de valores.

    O CV expressa o desvio padrão como percentual da média, permitindo
    comparar a dispersão entre conjuntos de dados de escalas diferentes.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Coeficiente de Variação em percentual (%).

    Raises:
        ValueError: Se a lista estiver vazia ou se a média for zero.
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    media = calcular_media(valores)

    if media == 0:
        raise ValueError("O Coeficiente de Variação é indefinido quando a média é zero.")

    desvio = calcular_desvio_padrao(valores)
    return (desvio / abs(media)) * 100


def gerar_painel_estatistico(valores: List[float]) -> Dict[str, Union[float, List[float]]]:
    """Gera um dicionário completo com todas as medidas estatísticas.

    Consolida Medidas de Posição e de Dispersão em um único retorno
    para facilitar a exibição na camada de apresentação.

    Args:
        valores: Lista de números (int ou float).

    Returns:
        Dicionário com as chaves:
            - media (float)
            - mediana (float)
            - moda (List[float])
            - desvio_padrao (float)
            - coeficiente_variacao (float)
    """
    return {
        "media": calcular_media(valores),
        "mediana": calcular_mediana(valores),
        "moda": calcular_moda(valores),
        "desvio_padrao": calcular_desvio_padrao(valores),
        "coeficiente_variacao": calcular_coeficiente_variacao(valores),
    }
