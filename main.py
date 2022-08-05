import os
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ.get('DB_URI'))

url_fii_resultado = "https://www.fundamentus.com.br/fii_resultado.php"
url_resultado = "https://www.fundamentus.com.br/resultado.php"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
data = date.today().strftime('%Y-%m-%d')
created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

app = FastAPI()

@app.get("/")
def fundamentus():
    scrap(url_fii_resultado)
    scrap(url_resultado)
    return {"message":"cadastrado com sucesso"}

def scrap(url):
    print(url)
    nome = url.split('/')
    nome = nome[-1].split('.')
    nome = nome[0]
    print(nome)
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        print('deu')
        df = pd.read_html(req.text)[0]
        df = df.apply(lambda x: x.astype(str).str.replace('.', ''))
        df = df.apply(lambda x: x.astype(str).str.replace(',', '.'))
        df = df.apply(lambda x: x.astype(str).str.replace('%', ''))
        df['created_at'] = created_at
        # df.columns = df.columns.str.replace(['.'], '')
        # df.columns = df.columns.str.replace([','], '.')
        # df.columns = df.columns.str.replace(['%'], '')
        print(df)
        # df[0].replace(['/'], '_')
        # df[0].columns.str.replace([' '], '')
        # df[0].to_csv(data+'_'+nome+'.csv') 
        df.to_sql(nome, engine, if_exists='append')


# scrap(url_fii_resultado)
# scrap(url_resultado)
