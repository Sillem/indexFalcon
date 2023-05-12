import download_data

if __name__ == '__main__':
    #download_data.download_stock_data('22-06-2022')
    print(download_data.read_stock_data_from_csv('XTB'))