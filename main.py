from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os


ruta = os.getcwd() + os.sep
nombre_archivo = 'datos_prueba.csv'


def mostrar_grafico(datos, explode, etiquetas, title, name):
    '''Esta funcion recibe los datos ya definidos en otra función
    y con ellos '''

    plt.pie(datos, explode=explode, labels=etiquetas, autopct='%1.2f%%', shadow=True, startangle=90, labeldistance=1.1)
    plt.axis('equal')
    plt.legend(etiquetas)
    plt.title(title)
    plt.savefig(f'{ruta}{name}', format='png')
    plt.show()


# def cargar_grafico(datos):
#     '''Esta función recibe los datos que se van a mostrar en el gráfico y con
#     ello define las diferentes configuraciones propias del gráfico de barras.'''

#     etiquetas = []
#     valores = []

#     for key, intentos in zip(datos.keys(), datos.values):
#         if len(etiquetas) != 5:
#             etiquetas.append(key)
#             valores.append(intentos)    
#         else:
#             break

#     plt.bar(etiquetas, valores)

#     plt.ylabel('Cantidad de intentos')
#     plt.xlabel('Palabras a adivinar')

#     plt.title('Cantidad de intentos por palabras')
#     #plt.show()


def cargar_grafico(datos):
    '''Esta función recibe los datos que se van a mostrar en el gráfico y con
    ello define las diferentes configuraciones propias del gráfico de barras.'''

    etiquetas = []

    fallos = []
    correctas = []

    for key, intentos in zip(datos.keys(), datos.values):
        if len(etiquetas) != 5:
            if not key[0] in etiquetas:
                etiquetas.append(key[0])

            if key[1] == 'error':
                fallos.append(intentos)
                if len(fallos) > len(correctas)+1:
                    correctas.append(0)
            else:
                if len(fallos) == len(correctas):
                    fallos.append(0)
                correctas.append(1)
        else:
            if key[0] == etiquetas[-1]:
                correctas.append(1)                
            else:
                break

    print(f"Etiquetas: {etiquetas}")
    print(f"Fallos: {fallos}")
    print(f"Correctas: {correctas}")

    indice = np.arange(len(etiquetas))

    # creo barras base
    plt.bar(indice, fallos, label='Intento fallido')

    # creo barras superiores
    plt.bar(indice, correctas, label='Intento correcto', bottom=fallos)

    plt.xticks(indice, etiquetas)
    plt.ylabel("Intentos")
    plt.xlabel("Palabras")
    plt.title('Intentos fallidos por palabras y si se encontró')
    plt.legend()

    plt.show()


def main():
    '''Funcion principal donde se leen los datos a trabajar, se muestran los IDs de partidas
    disponibles para elegir y se pide una elección.'''

    try:
        df_datos = pd.read_csv(f"{ruta}{nombre_archivo}")

        partidas_existentes = df_datos['Partida'].unique().tolist()
        print('IDs de partidas existentes: ', partidas_existentes)
        print()
        while True:
            try:
                id_partida = int(input('Seleccione sobre qué partida mostrar los datos: '))
                if id_partida not in partidas_existentes:
                    raise ValueError
                else:
                    break
            except ValueError:
                print('El valor ingresado es incorrecto o está fuera de rango, pruebe con otro.')
                print('-' * 70)

        datos = df_datos[df_datos['Partida'] == id_partida].groupby(['Palabra', 'Estado ']).size()
    
        print(datos)

        cargar_grafico(datos)
    except FileNotFoundError:
        print(f"No se encontro la ruta del archivo en: {ruta}{nombre_archivo}")




if __name__ == '__main__':
    main()