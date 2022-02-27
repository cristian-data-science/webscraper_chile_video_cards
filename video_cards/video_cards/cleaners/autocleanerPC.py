import pandas as pd
import numpy as np

datos = pd.read_csv('./preproceso/pc_pre.csv',delimiter=',')
datos

# comienzo de limpieza convirtiendo en df y sacando traspuesta


links_p = datos['links_p']
links_p = links_p.str.split(",", expand=True).T
lf0 = links_p[0]
lf1 = links_p[1]
linksfinal = pd.DataFrame(lf0.append(lf1,ignore_index= True),columns=['links'])
linksfinal

precios_p = datos['precios_p']
precios_p = precios_p.str.split(",", expand=True).T
precios_p

rf0 = precios_p[0]
rf1 = precios_p[1]

preciosfinal = pd.DataFrame(rf0.append(rf1,ignore_index= True),columns=['precios'])
preciosfinal

nombre_p = datos['nombre_p']
nombre_p = nombre_p.str.replace("\n                                ","")
nombre_p = nombre_p.str.replace("                            ","")
nombre_p = nombre_p.str.replace("\n",",")
nombre_p = nombre_p.str.replace("Video ","")
nombre_p

nombre_p = nombre_p.str.split(",", expand=True).T
df0 = pd.Series(nombre_p[0])
df0
df1 = pd.Series(nombre_p[1])
df1

nombrefinal = pd.DataFrame(df0.append(df1,ignore_index= True),columns=['nombre'])


stock_p = datos['stock_p']

stock_p = stock_p.str.replace(" Unid.","")
stock_p =stock_p.str.split(",", expand=True).T

st0 = stock_p[0]
st1 = stock_p[1]

stockfinal = pd.DataFrame(st0.append(st1,ignore_index= True),columns=['stock'])
df_final = pd.concat([nombrefinal, preciosfinal, stockfinal, linksfinal],axis=1)

df_final =df_final.assign(url= 'https://www.pcfactory.cl')
df_final.dropna(inplace=True)

df_final['enlaces'] = df_final['url'] + df_final['links']
df_final = df_final.drop(['url'], axis=1)
df_final = df_final.drop(['links'], axis=1)

df_final = df_final.drop_duplicates()

df_final.to_csv('./resultados/pcfinal.csv', index=False)