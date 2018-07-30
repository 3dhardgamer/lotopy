import requests
import zipfile
import io
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

df_loto = pd.read_html('D_LOTFAC.HTM')[0]
df_loto = pd.DataFrame(df_loto)
header = df_loto.iloc[0]
df_loto = df_loto[1:]
df_loto.rename(columns = header, inplace = True)
df_loto.drop(['Cidade', 'UF'], axis = 1, inplace = True)
df_loto.dropna(inplace = True)
df_loto.set_index('Concurso', inplace = True)

jogo1 = np.array(['01', '03', '04', '06', '09', '10', '11', '12', '14', '17', '18', '20', '21', '23', '25'])
jogo2 = np.array(['02', '04', '05', '05', '10', '11', '13', '14', '15', '16', '19', '21', '22', '23', '24'])

bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']

sorteio = df_loto[bolas]

numbers = np.array(sorteio.iloc[-1].values)
count1 = 0
count2 = 0

for num in numbers:
    if num in jogo1:
        count1 += 1
    if num in jogo2:
        count2 += 1

print(count1, count2)
