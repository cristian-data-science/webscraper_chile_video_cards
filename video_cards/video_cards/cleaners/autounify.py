import pandas as pd
import numpy as np

pc = pd.read_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/pcfinal.csv',encoding="latin-1")
pc = pc.assign(tienda= 'pcfactory')
sp = pd.read_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/spfinal.csv', encoding="latin-1")
sp = sp.assign(tienda= 'spdigital')
wp = pd.read_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/wpfinal.csv', encoding="latin-1")
wp = wp.assign(tienda= 'winpy')
test = pd.concat([pc, sp, wp ])
test = test.drop(['Unnamed: 0'], axis=1)
#test.dropna(inplace=True)
test[['stock']] = test[['stock']].astype(int)
test['nombre'] = test['nombre'].str.upper()
test['nombre'] = test['nombre'].str.replace('GEFORCE','')
test['nombre'] = test['nombre'].str.replace('NVIDIA','')
test['nombre'] = test['nombre'].str.replace('AMD','')
test['nombre'] = test['nombre'].str.replace('NVIDA','')
test['nombre'] = test['nombre'].str.replace('TARJETA DE VIDEO','')

lista_tarjetas = ['1050TI','1050','1650TI','1650 TI','1650','1660TI','1660 TI','1660S','1660','2060S','2060','2070S','2070', '2080 SUPER', '2080TI','2080 TI','2080', '3050', '3060TI','3060 TI', '3060','3070TI','3070 TI', '3070','3080TI', '3080','3080 TI','3090 TI','3090TI','3090','6500XT','6500 XT','6600XT','6600 XT','6600','6700XT','6700 XT','6700','6800 XT','6800XT','6800','6900XT','6900 XT']
cond = [test['nombre'].str.contains(lista, case=False) for lista in lista_tarjetas]
test['modelo']=np.select(cond,lista_tarjetas)
test['modelo'] = test['modelo'].str.replace(' ','')
test['modelo'] = test['modelo'].replace('0', 'OTROS')
test= test.sort_values("stock", ascending=True, ignore_index=True)

test2 = round(test.groupby(['modelo'])[['stock']].sum())
test2 = test2.sort_values('stock', ascending=False)
pd.DataFrame(test2).reset_index(inplace=True, drop=False)
filtro = test2['modelo'] !=  'OTROS'
test2 = test2[filtro]

test.to_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/resultadofinal.csv')
test2.to_csv('/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/top_stock.csv')