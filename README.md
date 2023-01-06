# **Rossmann Sales Forecast**
![jpg](img/rossmann_logo.png)

Este projeto foi orientado pela [Comunidade DS](), utilizando os dados disponíveis no [Kaggle]() da Rede de Lojas Rossmann.

**Produto final:**
- [Dashboard](): Análise Exploratória de Dados
- [BotTelegram](): Previsão de Vendas com Aprendizado de Máquina (Machine Learning)

# 1. Entendendo o Problema de Negócio
> O CFO da empresa fez uma reunião com todos Gerentes de Loja e pediu para que cada um deles trouxesse uma previsão diária das próximas 6 semanas de vendas. Depois desa reunião, todos os Gerentes entraram em contato com você, requisitando uma previsão de vendas de suas lojas.



# Dicionário dos Dados
Variable | Description
--- | ---
`Id` | An Id that represents a (Store, Date) duple within the test set
`Store` | A unique Id for each store
`DayOfWeek` | Day of week of the sale
`Date` | Date of the sale (daily)
`Sales` | The turnover for any given day (this is what you are predicting)
`Customers` | The number of customers on a given day
`Open` | An indicator for whether the store was open: 0 = closed, 1 = open
`Promo` | Indicates whether a store is running a promo on that day
`StateHoliday` | Indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None
`SchoolHoliday` | Indicates if the (Store, Date) was affected by the closure of public schools
`StoreType` | Differentiates between 4 different store models: a, b, c, d
`Assortment` | Describes an assortment level: a = basic, b = extra, c = extended
`CompetitionDistance` | Distance in meters to the nearest competitor store
`CompetitionOpenSinceMonth` | Gives the approximate month of the time the nearest competitor was opened
`CompetitionOpenSinceYear` | Gives the approximate year of the time the nearest competitor was opened
`Promo2` | Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
`Promo2SinceWeek` | Describes the calendar week when the store started participating in Promo2
`Promo2SinceYear` | Describes the year when the store started participating in Promo2
`PromoInterval` | Describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store