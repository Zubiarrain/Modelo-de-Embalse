from datetime import timedelta
from MyUtils.help import  interpolation,extract_excel_data
from .PasoDeCalculo import PasoDeCalculo
from more_itertools import sort_together

class CalculoTotal():

    """
    Esta clase, como principio, tomará los valores de entrada de cada paso de tiempo del modelo de embalse.
    Como valores de entrada se le deberá determinar un nivel mínimo y máximo del modelo, un caudal objetivo y el nivel con el que comenzará a funcionar el modelo.
    Llamará a la clase PasoDeCalculo para cada tiempo hasta alcanzar el tiempo total y almacenará cada instancia con sus respectivos datos.
    Al finalizar el modelo verá que el nivel inicial de iteración sea igual al final. De no cumplirse la iteración se volverá a realizar, pero con un nivel inicial igual al nivel final resultante de la corrida anterior.
    Una vez converja la iteración se calcula la falla
    """

    
    def __init__(self,input_data, nivel_min, potencia_firme, rendimiento) -> None:

        # ------------ INIT VARS ------------------

        self.input_data = input_data
        self.nivel_min = nivel_min
        self.potencia_firme = potencia_firme
        self.rendimiento = rendimiento

        # ---------------- VARS --------------------------

        self.time = 0
        fecha_inicial = self.input_data['Fecha Inicial'][0]
        fecha_actual = fecha_inicial + timedelta(days=self.time)
        mes = fecha_actual.month
        self.nivel_max = self.input_data['Nivel_max[m]'][mes-1]
        self.nivel_max_mayor = max(self.input_data['Nivel_max[m]'])
        
        self.nivel_inicial = (self.nivel_max + self.nivel_min)/2
        self.nivel_restituacion = (self.input_data['Nivel_res[m]'][0]+self.input_data['Nivel_res[m]'][-1])/2
        self.nivel_min_absoluto = self.input_data["Nivel[m]"][0]
        self.nivel_max_absoluto = self.input_data["Nivel[m]"][-1]
        
        if self.nivel_min < self.nivel_min_absoluto:
            raise Exception(f'Nivel minimo {self.nivel_min} no puede ser menor al mínimo absoluto {self.nivel_min_absoluto} ')
        if self.nivel_max > self.nivel_max_absoluto:
            raise Exception(f'Nivel máximo {self.nivel_max} no puede ser mayor al máximo absoluto {self.nivel_max_absoluto} ')
        if self.nivel_min > self.nivel_max:
            raise Exception(f'Nivel mínimo {self.nivel_min} no puede ser mayor al nivel máximo {self.nivel_max} ')

        self.calculos = []
        self.time = 0
        self.nivel_final_iteracion = 0
        self.falla = 0

        self.volumen_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Volumen[Hm3]"],self.nivel_inicial,'x',"Vol. Inicial")
        self.area_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Area[km2]"],self.nivel_inicial,'x',"Area Inicial")
        self.caudal_entrante = self.input_data['Caudal Entrante[m³/s]'][self.time]
        self.evaporacion = self.input_data['Evaporacion[mm/dia]'][self.time]
        self.precipitacion = self.input_data['Precipitacion[mm/dia]'][self.time]
        self.nivel_volumen = [self.input_data["Nivel[m]"],self.input_data["Volumen[Hm3]"]]
        self.caudal_nivelRes = [self.input_data["Caudal[m³/s]"],self.input_data["Nivel_res[m]"]]

        self.total_time = self.input_data['t[dias]'][-1]

        # ---------------- CALCULO --------------------------
        try:
            self._iteration()
            
            while self.nivel_final_iteracion != self.nivel_inicial:
                # Si el nivel final del modelo es distinto al nivel inicial del modelo, se resetea el tiempo y la lista de instancias de la clase PasoDeCalculo, el nivel inicial pasa a ser el final del modelo y se vuelve a realizar el modelo de embalse con el nuevo nivel inicial
                self.nivel_inicial = self.nivel_final_iteracion
                self.time = 0
                self.calculos = []
                self._iteration()
            
            # Ya cumplida la condicion nivel_inicial = nivel_final, se calcula la falla y las energías totales
            falla = 0
            energia_falla = 0
            energia_firme = 0
            energia_secundaria = 0
            años = self.total_time/365
            for calculo in self.calculos:
                falla += calculo.tiempo_falla
                energia_falla += calculo.energia_falla
                energia_firme += calculo.energia_firme
                energia_secundaria += calculo.energia_secundaria

            self.falla = round(falla/self.total_time*100,2)
            self.energia_falla = round(energia_falla/años/1000,3)
            self.energia_firme = round(energia_firme/años/1000,3)
            self.energia_secundaria = round(energia_secundaria/años/1000,3)
            self.duracion()
            self.data()
        except Exception as e:
                raise Exception(f" {e}\n Nm: {self.nivel_min} - NM: {self.nivel_max} - P: {self.potencia_firme}")
        
        
    # ---------------------- FUNCTIONS --------------------

    def _iteration(self):
        # Se hace una primera instancia de PasoDeCalculo con el nivel inicial (dato de entrada)
        self.volumen_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Volumen[Hm3]"],self.nivel_inicial,'x',"Vol. Inicial")
        self.area_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Area[km2]"],self.nivel_inicial,'x',"Area Inicial")
        self.calculos.append(PasoDeCalculo(
                                self.time,
                                self.nivel_inicial,
                                self.volumen_inicial,
                                self.area_inicial,
                                self.caudal_entrante,
                                self.evaporacion,
                                self.precipitacion,
                                self.nivel_volumen,
                                self.nivel_min,
                                self.nivel_max,
                                self.potencia_firme,
                                self.nivel_restituacion,
                                self.caudal_nivelRes,
                                self.rendimiento
                                ))
        while self.time < self.total_time-1:
            # Por cada tiempo (hasta el tiempo final) se realiza una instancia de PasoDeCalculo con el nivel incial igual al nivel final del paso anterior.
            self.time += 1
            nivel = self.calculos[-1].nivel_final
            nivel_restitucion = self.calculos[-1].nivel_restitucion
            volumen_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Volumen[Hm3]"],nivel,'x',"Vol. Inicial")
            area_inicial = interpolation(self.input_data["Nivel[m]"],self.input_data["Area[km2]"],nivel,'x',"Area Inicial")
            caudal_entrante = self.input_data['Caudal Entrante[m³/s]'][self.time]
            evaporacion = self.input_data['Evaporacion[mm/dia]'][self.time]
            precipitacion = self.input_data['Precipitacion[mm/dia]'][self.time]
            calculo = PasoDeCalculo(
                                self.time,
                                nivel,
                                volumen_inicial,
                                area_inicial,
                                caudal_entrante,
                                evaporacion,
                                precipitacion,
                                self.nivel_volumen,
                                self.nivel_min,
                                self.nivel_max,
                                self.potencia_firme,
                                nivel_restitucion,
                                self.caudal_nivelRes,
                                self.rendimiento
                                )
            self.calculos.append(calculo)

        self.nivel_final_iteracion = round(self.calculos[-1].nivel_final,2)

    
    def duracion(self):
        # Con esta función logramos almacenar las potencias del modelo en orden decreciente y los tiempos correspondientes a cada caudal
        potencias = []
        tiempos = []
        for calculo in self.calculos:
            #Almaceno en las listas todos las potencias y los tiempos
            potencias.append(calculo.potencia_falla)
            potencias.append(calculo.potencia_secundaria)
            potencias.append(calculo.potencia_firme)
            tiempos.append(calculo.tiempo_falla)
            tiempos.append(calculo.tiempo_secundario)
            tiempos.append(calculo.tiempo_firme)
        
        # Ordena la lista de tiempos en funcion de la lista de potencias. Por ejemplo si tenemos
        # X = ["r", "s", "t", "u", "v", "w", "x", "y", "z"]
        # Y = [ 0,   1,   1,    0,   1,   2,   2,   0,   1]
        # s = sort_together([Y, X])[1]
        # s = ['r', 'u', 'y', 's', 't', 'v', 'z', 'w', 'x']
        # Porque si ordenaramos de menor a mayor a la lista Y, el elemento en la posicion 3 (el segundo cero) pasaria  la posición 1 y el elemento en la posición 7 (el tercer cero) pasaría a la posición 2. Entonces esto se aplica a la lista X, por lo tanto el elemento de la posición 3 (la "u") pasa a estar en la posición 1 y el elemento de la posición 7 (la "y") pasa a la posición 2.
        # Lo que conseguimos con esto es que de la manera que ordenaría a las potencias de mayor a menor (le damos reverse=True para que no lo haga de menor a mayor) ordena a los tiempos. Luego ordenamos las potencias de mayor a menor y quedarán las dos listas ordenadas según la lista de potencias y emparejadas con las potencias-tiempos correspondientes
        tiempos = sort_together([potencias,tiempos],reverse=True)[1]

        # Luego ordeno las potencias de mayor a menor.
        potencias.sort(reverse=True)

        # Busco la posición en la lista de tiempos en el que comienza a haber ceros y redefino la lista para que finalice antes del cero
        index = tiempos.index(0)
        tiempos = tiempos[:index]
        potencias = potencias[:index]

        # Luego armo la lista de duración
        duracion = []
        duracion_acumulada = []
        for i in range(len(tiempos)):
            # Para cada tiempo veo la duracion que le corresponde
            tiempo = tiempos[i]
            duracion_i = tiempo/self.total_time * 100
            duracion.append(duracion_i)
            if i > 0:
                # A partir de la segunda iteración (i=1) la duración acumulada será la duración actual más la anterior.
                duracion_acumulada_i = duracion_i + duracion_acumulada[i-1]
                duracion_acumulada.append(duracion_acumulada_i)
            else:
                # En la primer iteración, la duración acumulada sera igual a la duración
                duracion_acumulada.append(duracion_i)
                
        # Armo un diccionario con los datos extraídos y manipulados para poder exportarlos a un excel
        dict = {
            "Tiempo": tiempos,
            "Potencia": potencias,
            'Duracion':duracion,
            'Duracion Acumulada':duracion_acumulada
            }
        self.duracion_data = dict
        """ export_excel(dict,"Duracion")
        garantia = round(100-self.falla,2)
        create_plot(duracion_acumulada,potencias, f'Curva Duración - Garantía {garantia}%','Duración[%]','Potencia [MW]','') """
    

    def data(self):
        dict = {
            "Tiempo [días]": [],
            "Nivel Inicial [m]": [],
            "Volumen Inicial [Hm³]": [],
            "Area Inicial [Km²]": [],
            'Qe [m³/s]':[],
            'Q Obj [m³/s]':[],
            'H [m]':[],
            'Nres [m]':[],
            'I [mm/día]':[],
            'E [mm/día]':[],
            "Q Balance [m³/s]": [],
            "DQ [m³/s]": [],
            "DV [Hm³]": [],
            "Vf [Hm³]": [],
            "Nf [m]": [],
            "TFalla [%]": [],
            "TSecundario [%]": [],
            "Tfirme [%]": [],
            "P Falla [MW]": [],
            "P Secundaria [MW]": [],
            "P firme [MW]": [],
            "E Falla [MWh]": [],
            "E Secundaria [MWh]": [],
            "E firme [MWh]": [],
            }
        self.niveles = [[],[self.nivel_min]*self.total_time,[self.nivel_max]*self.total_time]
        self.tiempos = [[]]*3
        i = 0
        for calculo in self.calculos:
            dict["Tiempo [días]"].append(calculo.time)
            dict["Nivel Inicial [m]"].append(calculo.nivel_inicial)
            dict["Volumen Inicial [Hm³]"].append(calculo.volumen_inicial)
            dict["Area Inicial [Km²]"].append(calculo.area_inicial)
            dict['Qe [m³/s]'].append(calculo.caudal_entrante)
            dict['Q Obj [m³/s]'].append(calculo.caudal_objetivo)
            dict['H [m]'].append(calculo.salto)
            dict['Nres [m]'].append(calculo.nivel_restitucion)
            dict['I [mm/día]'].append(calculo.precipitacion)
            dict['E [mm/día]'].append(calculo.evaporacion)
            dict["Q Balance [m³/s]"].append(calculo.caudal_balance)
            dict["DQ [m³/s]"].append(calculo.delta_caudal)
            dict["DV [Hm³]"].append(calculo.delta_volumen)
            dict["Vf [Hm³]"].append(calculo.volumen_final)
            dict["Nf [m]"].append(calculo.nivel_final)
            dict["TFalla [%]"].append(calculo.tiempo_falla)
            dict["TSecundario [%]"].append(calculo.tiempo_secundario)
            dict["Tfirme [%]"].append(calculo.tiempo_firme)
            dict["P Falla [MW]"].append(calculo.potencia_falla)
            dict["P Secundaria [MW]"].append(calculo.potencia_secundaria)
            dict["P firme [MW]"].append(calculo.potencia_firme)
            dict["E Falla [MWh]"].append(calculo.energia_falla)
            dict["E Secundaria [MWh]"].append(calculo.energia_secundaria)
            dict["E firme [MWh]"].append(calculo.energia_firme)

            self.niveles[0].append(calculo.nivel_inicial)
            self.tiempos[0].append(calculo.time)
            
            i += 1

        #export_excel(dict,"Output")
        self.total_data = dict
    


if __name__ == '__main__':

    # --------------- CALIBRATION VARS ----------------
    nivel_max = 160
    nivel_min = 142

    # --------------- RUN ----------------

    calculo_total = CalculoTotal(
                nivel_min=nivel_min,
                input_data=extract_excel_data(),
                nivel_max=nivel_max,
                potencia_firme=15.91,
                rendimiento=0.9
                )
    calculo_total.duracion()


