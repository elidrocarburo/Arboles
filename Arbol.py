import matplotlib.pyplot as plt
from collections import deque

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class Arbol:
    def __init__(self, raiz):
        self.raiz = raiz
        self.valoresx = []
        self.valoresy = []
        self.etiquetas = {}

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self.insertar_recursivo(valor, self.raiz)
    
    def insertar_recursivo(self,valor, nodo_actual):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self.insertar_recursivo(valor, nodo_actual.izquierda)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self.insertar_recursivo(valor, nodo_actual.derecha)
        else:
            pass
    
    def buscar(self, valor):
        return self.buscar_recursivo(valor, self.raiz)
    
    def buscar_recursivo(self, valor, nodo_actual):
        if nodo_actual is None:
            return False
        elif valor == nodo_actual.valor:
            return True
        elif valor < nodo_actual.valor:
            return self.buscar_recursivo(valor, nodo_actual.izquierda)
        else:
            return self.buscar_recursivo(valor, nodo_actual.derecha)
        
    def eliminar_sucesor(self, valor):
        self.raiz = self.eliminar_sucesor_r(self.raiz, valor)
    
    def eliminar_sucesor_r(self, nodo, valor):
        if nodo is None:
            return nodo
        
        if valor < nodo.valor:
            nodo.izquierda = self.eliminar_sucesor_r(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar_sucesor_r(nodo.derecha, valor)
        else:
            if nodo.derecha is None:
                return nodo.izquierda
                
            sucesor = self.encontrar_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self.eliminar_sucesor_r(nodo.derecha, sucesor.valor)
        return nodo
    
    def eliminar_predecesor(self, valor):
        self.raiz = self.eliminar_predecesor_r(self.raiz, valor)
    
    def eliminar_predecesor_r(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self.eliminar_predecesor_r(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar_predecesor_r(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            predecesor = self.encontrar_maximo(nodo.izquierda)
            nodo.valor = predecesor.valor
            nodo.izquierda = self.eliminar_predecesor_r(nodo.izquierda, predecesor.valor)
        return nodo

    def encontrar_maximo(self,nodo):
        actual = nodo
        while actual.derecha is not None:
            actual = actual.derecha
        return actual

    def preorden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self.preorden(nodo.izquierda, resultado)
            self.preorden(nodo.derecha, resultado)

    def inorden(self, nodo, resultado):
        if nodo is not None:
            self.inorden(nodo.izquierda, resultado)
            resultado.append(nodo.valor)
            self.inorden(nodo.derecha, resultado)

    def postorden(self, nodo, resultado):
        if nodo is not None:
            self.postorden(nodo.izquierda, resultado)
            self.postorden(nodo.derecha, resultado)
            resultado.append(nodo.valor)

    def niveles(self):
        if self.raiz is None:
            return []
        resultado = []
        cola = deque([self.raiz])

        while cola:
            nodo_actual = cola.popleft()
            resultado.append(nodo_actual.valor)
            if nodo_actual.izquierda is not None:
                cola.append(nodo_actual.izquierda)
            if nodo_actual.derecha is not None:
                cola.append(nodo_actual.derecha)
        return resultado

    def altura(self, nodo):
        if nodo is None:
            return -1
        
        altura_izquierda = self.altura(nodo.izquierda)
        altura_derecha = self.altura(nodo.derecha)
        return max(altura_izquierda, altura_derecha) + 1
    
    def hojas(self, nodo):
        if nodo is None:
            return 0
        elif nodo.izquierda is None and nodo.derecha is None:
            return 1
        else:
            return self.hojas(nodo.izquierda) + self.hojas(nodo.derecha)
    def nodos(self, nodo):
        if nodo is None:
            return 0
        else:
            return 1 + self.nodos(nodo.izquierda) + self.nodos(nodo.derecha)
        
    def completo(self):
        if not self.raiz:
            return True
        cola = deque([self.raiz])
        vacio = False

        while cola:
            nodo_actual = cola.popleft()
            if nodo_actual.izquierda:
                if vacio:
                    return False
                cola.append(nodo_actual.izquierda)
            else:
                vacio = True
            if nodo_actual.derecha:
                if vacio:
                    return False
                cola.append(nodo_actual.derecha)
            else:
                vacio = True

        return True
    
    def lleno(self, nodo=None):
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return True
        if nodo.izquierda is None and nodo.derecha is None:
            return True
        if nodo.izquierda is not None and nodo.derecha is not None:
            return self.lleno(nodo.izquierda) and self.lleno(nodo.derecha)
        return False

    def eliminar_todo(self):
        self.raiz = None
        print("El árbol se ha eliminado.")

    def generar_coordenadas(self,nodo,nivel,pos):
        if nodo is not None:
            self.valoresx.append(pos)
            self.valoresy.append(nivel)
            self.etiquetas[(pos,nivel)] = nodo.valor
            self.generar_coordenadas(nodo.izquierda, nivel-1, pos-2)
            self.generar_coordenadas(nodo.derecha, nivel-1, pos+2)

    def dibujar_conexiones(self,nodo,nivel,pos):
        if nodo is not None:
            if nodo.izquierda is not None:
                plt.plot([pos, pos-2], [nivel, nivel-1], color='black')
                self.dibujar_conexiones(nodo.izquierda, nivel-1, pos-2)
            if nodo.derecha is not None:
                plt.plot([pos, pos+2], [nivel, nivel-1], color='black')
                self.dibujar_conexiones(nodo.derecha, nivel-1, pos+2)

    def mostrar_graficamente(self):
        self.valoresx = []
        self.valoresy = []
        self.etiquetas = {}

        self.generar_coordenadas(self.raiz, 0, 0)
        for (x,y), etiqueta in self.etiquetas.items():
            plt.text(x,y,str(etiqueta), fontsize=12, ha='center')
        
        self.dibujar_conexiones(self.raiz, 0, 0)
        plt.scatter(self.valoresx, self.valoresy, c='blue', s=300, alpha=0.5)
        plt.axis('off')
        plt.show()

    def mostrar_acostado(self, nodo=None,nivel=0):
        if nodo is None:
            nodo = self.raiz
        if nodo.derecha is not None:
            self.mostrar_acostado(nodo.derecha, nivel+1)
        
        print("    " * nivel + str(nodo.valor))
        if nodo.izquierda is not None:
            self.mostrar_acostado(nodo.izquierda, nivel+1)

if __name__ == "__main__":
    arbol = Arbol(None)

    while True:
        print("Programa para formar árboles, seleccione una opción:"
              "\n 1. Insertar un nuevo árbol"
              "\n 2. Buscar un valor en el árbol"
              "\n 3. Recorrer el árbol en preorden"
              "\n 4. Recorrer el árbol en inorden"
              "\n 5. Recorrer el árbol en postorden"
              "\n 6. Eliminar un nodo del árbol predecesor"
              "\n 7. Eliminar un nodo del árbol sucesor"
              "\n 8. Recorrer el árbol por niveles (amplitud)"
              "\n 9. Saber la altura del árbol"
              "\n 10. Saber la cantidad de hojas del árbol"
              "\n 11. Saber la cantidad de nodos"
              "\n 12. ¿Es un árbol binario completo?"
              "\n 13. ¿Es un árbol binario lleno?"
              "\n 14. Graficar árbol"
              "\n 15. Mostrar árbol acostado"
              "\n 16. Eliminar árbol completo"
              "\n 17. Salir del programa"
              "\n")
        opcion = input("Seleccione una de las opciones: ")

        if opcion == '1':
            num = input('Ingrese los valores que desea insertar, separados por comas: ')
            valores = [int(valor.strip()) for valor in num.split(",")]
            for valor in valores:
                arbol.insertar(valor)
            print(f'Valores {valores} insertados.')

        elif opcion == '2':
            busqueda = int(input("¿Qué valor desea buscar en el árbol? "))
            encontrado = arbol.buscar(busqueda)
            print(f'El valor {busqueda} {"está" if encontrado else "no está"} en el árbol.')
            
        elif opcion == '3':
            resultado = []
            arbol.preorden(arbol.raiz, resultado)
            print("Recorrido en preorden:", resultado)

        elif opcion == '4':
            resultado = []
            arbol.inorden(arbol.raiz, resultado)
            print("Recorrido en inorden:", resultado)

        elif opcion == '5':
            resultado = []
            arbol.postorden(arbol.raiz, resultado)
            print("Recorrido en postorden:", resultado)

        elif opcion == '6':
            valor = int(input("¿Qué valor desea eliminar como predecesor? "))
            arbol.eliminar_predecesor(valor)
            print(f'Predecesor {valor} eliminado.')

        elif opcion == '7':
            valor = int(input("¿Qué valor desea eliminar como sucesor? "))
            arbol.eliminar_sucesor(valor)
            print(f'Sucesor {valor} eliminado.')

        elif opcion == '8':
            resultado = arbol.niveles()
            print("Recorrido por niveles:", resultado)

        elif opcion == '9':
            altura = arbol.altura(arbol.raiz)
            print("Altura del árbol:", altura)

        elif opcion == '10':
            cantidad_hojas = arbol.hojas(arbol.raiz)
            print("Cantidad de hojas:", cantidad_hojas)

        elif opcion == '11':
            cantidad_nodos = arbol.nodos(arbol.raiz)
            print("Cantidad de nodos:", cantidad_nodos)

        elif opcion == '12':
            es_completo = arbol.completo()
            print("El árbol está completo:", es_completo)

        elif opcion == '13':
            es_lleno = arbol.lleno()
            print("El árbol está lleno:", es_lleno)

        elif opcion == '14':
            arbol.mostrar_graficamente()
            print("Árbol mostrado gráficamente.")

        elif opcion == '15':
            print("Árbol en orden acostado:")
            arbol.mostrar_acostado()

        elif opcion == '16':
            print("Árbol eliminado.")
            arbol.eliminar_todo()

        elif opcion == '17':
            break
        else:
            print("Opción no válida, intente de nuevo.")