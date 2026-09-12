# Análise Estatística — Gapminder (Fase 1)

Análise estatística descritiva do dataset Gapminder com Python puro. Calcula média, mediana, moda, desvio padrão e coeficiente de variação da expectativa de vida (`lifeExp`). Arquitetura em camadas (dados → estatística → apresentação) com saída em terminal e gráficos via matplotlib.

## Estrutura

| Módulo | Responsabilidade |
|---|---|
| `dados.py` | Extração e preparação dos dados (CSV remoto via pandas) |
| `estatistica.py` | Funções estatísticas puras (sem dependências externas) |
| `frontend.py` | Apresentação: painel textual + gráficos (matplotlib) |
| `main.py` | Orquestrador — conecta as três camadas |

## Execução

```bash
pip install pandas matplotlib
python main.py
```
