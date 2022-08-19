from MyUtils.help import extract_excel_data,interpolation


class PasoDeCalculo:
    """
    Esta clase recibirá como datos de entrada las condiciones iniciales para un determinado paso de calculo de un modelo de embalse y los procesará y devolverá las condiciones finales de dicho paso de calculo
    """

    def __init__(self,time,nivel_inicial,volumen_inicial,area_inicial,caudal_entrante,evaporacion,precipitacion,nivel_volumen,nivel_min,nivel_max,caudal_objetivo):

        # ------------ INIT VARS ------------------
        
        self.time = time
        self.nivel_inicial = nivel_inicial
        self.volumen_inicial = volumen_inicial
        self.area_inicial = area_inicial
        self.caudal_entrante = caudal_entrante
        self.evaporacion = evaporacion
        self.precipitacion = precipitacion
        self.nivel_volumen = nivel_volumen
        self.nivel_min = nivel_min
        self.nivel_max = nivel_max
        self.caudal_objetivo = caudal_objetivo

        # ----------- CALCULO DE CONDICIONES FINALES -----------------
        
        self.caudal_balance = (self.precipitacion-self.evaporacion)*self.area_inicial*1000/(24*60*60)
        self.delta_caudal = self.caudal_entrante + self.caudal_balance - self.caudal_objetivo
        self.delta_volumen = self.delta_caudal*24*60*60/1000000
        self.volumen_final = self.volumen_inicial + self.delta_volumen
        # Por defecto, las condiciones de falla y secundarias son cero
        self.tiempo_falla = 0
        self.caudal_falla = 0

        self.tiempo_secundario = 0
        self.caudal_secundario = 0

        if self.volumen_final <= self.nivel_volumen[1][-1]:
            self.nivel_final = interpolation(self.nivel_volumen[0],self.nivel_volumen[1],self.volumen_final,'y',"Vol. Final")
        else:
            pendiente = (self.nivel_volumen[1][-1]-self.nivel_volumen[1][-2])/(self.nivel_volumen[0][-1]-self.nivel_volumen[0][-2])
            self.nivel_final = (self.volumen_final-self.nivel_volumen[1][-2])/pendiente + self.nivel_volumen[0][-2]

        self._verification()
        """ try:
            self.nivel_final = interpolation(self.nivel_volumen[0],self.nivel_volumen[1],self.volumen_final,'y')
            self._verification()
        except:
            self.nivel_final = self.nivel_max """


        # Si no tenemos falla o secundario, el tiempo objetivo será del 100%, de lo contrario, será menor a este
        self.tiempo_objetivo = 1 - self.tiempo_falla - self.tiempo_secundario
        
        
        if self.tiempo_objetivo > 0:
            # Si el tiempo objetivo es mayor a cero (la falla o el secundario no es total) el caudal saliente objetivo será el caudal objetivo
            self.caudal_saliente_objetivo = self.caudal_objetivo
        else:
            self.caudal_saliente_objetivo= 0

        self.caudal_saliente = self.caudal_falla*self.tiempo_falla + self.caudal_secundario*self.tiempo_secundario + self.caudal_objetivo*self.tiempo_objetivo

    def _verification(self):
        
        if self.nivel_final < self.nivel_min:
            # Si el nivel final es menor al mínimo, tendrémos tiempo de falla, caudal de falla y el nivel se limita al nivel mínimo
            self.tiempo_falla = (self.nivel_min - self.nivel_final) / (self.nivel_inicial-self.nivel_final)
            self.caudal_falla = self.caudal_entrante + self.caudal_balance
            self.nivel_final = self.nivel_min

        elif self.nivel_final > self.nivel_max:
            # Si el nivel final es mayor al máximo, tendrémos tiempo secundario, caudal secundario y el nivel se limita al nivel máximo
            self.tiempo_secundario = (self.nivel_final-self.nivel_max) / (self.nivel_final-self.nivel_inicial)
            self.caudal_secundario = self.caudal_entrante + self.caudal_balance
            self.nivel_final = self.nivel_max

if __name__ == '__main__':
    
    input_data = extract_excel_data()
    nivel_volumen = [input_data["Nivel[m]"],input_data["Volumen[Hm3]"]]
    paso_de_calculo_1 = PasoDeCalculo(
                                0,
                                192,
                                35864.38,
                                337.46,
                                242,
                                8.18,
                                0.0673,
                                nivel_volumen,
                                140,
                                192.5,
                                730.528
                                )
    print(paso_de_calculo_1.volumen_final)