import requests
import zipfile
import io
import pandas as pd
import numpy as np

# URL to zipfile where lotofacil runs can be found
url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'

# My lucky numbers :)
jogo1 = np.array(['01', '03', '04', '06', '09', '10', '11', '12', '14', '17', '18', '20', '21', '23', '25'])
jogo2 = np.array(['02', '04', '05', '05', '10', '11', '13', '14', '15', '16', '19', '21', '22', '23', '24'])

# Columns name with withdrawn numbers
bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']


def extract_page(url):
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()


def create_df():
    df = pd.read_html('D_LOTFAC.HTM')[0]
    df = pd.DataFrame(df)
    header = df.iloc[0]
    df = df[1:]
    df.rename(columns = header, inplace = True)
    df.drop(['Cidade', 'UF'], axis = 1, inplace = True)
    df.dropna(inplace = True)
    df.set_index('Concurso', inplace = True)

    return df

def select_cols(df, cols = bolas):
    return df[cols]

def count_numbers(df, jogo):
    count = 0
    numbers = np.array(df.iloc[-1].values)
    for num in numbers:
        if num in jogo:
            count += 1

    return count


extract_page(url)
df = create_df()
sorteio = select_cols(df, bolas)

concurso = sorteio.index[-1]
data = df['Data Sorteio'][-1]
print(concurso, data)

count1 = count_numbers(sorteio, jogo1)
count2 = count_numbers(sorteio, jogo2)
print(count1, count2)
