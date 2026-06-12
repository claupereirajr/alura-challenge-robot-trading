# 🤖 Desafio Alura - Robô de Negociação

## 📜 Requisitos

- **Configuração do Ambiente:** Para começar, você pode usar um ambiente virtual como o Google Colaboratory ou, se preferir, seu editor Python favorito. Certifique-se de ter o Python 3.x instalado em seu computador. Você também precisará instalar algumas bibliotecas Python essenciais para este projeto, como Pandas, NumPy, Matplotlib, etc.

- **Aquisição de Dados:** Você precisará acessar uma API que forneça dados históricos de preços do Bitcoin em formato JSON. Além disso, você precisará realizar web scraping em um site de notícias para obter o preço atual e alguns indicadores de tendência do Bitcoin.

- **Limpeza de Dados:** Depois de obter os dados históricos, você precisará carregá-los em um DataFrame do Pandas para manipulá-los e analisá-los. Você precisará identificar e remover outliers, bem como tratar quaisquer valores nulos ou duplicados no banco de dados. Finalmente, com os dados limpos, calcule o preço médio do Bitcoin.

- **Tomada de Decisão:** Depois de obter o preço médio, compare-o com o preço atual e a tendência do Bitcoin, que você obteve anteriormente por meio de web scraping. Se o preço atual for maior ou igual à média e a tendência for de baixa, você deve vender. No entanto, se o preço atual for menor que a média e a tendência for de alta, você deve comprar.

- **Visualização:** Use a biblioteca Matplotlib para criar um gráfico mostrando a evolução do preço do Bitcoin durante o período selecionado e uma linha reta passando pelo preço médio. Por fim, exiba uma mensagem no gráfico indicando "Vender", "Comprar" ou "" dependendo da decisão do algoritmo.

- **Automação:** Finalmente, agora que você tem o algoritmo de decisão, é hora de automatizar o processo. Use a biblioteca "time" do Python para executar o algoritmo de decisão a cada 5 minutos e atualizar o gráfico.