import requests
import json
import openpyxl
import time
import os

print("PumpOmeter v1.2")
filename = 'pumpometer.xlsx'
wb = openpyxl.load_workbook(filename)
sheet = wb['binance']

url = 'https://api.binance.com/api/v3/ticker/price'
anclaje = requests.get(url)
pump = anclaje.json()

contador = 2
for a in pump:
    if 'BUSD' in a['symbol']:
        sheet['A' + str(contador)] = a['symbol']
        sheet['B' + str(contador)] = float(a['price'])
        contador = contador + 1
wb.save(filename)

tempg = 10
while(tempg>0):
    dictVariacion = {}
    temp = 5
    while(temp>0):
        #print(temp)
        time.sleep(1)
        temp = temp - 1
        contador2 = 2
        if temp == 1:
            os.system('cls')
            refresh = requests.get(url)
            refresh1 = refresh.json()
            for r in refresh1:
                if 'BUSD' in r['symbol']:
                    sheet['D' + str(contador2)] = float(r['price'])
                    sheet['F' + str(contador2)] = round((float(r['price']) / sheet['B' + str(contador2)].value -1) * 100, 2)
                    variacion = sheet['A' + str(contador2)].value, ": ", sheet['F' + str(contador2)].value, "%"
                    dictVariacion[str(sheet['A' + str(contador2)].value)]= float(sheet['F' + str(contador2)].value)
                    pairlist = sorted(dictVariacion.items(), key=lambda x: x[1])
                    sortdict = dict(pairlist)
                    contador2 = contador2 + 1
            for each in sortdict:
                print(each + ': ' + str(sortdict[each]) + "%")
            print("****************")
                    #contador2 = contador2 + 1
            wb.save(filename)
    tempg = tempg - 1


#for i in range(sheetresult.nrows):
#    print(sheetresult.cell_value(i,0), "   ", sheetresult.cell_value(i,3))


#def maximo(valores):
#    mayor = valores[0]
#    for i in range(1, len(valores)):
#        if valores[i] > mayor:
#            mayor = valores[i]
#    return mayor

#print(maximo(sheet['D']))


