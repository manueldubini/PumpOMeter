import requests
import json
import openpyxl
import time
import os
import datetime
from pygame import mixer


os.system('cls')
print(" PumpOmeter v1.51 Beta")
print(" ")
print(" Bienvenido! Exito en tus Trades!!")
print(" ")
print(" Que par deseas trabajar? Opciones:")
print(" ")
print(" a) BUSD")
print(" b) USDT")
print(" c) ETH")
print(" d) BTC")
print(" ")
par = input(" Elija una opcion de la lista (a,b,c,d): ")
if par == 'a':
    PAR = 'BUSD'
elif par == 'b':
    PAR = 'USDT'
elif par == 'c':
    PAR = 'ETH'
elif par == 'd':
    PAR = 'BTC'
else:
    print(" La opcion ingresada no existe, cierre y vuelva a ejecutar")
    time.sleep(5)
filename = 'pumpometer.xlsx'
wb = openpyxl.load_workbook(filename)
sheet = wb[PAR]
url = 'https://api.binance.com/api/v3/ticker/price'
print(" ")
tempgx = int(input(" Durante cuantos minutos queres trabajar?: "))
print(" ")
tempanclajes = int(input(" Cada cuantos minutos queres refrescar el alclaje?: "))
anclajestot = tempgx / tempanclajes
cantrefresh = tempanclajes * 6
horadeinicio = datetime.datetime.now()
horadeinicio2 = datetime.datetime.strftime(horadeinicio, '%H:%M')
while anclajestot > 0:
    cantrefresh1 = cantrefresh
    hora = datetime.datetime.now()
    hora2 = datetime.datetime.strftime(hora, '%H:%M')
    print(" ")
    print(" Generando Aclaje de precios, espere 10 segundos")
    anclaje = requests.get(url)
    pump = anclaje.json()
    contador = 2
    for z in pump:
        if PAR in z['symbol']:
            sheet['A' + str(contador)] = z['symbol']
            sheet['B' + str(contador)] = float(z['price'])
            contador = contador + 1
        #wb.save(filename)
    while cantrefresh1 > 0:
        dictVariacion = {}
        time.sleep(10)
        contador2 = 2
        os.system('cls')
        refresh = requests.get(url)
        refresh1 = refresh.json()
        for r in refresh1:
            if PAR in r['symbol']:
                sheet['D' + str(contador2)] = float(r['price'])
                sheet['F' + str(contador2)] = round((float(r['price']) / sheet['B' + str(contador2)].value -1) * 100, 2)
                variacion = sheet['A' + str(contador2)].value, ": ", sheet['F' + str(contador2)].value, "%"
                dictVariacion[str(sheet['A' + str(contador2)].value)] = float(sheet['F' + str(contador2)].value)
                pairlist = sorted(dictVariacion.items(), key=lambda x: x[1])
                sortdict = dict(pairlist)
                contador2 = contador2 + 1
        for each in sortdict:
            print(" " + each + ': ' + str(sortdict[each]) + "%")
            if float(sortdict[each]) >= 2 and float(sortdict[each]) < 3:
                mixer.init()
                mixer.music.load("Alarm02.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta subiendo!!")
                print(" -------------------------")
            if float(sortdict[each]) >= 3 and float(sortdict[each]) < 5:
                mixer.init()
                mixer.music.load("Alarm10.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta subiendo mas!!")
                print(" -------------------------")
            if float(sortdict[each]) >= 5:
                mixer.init()
                mixer.music.load("tada.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta pumpeando!!")
                print(" -------------------------")
        print(" ")
        print(" ****************")
        print(" Hora de Inicio: ", horadeinicio2)
        print(" Hora de Anclaje: ", hora2)
        print(" Quedan", int(anclajestot - 1), "anclajes reseteables cada", tempanclajes, "minutos")
        print(" Quedan", cantrefresh1 - 1, "refresh de este anclaje")
        wb.save(filename)
        cantrefresh1 = cantrefresh1 - 1
    anclajestot = anclajestot - 1
print(" ")
print(" Gracias por usar PumpOmeter!")
time.sleep(5)
print(" ")
input(" El ciclo programado termino! toque cualquier tecla")