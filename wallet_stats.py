# moduł zawierający funkcje liczące statystyki dla obiektu Wallet
from classes.Wallet import *
import download_data
import pandas as pd
import numpy as np
def mean(portfel):
    shares = np.array(list(portfel.shares.values()))
    return np.matmul(portfel.load_wallet_stock_data().mean(), np.transpose(shares))

def variance(portfel):
    srednia_portfela = mean(portfel)
    return sum(np.square(portfel.load_wallet_stock_data().mean() - srednia_portfela))

def kurtosis(portfel):
    srednia_portfela = mean(portfel)
    std_dev = np.sqrt(variance(portfel))
    M4 = sum(np.power((portfel.load_wallet_stock_data().mean() - srednia_portfela), 4))/(std_dev**4*len(portfel.shares.values()))
    return M4 -3

def skewness(portfel):
    srednia_portfela = mean(portfel)
    std_dev = np.sqrt(variance(portfel))
    M3 = sum(np.power((portfel.load_wallet_stock_data().mean() - srednia_portfela), 3)) / (
                std_dev ** 3 * len(portfel.shares.values()))
    return M3
print(skewness(portfel_testowy))