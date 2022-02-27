import pandas as pd
import numpy as np
datos = pd.read_json('./preproceso/sp_pre.json')

nombre_sp = datos['nombre_sp']
#nombre_sp = nombre_sp.str.replace("\n                                ","")
#nombre_sp = nombre_sp.str.replace("                            ","")
#nombre_sp = nombre_sp.str.replace("\n",",")
nombre_sp = list(nombre_sp)
nombre_sp = pd.DataFrame(nombre_sp).T
nombre_sp = nombre_sp.replace('Tarjeta de Video ','',regex=True)
precios_sp = datos['precios_sp']
precios_sp = pd.DataFrame(precios_sp[0])

stock_sp = datos['stock_sp']
stock_sp = datos['stock_sp']
stock_sp = pd.DataFrame(stock_sp)
#print(type(stock_sp))
stock_sp = stock_sp['stock_sp'].tolist()
stock_sp = pd.DataFrame(stock_sp).T
stock_sp = stock_sp.replace('        CANTIDAD: +       ','',regex=True)
stock_sp = stock_sp.replace('\n                                AGOTADO\n                        ','',regex=True)
stock_sp = stock_sp.replace({'\n                                CANTIDAD: +':'' , '\n                                CANTIDAD: ':''},regex=True)
stock_sp = stock_sp.replace({'\n':'' , '\n                        ':''},regex=True)
stock_sp = stock_sp.replace('','AGOTADO',regex=True)
stock_sp = stock_sp.replace('                        ','',regex=True)
stock_sp = stock_sp.replace('                        ','',regex=True)

links_sp = datos['links_sp']
links_sp = pd.DataFrame(links_sp)
#print(type(stock_sp))
links_sp = links_sp['links_sp'].tolist()
links_sp = pd.DataFrame(links_sp).T

df_final = pd.concat([nombre_sp, precios_sp, stock_sp, links_sp],axis=1)
df_final.columns = ['nombre','precios', 'stock', 'links_sp']
df_final=df_final[~df_final["stock"].str.contains("AGOTADO", na=False)]
df_final =df_final.assign(url= 'https://www.spdigital.cl')
df_final['enlaces'] = df_final['url'] + df_final['links_sp']
df_final = df_final.drop(['url'], axis=1)
df_final = df_final.drop(['links_sp'], axis=1)

df_final.to_csv('./resultados/spfinal.csv', index=True, encoding="latin-1")