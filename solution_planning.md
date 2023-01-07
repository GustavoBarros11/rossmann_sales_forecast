## Problema de Negócio
- **Empresa**: Rossmann
- **Modelo de Negócio**: Empresa dona de uma rede de Farmácias espalhadas por 7 países na Europa. Seu faturamento vem das vendas geradas por cada uma das lojas.
- **Qual o desafio**: 
    O CFO da empresa fez uma reunião com todos Gerentes de Loja e pediu para que cada um deles trouxesse uma previsão diária das próximas 6 semanas de vendas.
    Depois desa reunião, todos os Gerentes entraram em contato com você, requisitando uma previsão de vendas de suas lojas.

## Planejamento da Solução
### 1) Identificação da causa raíz
- Motivação: Qual o contexto?
    - Durante uma reunião de resultados mensais, o CFO requisitou a cada um dos Gerentes de Loja que entreguem um relatório contendo a previsão de vendas para as próximas 6 semanas.
- Qual é a causa raiz do problema?
    - O CFO quer liberar uma quantia para investir na reforma das lojas, porém ele quer fazer um investimento consciente e para isso ele precisa ter uma noção de quanto será o faturamento futuro de cada uma delas para balancear o valor investido, para mais ou para menos.
    - Investimento em reforma das Lojas.
- Quem é o stakeholder?
    - O CFO
### 2) Definir um escopo fechado para uma pergunta aberta
- **Quanto será o valor das vendas de cada loja nas próximas 6 semanas?**
    - R: Criar de um modelo de machine learning de regressão que faça a predição do valor futuro de vendas para cada Loja (farmácia), em um período de 6 semanas.
    <br><span style="color:gray">Produto | Tipo | Localidade | Atributo</span>

### 3) Quebrar o problema definido em tarefas menores
- **Criar de um modelo de machine learning de regressão que faça a predição do valor futuro de vendas para cada farmácia, em um período de 6 semanas.**
    - SAÍDA (o que irei entregar):
        + Vendas diárias em R$, nas próximas 6 semanas
        + Problema de Predição (Regressão)
        + Time Series, Regressão Linear e Redes Neurais
        + Predições acessadas via app de mensagens no celular
    - PROCESSO:
        - Ciclo 1:
            1. Download dos dados no Kaggle
            2. Entender o problema de negócio
            3. Construir dicionário dos dados
            3. Gerar hipóteses a serem validadas na etapa de análise exploratória
            4. Limpeza dos dados
            5. Descrição dos dados (estastísticas descritivas)
            6. Feature Engineering inicial
            8. Análise exploratória dos dados
                - Análise univariada, bivariada e multivariada
            9. Preparação dos dados
            10. Seleção de atributos
            11. Definição do modelo baseline
            12. ,
            13. Avaliação das performances dos modelos nos dataset de validação e teste
    - ENTRADA DE DADOS:
        + [Download dos dados na página da competição no kaggle](https://www.kaggle.com/c/rossmann-store-sales)
### 4) Executar com uma mentalidade cíclica
1. Eu preciso passar por todas as tarefas o mais rápido possível para:
    1. Identificar bloqueios
    2. Identificar impeditivos que possam desvalidar o projeto
    3. Entregar valor para empresa rapidamente
2. Fazer escolhas simples (Keep it Simple)

### 5) Próximos passos:
- Executar a solução de forma cíclica
- Fazer a coleta dos dados
- Criar arquivo REAME.md
- Fazer gerenciamento do repositório Git