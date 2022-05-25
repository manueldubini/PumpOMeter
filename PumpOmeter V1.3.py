import requests
import json
import openpyxl
import time
import os

print("PumpOmeter v1.3")
print(" ")
print("Bienvenido! Exito en tus Trades!!")
print(" ")
print("Que par deseas trabajar? Opciones:")
print(" ")
print("-BUSD")
print("-USDT")
print("-ETH")
print("-BTC")
print(" ")
PAR = input("Escriba el par correspondiente: ")
print(" ")
tempgx = int(input("Durante cuantos minutos queres trabajar?: "))
tempg = tempgx * 6
print(" ")
#temp = int(input("Ingrese el tiempo de espera del refresh: "))
print("Iniciando, espere 10 seg")

filename = 'pumpometer.xlsx'
wb = openpyxl.load_workbook(filename)
sheet = wb[PAR]

url = 'https://api.binance.com/api/v3/ticker/price'
anclaje = requests.get(url)
pump = anclaje.json()

contador = 2
for z in pump:
    if PAR in z['symbol']:
        sheet['A' + str(contador)] = z['symbol']
        sheet['B' + str(contador)] = float(z['price'])
        contador = contador + 1
wb.save(filename)

#tempg = 10
while(tempg>0):
    dictVariacion = {}
    temp = 10
    while(temp>0):
        #print(temp)
        time.sleep(1)
        temp = temp - 1
        contador2 = 2
        if temp == 0:
            os.system('cls')
            refresh = requests.get(url)
            refresh1 = refresh.json()
            for r in refresh1:
                if PAR in r['symbol']:
                    sheet['D' + str(contador2)] = float(r['price'])
                    sheet['F' + str(contador2)] = round((float(r['price']) / sheet['B' + str(contador2)].value -1) * 100, 2)
                    variacion = sheet['A' + str(contador2)].value, ": ", sheet['F' + str(contador2)].value, "%"
                    dictVariacion[str(sheet['A' + str(contador2)].value)]= float(sheet['F' + str(contador2)].value)
                    pairlist = sorted(dictVariacion.items(), key=lambda x: x[1])
                    sortdict = dict(pairlist)
                    contador2 = contador2 + 1
            for each in sortdict:
                print(each + ': ' + str(sortdict[each]) + "%")
            print(" ")
            print("****************")
            print("Restan", tempg - 1, "refresh")
            wb.save(filename)
    tempg = tempg - 1

#opcion = input("Desea reiniciar el programa? S/N:")
#if opcion = S:


