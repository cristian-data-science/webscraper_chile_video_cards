import pandas as pd
import numpy as np
from babel.numbers import format_currency

df = pd.read_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/preproceso/tecnopre.csv', encoding= "latin-1")

df.dropna(inplace=True)
df['precios'] = df['precios'].astype(int)
df['precios'] = df['precios'].apply(lambda x: format_currency(x, currency="CLP", locale="es_CL"))
#df = df['nombre'].unique()
df = df.drop_duplicates()
df['stock'] = df['stock'].str.replace('disponibles', '') 
df['stock'] = df['stock'].astype(int)


df.to_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/tecnofinal.csv"')