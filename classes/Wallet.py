import numpy as np
import pandas as pd
import download_data
from datetime import datetime
# tutaj ustalam na podstawie jakiego kryterium ma być ustalana hierarchia między portfelami
comparison_metric = 'VX'
class Wallet:
    def __init__(self, shares, balance, data):
        self.shares = shares
        self.balance = balance
        self.statystyki = {'mean':np.nan, 'std_dev':np.nan}
        self.data = datetime.strptime(data, '%d-%m-%Y')
        self.no_shares = {}
        # wyliczanie liczby zakupionych stocków
        for key, value in self.shares.items():
            a = download_data.read_stock_data_from_csv(key, prices=True).reset_index()
            a['Date'] = pd.to_datetime(a['Date'])
            a = a.loc[a['Date'] <= self.data].set_index('Date')

            self.no_shares[key] = int((value*self.balance) // a.tail(1)['Close'].values[0])
        # wyliczanie statystyk

    def load_wallet_stock_data(self):
        """
        Za zadanie ma dla danego portfela wyplucie danych na których portfel został zbudowany, tj. stopy zwrotu
        na których podstawie został wybrany (czyli stopy zwrotu dla spółek znajdujących się w portfelu z okresu sprzed budowy
        portfela inwestycyjnego)
        """
        wallet_returns = pd.DataFrame({})
        for key, value in self.shares.items():
            a = download_data.read_stock_data_from_csv(key).reset_index()
            a['index'] = pd.to_datetime(a['index'])
            a = a.loc[a['index'] <= self.data].set_index('index')['Close']
            wallet_returns = pd.concat([wallet_returns, a.rename(key)], axis=1)
        return wallet_returns

    def __str__(self):
        result = 'Udziały w spółkach: \n SPÓŁKA | UDZIAŁ | LICZBA AKCJI | KWOTA WYDANA \n'
        for key, value in self.shares.items():
            result+=f"{key} | {round(value*100, 2)}% |  {self.no_shares[key]}szt. | {round(self.balance*value, 2)} \n"
        result += '----------------------------------'
        return f"Portfel typu basic utworzony w dniu {self.data} z zainwestowaną kwotą {self.balance} złotych. "+result

    #overriding comparisons
    # overriding <
    def __lt__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev']/self.statystyki['mean'] < other.statystyki['std_dev']/other.statystyki['mean']
        else:
            raise ValueError

    # overriding <=
    def __le__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev']/self.statystyki['mean'] <= other.statystyki['std_dev']/other.statystyki['mean']
        else:
            raise ValueError

    # overriding ==
    def __eq__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev']/self.statystyki['mean'] == other.statystyki['std_dev']/other.statystyki['mean']
        else:
            raise ValueError

    # overriding !=
    def __ne__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev']/self.statystyki['mean'] != other.statystyki['std_dev']/other.statystyki['mean']
        else:
            raise ValueError

    # overriding >
    def __gt__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev'] / self.statystyki['mean'] > other.statystyki['std_dev'] / \
                   other.statystyki['mean']
        else:
            raise ValueError

    # overriding >=
    def __ge__(self, other):
        if comparison_metric == 'VX':
            return self.statystyki['std_dev'] / self.statystyki['mean'] >= other.statystyki['std_dev'] / \
                   other.statystyki['mean']
        else:
            raise ValueError
portfel_testowy = Wallet({'PKO':0.833333, 'SGN':0.2}, 20000, '22-08-2022')