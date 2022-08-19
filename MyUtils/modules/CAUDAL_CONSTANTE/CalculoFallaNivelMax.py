from help import extract_excel_data
from CalculoTotal import CalculoTotal

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

    def __init__(self,falla_buscada, nivel_min,caudal_objetivo) -> None:
        # ----------------- INITIAL VARS -----------------------

        self.falla_buscada = falla_buscada
        self.nivel_min = nivel_min
        self.caudal_objetivo = caudal_objetivo
        self.nivel_max = self.nivel_min * 1.2
        self.input_data = extract_excel_data()
        self.nivel_min_absoluto = self.input_data["Nivel[m]"][0]
        self.nivel_max_absoluto = self.input_data["Nivel[m]"][-1]
        if nivel_min < self.nivel_min_absoluto:
            raise Exception(f'Nivel minimo {self.nivel_min} es menor al mínimo absoluto {self.nivel_min_absoluto} ')

        # ----------------- ITERATION VARS --------------------
        self.falla_obtenida = 0
        self.falla_paso_previo = 0
        self.diferencia_porcentual_paso_previo = 1.1
        self.error = False
        self.multiplicador = 5
        self.nivel_maximo_critico = False
        self.nivel_maximo_absoluto_alcanzado = False
        
        # --------------- CALC ---------------------
        self._calcular_falla()
    
    def _ajuste_falla(self):
        # Partimos de una diferencia porcentual entre la falla obtenida y la buscada para concer la magnitud del error.
        # Este valor lo usaremos con un multiplicador para aplicar un cambio al nivel máximo para realizar otra iteración
        diferencia_porcentual = abs(1- self.falla_obtenida_exacta/self.falla_buscada)
        print(self.falla_obtenida,diferencia_porcentual,self.multiplicador,self.nivel_max)
        if diferencia_porcentual > self.diferencia_porcentual_paso_previo and self.multiplicador>0.5:
            # Si la diferencia porcentual es mayor a la del paso previo quiere decir que estamos cerca del valor y estamos iterando entre valores mayores y menores al nivel máximo que converge. Por lo tanto disminuimos el multiplicador
            self.multiplicador -=0.5
        cambio = diferencia_porcentual*self.multiplicador
        if self.falla_obtenida > self.falla_buscada:
            self.nivel_max += cambio
        else:
            self.nivel_max -= cambio
        
        self.diferencia_porcentual_paso_previo = diferencia_porcentual
        

    def _calcular_falla(self):
        while True:
            # Se ejecutará todo hasta que haya un break

            if self.nivel_max < self.nivel_min:
                # Si el nivel máximo es menor al mínimo quiere decir que en la iteración del nivel máximo se llegó a una falla máxima (se produce un break)
                # Sin embargo puede pasar que tengamos un cambio demasiado bruzco por ejemplo buscamos una falla del 5%, con un nivel mino de 140. Imaginemos que en un paso de cálculo llegamos a una falla del 4.9% y nuestro cambio es de 5m, por lo que nuestro nuevo nivel máximo es 138<nivel minimo. Cuando pase por esta verificación entendería que se llegó a una falla máxima sin probar con valores intermedios entre 143 y 140. De suceder este caso por primera vez en las iteraciones del nivel maximo, este se ajusta al nivel minimo y el multiplicador del ajuste se lleva al mínimo para prevenir errores de converencia y se vuelve a iterar.
                if self.nivel_maximo_critico:
                    falla = round(self.falla_paso_previo,2)
                    print(f'La máxima falla para un caudal de {self.caudal_objetivo} es: {falla} ')
                    break
                else:
                    self.nivel_max = self.nivel_min
                    self.nivel_maximo_critico = True
                    self.multiplicador = 0.5
            
            elif self.nivel_max > self.nivel_max_absoluto:
                if self.nivel_maximo_absoluto_alcanzado:
                    falla = round(self.falla_paso_previo,2)
                    print(f'Para un caudal de {self.caudal_objetivo} se alcanza una falla de {falla} llegando al nivel maximo absoluto de {self.nivel_max_absoluto}' )
                    self.error = True
                    break
                else:
                    self.nivel_maximo_absoluto_alcanzado = True
                    self.nivel_max = self.nivel_max_absoluto


            calculo_total = CalculoTotal(
                self.input_data,
                nivel_min=self.nivel_min,
                nivel_max=self.nivel_max,
                caudal_objetivo=self.caudal_objetivo
                )

            self.falla_obtenida = round(calculo_total.falla,1)
            self.falla_obtenida_exacta = calculo_total.falla

            if self.falla_obtenida_exacta == self.falla_paso_previo and self.falla_obtenida_exacta != 0:
                # Si dos fallas consecutivas son exactamente iguales quiere decir que no se están pudiendo conseguir fallas menores por más que aumentemos el nivel máximo. Se genera una falla mínima (se produce un break)
                # Como excepción a la regla se encuentra el caso en que la falla es igual a cero, ya que si el nivel máximo con el que comenzamos la iteración es alto, tardaremos varios pasos de calculo para llegar a un nivel máximo que nos de falla.
                print(f'La mínima falla para un caudal de {self.caudal_objetivo} es: {self.falla_obtenida} ')
                self.error = True
                break
        
            if self.falla_obtenida != self.falla_buscada:
                # Si la falla obtenida es distinta a la buscada realizo un ajuste y luego el while vuelve a ejecutarse
                self.falla_paso_previo = self.falla_obtenida_exacta
                self._ajuste_falla()
            else:
                # Si nada de lo anterior pasó, significa que llegamos a la falla buscada.
                print('Caudal Saliente:',self.caudal_objetivo)
                print('Falla Obtenida:',self.falla_obtenida)
                print('Nivel Máximo:',self.nivel_max)
                print('Nivel Inicial:',calculo_total.nivel_final_iteracion)
                print('Multiplicador:',self.multiplicador)
                print('\n')
                #calculo_total.duracion()
                break


if __name__ == '__main__':

    falla_buscada = 5
    nivel_min = 140
    caudal_objetivo = 730.5

    calculo_falla = CalculoFalla(
            falla_buscada = falla_buscada,
            nivel_min = nivel_min,
            caudal_objetivo= caudal_objetivo
    )