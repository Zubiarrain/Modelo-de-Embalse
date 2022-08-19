from .CalculoTotal import CalculoTotal
import time
import logging as log
from loggers import logger


class CalculoFalla:
    """
    Esta clase tiene el objetivo de ejecutar el CalculoTotal iterando el nivel máximo y el nivel inicial hasta alcanzar una falla deseada.
    Los datos de entrada serán la falla buscada, el nivel minimo y un caudal objetivo.
    Comenzará con un nivel máximo de un 20% mayor al nivel minimo y con un nivel inicial para el modelo de embalse igual al promedio entre el nivel máximo y el mínimo.
    Ejecutará el CalculoTotal con ciertos valores de entrada y obtendrá la falla. Si esta no es la deseada, cambiará el nivel máximo para para ajustarla hacia donde desea (aumentarlo si la falla fue mayor a la deseada o dismunirlo si la falla fue menor).
    La clase tiene en cuenta que el nivel máximo no puede ser menor al mínimo. Si esto pasa entiende que no se puede alcanzar la falla deseada (obtendremos una falla máxima para ese caudal).
    También tiene en cuenta si al seguir aumentando el nivel máximo la falla no aumenta, llegamos a una falla máxima.
    Ambas situaciones concluyen con la finalizacón de la ejecución.
    """

    def __init__(self,input_data,falla_buscada, nivel_min,nivel_max,caudal_objetivo=None) -> None:


        c_handler = log.FileHandler('CAUDAL-Consigna_Déficit.log',encoding='utf-8')
        format = log.Formatter('%(asctime)s: %(levelname)s [%(message)s]',datefmt = '%d/%m/%Y %I:%M:%S %p')
        c_handler.setFormatter(format)
        logger.handlers[0] = c_handler
        # ----------------- INITIAL VARS -----------------------
        if falla_buscada == 0:
            self.falla_buscada = 0.1
        else:
            self.falla_buscada = falla_buscada
        self.nivel_min = nivel_min
        self.nivel_max = nivel_max

        # ----------------- ITERATION VARS --------------------
        self.iteraciones = 0
        self.tiempo_inicial_corrida = time.time()
        self.tiempo_corrida_minutos = 0
        self.input_data = input_data
        self.falla_obtenida = 0
        self.falla_paso_previo = 0
        self.diferencia_porcentual_paso_previo = 1.1
        self.error = False
        self.multiplicador = 1.1

        self.caudal_modulo = sum(self.input_data['Caudal Entrante[m³/s]'])/len(self.input_data['Caudal Entrante[m³/s]'])
        if caudal_objetivo:
            self.caudal_objetivo = caudal_objetivo
        else:
            self.caudal_objetivo = self.caudal_modulo

        self.convergencia_cercana = False
        self.caudal_superior = {"Caudal":0,"Falla":0}
        self.caudal_inferior = {"Caudal":0,"Falla":0}

        # --------------- CALC ---------------------
        try:
            self._calcular_falla()
        except Exception as e:
            raise Exception(f" {e}\nDb: {self.falla_buscada}")
    
    def _ajuste_falla(self):
        # Partimos de una diferencia porcentual entre la falla obtenida y la buscada para concer la magnitud del error.
        # Este valor lo usaremos con un multiplicador para aplicar un cambio al nivel máximo para realizar otra iteración
        diferencia_porcentual = abs(self.falla_obtenida_exacta - self.falla_buscada)/100
        logger.info(f'Iteración: {self.iteraciones} || Caudal: {round(self.caudal_objetivo,2)} || Déficit Obtenido: {self.falla_obtenida_exacta} / {self.falla_buscada}')
        logger.handlers[0].close()

        if self.falla_obtenida_exacta > self.falla_buscada:
            self.caudal_superior["Caudal"] = self.caudal_objetivo
            self.caudal_superior["Falla"] = self.falla_obtenida_exacta
        else:
            self.caudal_inferior["Caudal"] = self.caudal_objetivo
            self.caudal_inferior["Falla"] = self.falla_obtenida_exacta

        if (self.falla_obtenida_exacta - self.falla_buscada) * (self.falla_paso_previo - self.falla_buscada) < 0 and self.convergencia_cercana == False:
            self.convergencia_cercana = True
            logger.warning("Convergencia cercana")

        if self.convergencia_cercana:
            if self.falla_buscada == 0.1:
                self.caudal_objetivo=(self.caudal_superior["Caudal"]+self.caudal_inferior["Caudal"])/2
            else:
                dif_falla_sup = abs(self.caudal_superior["Falla"] - self.falla_buscada)
                dif_falla_inf = abs(self.caudal_inferior["Falla"] - self.falla_buscada)
                self.caudal_objetivo = (self.caudal_superior["Caudal"]*1/dif_falla_sup+self.caudal_inferior["Caudal"]*1/dif_falla_inf)/(1/dif_falla_sup+1/dif_falla_inf)

        else:

            cambio = self.multiplicador + diferencia_porcentual
            if self.falla_obtenida_exacta > self.falla_buscada:
                self.caudal_objetivo /= cambio
            else:
                self.caudal_objetivo *= cambio
        self.diferencia_porcentual_paso_previo = diferencia_porcentual
        

    def _calcular_falla(self):
        no_falla = True
        while True:
            if self.iteraciones > 20:
                logger.critical('Demasiadas iteraciones, puede existir problemas de convergencia para las condiciones ingresadas')
            self.iteraciones +=1
            try:
                self.calculo_total = CalculoTotal(
                    input_data=self.input_data,
                    nivel_min=self.nivel_min,
                    nivel_max=self.nivel_max,
                    caudal_objetivo=self.caudal_objetivo
                    )

                self.falla_obtenida = round(self.calculo_total.falla,1)
                self.falla_obtenida_exacta = self.calculo_total.falla

                """ if self.falla_obtenida_exacta == self.falla_paso_previo and self.falla_obtenida_exacta != 0 :
                    # Si dos fallas consecutivas son exactamente iguales quiere decir que no se están pudiendo conseguir fallas menores por más que aumentemos el nivel máximo. Se genera una falla mínima (se produce un break)
                    # Como excepción a la regla se encuentra el caso en que la falla es igual a cero, ya que si el nivel máximo con el que comenzamos la iteración es alto, tardaremos varios pasos de calculo para llegar a un nivel máximo que nos de falla.
                    print(f'La mínima falla para un caudal de {self.caudal_objetivo} es: {self.falla_obtenida} ')
                    print("Falla exacta",self.falla_obtenida_exacta)
                    print("falla paso previo",self.falla_paso_previo)
                    self.error = True
                    break """
            
                if self.falla_obtenida != self.falla_buscada:
                    # Si la falla obtenida es distinta a la buscada realizo un ajuste y luego el while vuelve a ejecutarse
                    self._ajuste_falla()
                    self.falla_paso_previo = self.falla_obtenida_exacta
                    
                else:
                    self.caudal_objetivo = round(self.caudal_objetivo,2)
                    # Si nada de lo anterior pasó, significa que llegamos a la falla buscada.
                    logger.warning("Déficit Encontrado")
                    logger.info(f'Caudal Saliente:: {self.caudal_objetivo}')
                    logger.info(f'Déficit Obtenido: {self.falla_obtenida_exacta}')
                    logger.info(f'Nivel Mínimo: {self.nivel_min}')
                    logger.info(f'Nivel Inicial: {self.calculo_total.nivel_final_iteracion}')
                    logger.info(f"Iteraciones: {self.iteraciones}")
                    logger.warning("Fin de la iteración")
                    logger.handlers[0].close()
                    #calculo_total.duracion()
                    break
            except Exception as e:
                error = str(e)
                if error.find("Final") and no_falla:
                    if self.iteraciones > 1:
                        logger.error("Error")
                        self.caudal_objetivo = max(self.caudal_superior["Caudal"],self.caudal_inferior["Caudal"]) *1.01
                        self.multiplicador = 1.01
                        no_falla = False
                    else:
                        logger.error("Error")
                        self.caudal_objetivo *= 0.1
                else:
                    raise Exception(e)

        self.tiempo_corrida_minutos = round((time.time() - self.tiempo_inicial_corrida)/60,4)

if __name__ == '__main__':

    falla_buscada = 5
    nivel_min = 140
    nivel_max = 192.5

    calculo_falla = CalculoFalla(
            falla_buscada = falla_buscada,
            nivel_min = nivel_min,
            nivel_max=nivel_max
    )