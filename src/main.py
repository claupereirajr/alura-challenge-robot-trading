import time
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# Global variables (storing current state)
df_bitcoin = pd.DataFrame()
preco_atual = 0.0
tendencia = ""
media_preco = 0.0
decisao = ""

def importar_dados_historicos():
    """Fetches Bitcoin historical prices from CoinGecko API."""
    global df_bitcoin
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            prices = data.get("prices", [])
            df_bitcoin = pd.DataFrame(prices, columns=["Timestamp", "Price"])
            # Converter Timestamp para Datetime para melhor visualização
            df_bitcoin["Datetime"] = pd.to_datetime(df_bitcoin["Timestamp"], unit="ms")
            print(f"Importados com sucesso {len(df_bitcoin)} pontos de dados históricos.")
        else:
            print(f"Erro ao obter dados históricos. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao obter dados históricos: {e}")

def obter_dados_atual():
    """Scrapes current price and 24h trend from Yahoo Finance."""
    global preco_atual, tendencia
    url = "https://finance.yahoo.com/quote/BTC-USD/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Obter preco atual
            price_element = soup.find(attrs={"data-testid": "qsp-price"})
            if price_element:
                price_text = price_element.text.strip().replace(",", "")
                preco_atual = float(price_text)
            else:
                raise ValueError("Não foi possível encontrar o elemento do preço atual")
                
            # Obter variação / tendência
            change_element = soup.find(attrs={"data-testid": "qsp-price-change"})
            if change_element:
                change_text = change_element.text.strip()
                if change_text.startswith("+"):
                    tendencia = "alta"
                elif change_text.startswith("-"):
                    tendencia = "baixa"
                else:
                    change_val = float(change_text.replace(",", ""))
                    tendencia = "alta" if change_val >= 0 else "baixa"
            else:
                raise ValueError("Não foi possível encontrar o elemento da variação de preço")
                
            print(f"Dados obtidos - Preço atual: US$ {preco_atual:,.2f} | Tendência: {tendencia}")
        else:
            print(f"Erro ao obter dados atuais. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao raspar dados em tempo real: {e}")

def limpeza_dados():
    """Cleans df_bitcoin and calculates the mean price."""
    global df_bitcoin, media_preco
    if df_bitcoin.empty:
        print("DataFrame de dados históricos está vazio. Limpeza ignorada.")
        return
        
    try:
        before_count = len(df_bitcoin)
        
        # Remover duplicados e valores nulos
        df_bitcoin.drop_duplicates(subset=["Timestamp"], inplace=True)
        df_bitcoin.dropna(subset=["Price"], inplace=True)
        
        # Filtrar outliers usando IQR (Intervalo Interquartil)
        q1 = df_bitcoin["Price"].quantile(0.25)
        q3 = df_bitcoin["Price"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        df_bitcoin = df_bitcoin[(df_bitcoin["Price"] >= lower_bound) & (df_bitcoin["Price"] <= upper_bound)]
        
        # Calcular preço médio dos dados limpos
        media_preco = df_bitcoin["Price"].mean()
        after_count = len(df_bitcoin)
        print(f"Limpeza concluída: {before_count} -> {after_count} registros. Preço Médio: US$ {media_preco:,.2f}")
    except Exception as e:
        print(f"Erro ao limpar dados: {e}")

def tomar_decisao():
    """Makes a trade decision based on current price, trend, and mean price."""
    global preco_atual, tendencia, media_preco, decisao
    try:
        if preco_atual >= media_preco and tendencia == "baixa":
            decisao = "Vender"
        elif preco_atual < media_preco and tendencia == "alta":
            decisao = "Comprar"
        else:
            decisao = ""
            
        print(f"Decisão tomada: {decisao if decisao else 'Aguardar (Nenhuma ação)'}")
    except Exception as e:
        print(f"Erro ao tomar decisão: {e}")

def visualizacao():
    """Generates the plot of historical prices, average, and decision annotation."""
    global df_bitcoin, media_preco, decisao, preco_atual, tendencia
    if df_bitcoin.empty:
        print("DataFrame de dados históricos está vazio. Visualização ignorada.")
        return
        
    try:
        # Criar a figura
        plt.figure(figsize=(10, 6))
        
        # Plotar o preço histórico
        plt.plot(df_bitcoin["Datetime"], df_bitcoin["Price"], marker="o", color="#1f77b4", linewidth=2, label="Preço Histórico (USD)")
        
        # Linha do preço médio
        plt.axhline(y=media_preco, color="#d62728", linestyle="--", linewidth=1.5, label=f"Preço Médio (US$ {media_preco:,.2f})")
        
        # Ponto do preço atual (usando a data mais recente no histórico como referência de tempo para plotagem)
        last_date = df_bitcoin["Datetime"].iloc[-1]
        plt.scatter(last_date, preco_atual, color="#2ca02c" if tendencia == "alta" else "#ff7f0e", s=120, zorder=5, 
                    label=f"Preço Atual (US$ {preco_atual:,.2f})")
        
        # Título e labels
        plt.title("🤖 Evolução do Preço do Bitcoin & Tomada de Decisão", fontsize=14, pad=15)
        plt.xlabel("Data/Hora (UTC)", fontsize=11)
        plt.ylabel("Preço em USD", fontsize=11)
        plt.grid(True, linestyle=":", alpha=0.6)
        
        # Rotacionar datas para legibilidade
        plt.xticks(rotation=15)
        
        # Legenda
        plt.legend(loc="upper left")
        
        # Caixa de texto com a recomendação
        if decisao:
            color = "#2ca02c" if decisao == "Comprar" else "#d62728"
            plt.text(0.5, 0.88, f"RECOMENDAÇÃO: {decisao.upper()}", 
                     transform=plt.gca().transAxes, 
                     fontsize=14, color="white", weight="bold", ha="center",
                     bbox=dict(facecolor=color, alpha=0.9, edgecolor="none", boxstyle="round,pad=0.5"))
        else:
            plt.text(0.5, 0.88, "RECOMENDAÇÃO: AGUARDAR", 
                     transform=plt.gca().transAxes, 
                     fontsize=14, color="white", weight="bold", ha="center",
                     bbox=dict(facecolor="#7f7f7f", alpha=0.9, edgecolor="none", boxstyle="round,pad=0.5"))
            
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar o gráfico
        chart_path = "/home/claudineijr/seagate1TB/projects/ai/alura-challenge-robot-trading/src/bitcoin_chart.png"
        plt.savefig(chart_path)
        plt.close()
        print(f"Gráfico atualizado e salvo com sucesso em: {chart_path}")
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")

def main():
    """Main execution loop running every 5 minutes."""
    print("Iniciando o Robô de Negociação Bitcoin...")
    ciclo = 1
    while True:
        timestamp_atual = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n==================================================")
        print(f"🔄 Iniciando Ciclo {ciclo} às {timestamp_atual}")
        print(f"==================================================")
        
        try:
            importar_dados_historicos()
            obter_dados_atual()
            limpeza_dados()
            tomar_decisao()
            visualizacao()
        except Exception as e:
            print(f"❌ Erro crítico no ciclo {ciclo}: {e}")
            
        print(f"\n💤 Ciclo {ciclo} concluído. Aguardando 5 minutos (300s)...")
        ciclo += 1
        time.sleep(300)

if __name__ == "__main__":
    main()
