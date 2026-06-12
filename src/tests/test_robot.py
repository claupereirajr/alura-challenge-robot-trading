import unittest
import pandas as pd
from src.main import limpeza_dados, tomar_decisao
import src.main as main_module

class TestTradingRobot(unittest.TestCase):

    def setUp(self):
        # Resetar as variáveis globais do módulo main antes de cada teste
        main_module.df_bitcoin = pd.DataFrame()
        main_module.preco_atual = 0.0
        main_module.tendencia = ""
        main_module.media_preco = 0.0
        main_module.decisao = ""

    def test_limpeza_dados_removes_duplicates_nulls_and_outliers(self):
        # Criar dataframe simulado contendo:
        # - Registro duplicado (Timestamp 1000)
        # - Valor nulo (Timestamp 2000)
        # - Outlier extremo (Preço 1.000.000)
        data = {
            "Timestamp": [1000, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
            "Price": [60000.0, 60000.0, None, 61000.0, 59000.0, 60500.0, 59500.0, 60100.0, 1000000.0]
        }
        main_module.df_bitcoin = pd.DataFrame(data)
        
        limpeza_dados()
        
        # O duplicado deve ser removido, o nulo também, e o outlier filtrado por IQR.
        # Sobram os preços: 60000, 61000, 59000, 60500, 59500, 60100 (6 registros)
        self.assertEqual(len(main_module.df_bitcoin), 6)
        self.assertNotIn(1000000.0, main_module.df_bitcoin["Price"].values)
        
        # Média calculada esperada: (60000 + 61000 + 59000 + 60500 + 59500 + 60100) / 6 = 60016.67
        self.assertAlmostEqual(main_module.media_preco, 60016.666666666664, places=2)

    def test_tomar_decisao_buy_condition(self):
        # Compra: Preço atual < média e Tendência == "alta"
        main_module.preco_atual = 55000.0
        main_module.media_preco = 60000.0
        main_module.tendencia = "alta"
        
        tomar_decisao()
        
        self.assertEqual(main_module.decisao, "Comprar")

    def test_tomar_decisao_sell_condition(self):
        # Venda: Preço atual >= média e Tendência == "baixa"
        main_module.preco_atual = 62000.0
        main_module.media_preco = 60000.0
        main_module.tendencia = "baixa"
        
        tomar_decisao()
        
        self.assertEqual(main_module.decisao, "Vender")

    def test_tomar_decisao_hold_condition(self):
        # Manter: Preço atual >= média mas Tendência == "alta"
        main_module.preco_atual = 62000.0
        main_module.media_preco = 60000.0
        main_module.tendencia = "alta"
        
        tomar_decisao()
        
        self.assertEqual(main_module.decisao, "")

if __name__ == '__main__':
    unittest.main()
