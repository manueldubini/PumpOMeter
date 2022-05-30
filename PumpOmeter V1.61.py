import requests
import json
import openpyxl
import time
import os
import datetime
from pygame import mixer
import pyautogui as pg
import webbrowser as web

os.system('cls')
print(" PumpOmeter v1.7 Beta\n \n Bienvenido! Exito en tus Trades!!\n")
whats = input(" Desea recibir avisos por Whatsapp? s/n: ")
if whats == 's':
    telefono = input(" Ingrese el numero de telefono: ")
    #web.open('https://web.whatsapp.com/send?phone=+549' + telefono)
    print(" Espere mientras se abre Whatsapp Web")
    #time.sleep(60)
print(" ")
Trend = input(" Vas a usar TrendOmeter?")

print("\n Que par deseas trabajar? Opciones:\n\n a) BUSD\n b) USDT\n c) ETH\n d) BTC\n")
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
cantrefresh = tempanclajes * 10
horadeinicio = datetime.datetime.now()
horadeinicio2 = datetime.datetime.strftime(horadeinicio, '%H:%M')
if whats == 's':
    time.sleep(5)
    pg.write("*---Aviso_PumpOmeter!---*")
    pg.hotkey('shift','enter')
    pg.write("Iniciando nueva sesion de " + str(tempgx) + " minutos de trabajo con anclajes cada " + str(tempanclajes) + " minutos, con par " + PAR + "... Exitos en tus Trades!!")
    pg.press('enter')

while anclajestot > 0:
    if whats == 's':
        pg.write("*---Aviso_PumpOmeter!---*")
        pg.hotkey('shift','enter')
        pg.write("-----Anclaje_Reseteado-----")
        pg.press('enter')
    cantrefresh1 = cantrefresh
    hora = datetime.datetime.now()
    hora2 = datetime.datetime.strftime(hora, '%H:%M')
    print("\n Generando Aclaje de precios, espere 6 segundos")
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
        time.sleep(6)
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
            if float(sortdict[each]) >= 1.5 and float(sortdict[each]) < 3:
                mixer.init()
                mixer.music.load("Alarm02.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta subiendo!!")
                print(" -------------------------")
                if whats == 's':
                    pg.write("*---Aviso_PumpOmeter!---*")
                    pg.hotkey('shift', 'enter')
                    pg.write(each + " subio " + str(float(sortdict[each])) + "% :-)")
                    pg.press('enter')
            if float(sortdict[each]) >= 3 and float(sortdict[each]) < 5:
                mixer.init()
                mixer.music.load("Alarm10.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta subiendo mas!!")
                print(" -------------------------")
                if whats == 's':
                    pg.write("*---Aviso_PumpOmeter!---*")
                    pg.hotkey('shift', 'enter')
                    pg.write(each + " subio " + str(float(sortdict[each])) + "% :-D")
                    pg.press('enter')
            if float(sortdict[each]) >= 5:
                mixer.init()
                mixer.music.load("tada.wav")
                mixer.music.play()
                print(" -------------------------")
                print(" " + each + " esta pumpeando!!")
                print(" -------------------------")
                if whats == 's':
                    pg.write("*---Aviso_PumpOmeter!---*")
                    pg.hotkey('shift', 'enter')
                    pg.write(each + " subio " + str(float(sortdict[each])) + "% :-o")
                    pg.press('enter')
        print(" ")
        print(" ****************")
        print(" PumpOmeter V1.7 Beta")
        print(" Hora de Inicio: ", horadeinicio2)
        print(" Hora de Anclaje: ", hora2)
        print(" Quedan", int(anclajestot - 1), "anclajes reseteables cada", tempanclajes, "minutos")
        print(" Quedan", cantrefresh1 - 1, "refresh de este anclaje")
        wb.save(filename)
        cantrefresh1 = cantrefresh1 - 1
    anclajestot = anclajestot - 1

if whats == 's':
    pg.write("*---Aviso_PumpOmeter!---*")
    pg.hotkey('shift', 'enter')
    pg.write("-----Sesion_finalizada-----")
    pg.press('enter')
print(" ")
print(" Gracias por usar PumpOmeter!")
time.sleep(5)
print(" ")
input(" El ciclo programado termino! toque cualquier tecla")