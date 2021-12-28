import pandas as pd

def make_dataframe():
    data_list = []
    for i in range(330000, 350000):
        url_str = 'https://www.melon.com/song/detail.htm?songId='+ str(i)
        data_list.append((url_str, '', '', ''))

    data_df = pd.DataFrame(data_list, columns=['link', 'singer', 'title', 'emotional words'])
    return data_df

make_dataframe().to_excel('./dataset.xlsx', header=True)
