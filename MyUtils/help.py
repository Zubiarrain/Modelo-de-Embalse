import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter

def create_plot(xpoints, ypoints,labels, title, xlabel, ylabel, marker):
    for i in range(len(xpoints)):

        xpoint = np.array(xpoints[i])
        ypoint = np.array(ypoints[i])
        plt.plot(xpoint, ypoint,marker = marker,label=labels[i])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()

def export_excel(dict,name):
    df = pd.DataFrame(dict)
    writer = ExcelWriter(f"MyUtils/outputs/{name}.xlsx")
    df.to_excel(writer, "H1", index=False)
    writer.save()


def interpolation(x_data,y_data,dato,eje, nombre):
    resultado = None
    for i in range(len(x_data)):
        x_mayor = x_data[i]
        x_menor = x_data[i-1]
        y_mayor = y_data[i]
        y_menor = y_data[i-1]

        if eje == 'x':
            if dato == x_mayor:
                return y_mayor
            elif dato < x_mayor and dato > x_menor:
                resultado = (dato-x_menor)/(x_mayor-x_menor) * (y_mayor-y_menor) + y_menor
                break

        if eje == 'y':
            if dato == y_mayor:
                return x_mayor
            elif dato < y_mayor and dato > y_menor:
                resultado = (dato-y_menor)/(y_mayor-y_menor) * (x_mayor-x_menor) + x_menor
                break

    if resultado is None:
        raise Exception(f"Fallo en interpolación, {nombre}: ({round(dato,2)}) fuera de los límites conocidos")
    else:
        return resultado


import time
def extract_excel_data(path):
    df = pd.read_excel("MyUtils/inputs/" + path, comment='#', index_col=None)
    input_data = df.to_dict()
    for key,value in input_data.items():
        list = df[key].tolist()        
        for i in list:
            if pd.isna(i):
                input_data[key] = list[:list.index(i)]
                break
            else:
                input_data[key] = list
    
    data_verification(input_data)
    return input_data


def data_verification(input_data):
    tiempo = input_data["t[dias]"]
    caudal_entrante = input_data["Caudal Entrante[m³/s]"]
    precipitacion = input_data['Precipitacion[mm/dia]']
    evaporacion= input_data['Evaporacion[mm/dia]']
    entrada = [tiempo, caudal_entrante, precipitacion, evaporacion]

    nivel = input_data['Nivel[m]']
    area = input_data['Area[km2]']
    volumen = input_data['Volumen[Hm3]']
    ley = [nivel,area,volumen]

    for e in entrada:
        for e2 in entrada:
            if len(e) != len(e2):
                raise Exception("La longitud de los parámetros de entrada debe ser la misma")
    
    for i in ley:
        for i2 in ley:
            if len(i) != len(i2):
                raise Exception("La longitud de los datos de ley nivel-area-volumen debe ser la misma")



#extract_excel_data("input_energia_nico.xlsx")



#----------- FUNCION EN DESUSO ----------------------

""" def input_data():
    PATH= r'H:\Mi unidad\FACULTAD\6to Año\Trabajo Final\Programa\CAUDAL_CONSTANTE\INPUT'
    input_data = {
            'caudal_entrante':[],
            'precipitacion':[], 
            'evaporacion':[], 
            'nivel_area':[], 
            'nivel_volumen':[], 
            'nres':[]
            }

    for name,data in input_data.items():
        path_a = PATH + '\\' +  name + '.txt'
        try:
            with open(path_a,'r') as archivo:
                for line in archivo.readlines():
                    info = line.split(',')
                    item_1 = float(info[0].strip())
                    item_2 = float(info[1].strip())
                    data.append((item_1,item_2))
                input_data[name] = tuple(data)
        except Exception as e:
            print(e)
    
    return input_data


def interpolation_txt(curva,dato,eje):
    resultado = None
    for data in curva:
        index = curva.index(data)-1

        x_mayor = data[0]
        x_menor = curva[index][0]
        y_mayor = data[1]
        y_menor = curva[index][1]

        if eje == 'x':
            if dato == x_mayor:
                return y_mayor
            elif dato < x_mayor and dato > x_menor:
                resultado = (dato-x_menor)/(x_mayor-x_menor) * (y_mayor-y_menor) + y_menor
                break

        if eje == 'y':
            if dato == y_mayor:
                return x_mayor
            elif dato < y_mayor and dato > y_menor:
                resultado = (dato-y_menor)/(y_mayor-y_menor) * (x_mayor-x_menor) + x_menor
                break

    if resultado is None:
        raise Exception("No se encontró parámetro para interpolación")
    else:
        return resultado """