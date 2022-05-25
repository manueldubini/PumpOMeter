import requests
import json
import openpyxl
import time
import os
import datetime

os.system('cls')
print("PumpOmeter v1.4")
print(" ")
print("Bienvenido! Exito en tus Trades!!")
print(" ")
print("Que par deseas trabajar? Opciones:")
print(" ")
print("a) BUSD")
print("b) USDT")
print("c) ETH")
print("d) BTC")
print(" ")
par = input("Elija una opcion de la lista (a,b,c,d): ")
if par == 'a':
    PAR = 'BUSD'
elif par == 'b':
    PAR = 'USDT'
elif par == 'c':
    PAR = 'ETH'
elif par == 'd':
    PAR = 'BTC'
else:
    print("La opcion ingresada no existe, reiniciando en 5 seg")
    time.sleep(5)

print(" ")
tempgx = int(input("Durante cuantos minutos queres trabajar?: "))
tempg = tempgx * 6
print(" ")
hora = datetime.datetime.now()
hora2 = datetime.datetime.strftime(hora, '%H:%M')
print("Generando Aclaje de precios, espere 10 seg")
print("Hora de Anclaje: ", hora2)

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
            print("Hora de Anclaje: ", hora2)
            print("Quedan", tempg - 1, "refresh")
            wb.save(filename)
    tempg = tempg - 1
print(" ")
print("Gracias por usar PumpOmeter!")
time.sleep(5)
print(" ")
final = input("El ciclo programado termino! Desea Continuar, Reiniciar o Finalizar?")




