from pandas_datareader.stooq import StooqDailyReader
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import os
def get_symbols():
    """
    Funckcja zwracająca listę symboli na których obecnie działa program (chce przeprowadzać wszystkie operacje). Dla
    porządku jeżeli chcemy zmienić listę symboli musimy użyć funkcji do modyfikacji tego pliku żeby zachować spójność
    działań i operacji. Jest to kluczowa funkcja.
    """

    with open('./config/symbols.txt', 'r') as file:
        return [x for x in file.read().split('\n') if x !='']

def download_stock_data(start_date, end_date=date.today(), frequency='d'):
    """
    PARAMETRY:
    symbole <- lista z symbolami na stooqa których dane chcemy pobrać,
    start_date <- data od której chcemy dane,
    end_date <- data do której chcemy dane (jeżeli nie podane to weźmie datę dzisiejszą),
    frequency <- 'd' - dzienne, 'w' - tygodniowe, 'm' - miesięczne

    Pobiera dane spółek do plików .csv z podanego horyzontu czasowego i o podanej częstotliwości do plików csv
    w folderze stock_info.
    """
    symbole = get_symbols()
    start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
    print(f"Trwa pobieranie danych od dnia {start_date} do dnia {end_date} o interwale '{frequency}' dla spółek:", *symbole)
    if not isinstance(end_date, date):
        end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
    for stock in symbole:
        reader = StooqDailyReader(f"{stock}.PL", start=start_date, end=end_date + timedelta(1))
        reader.freq = frequency
        #tutaj zabezpieczenie jak odrzuca serwer
        while True:
            try:
                stock_data = reader.read()
                break
            except:
                time.sleep(5)
                continue
        reader.close()
        if stock_data.shape[0] > 0:
            stock_data.to_csv(f'./stock_info/{stock}.csv')
            print(f"Zaktualizowano dane dla spółki {stock}")
        else:
            print(f"Nie udało się zaktualizować danych dla spółki {stock}")

    return

def read_stock_data_from_csv(stock, prices=False):
    raw_data = pd.read_csv(f"{os.path.dirname(__file__)}/stock_info/{stock}.csv").set_index('Date').iloc[::-1]
    if prices:
        return raw_data
    else:
        returns = pd.DataFrame({})
        for row in range(1, raw_data.shape[0]):
            log_return = (raw_data.iloc[row, :]/raw_data.iloc[row-1, :]).apply(lambda x: np.log(x))
            log_return = log_return._set_name(raw_data.index[row])
            returns = pd.concat([returns, log_return], axis=1)
        return returns.transpose()


