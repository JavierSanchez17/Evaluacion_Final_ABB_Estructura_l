import tkinter as tk
from tkinter import filedialog


class NodoArbolBinario:
    def __init__(self, id, nombre=None, edad=None, telefono=None):
        self.data = id
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.izquierda = None
        self.derecha = None


class VentanaListado:
    def __init__(self, ventana):
        self.ventana = ventana

        self.info_frame = tk.Frame(ventana)
        self.info_frame.pack(side=tk.RIGHT)

        self.frame_dibujo = tk.Frame(ventana)
        self.frame_dibujo.pack()

        self.frame = tk.Frame(ventana)
        self.frame.pack()

        self.search_frame = tk.Frame(ventana)
        self.search_frame.pack()

        self.canvas_width = 800
        self.canvas_height = 300
        self.rect_width = 60
        self.rect_height = 30
        self.rect_spacing = 10
        self.canvas = tk.Canvas(self.frame_dibujo, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.raiz = None

        self.labelid = tk.Label(self.frame, text='ID')
        self.labelid.pack(side=tk.LEFT)

        self.dato = tk.Entry(self.frame)
        self.dato.pack(side=tk.LEFT)

        self.labelnombre = tk.Label(self.frame, text='Nombre')
        self.labelnombre.pack(side=tk.LEFT)

        self.nombre = tk.Entry(self.frame)
        self.nombre.pack(side=tk.LEFT)

        self.labeledad = tk.Label(self.frame, text='Edad')
        self.labeledad.pack(side=tk.LEFT)

        self.edad = tk.Entry(self.frame)
        self.edad.pack(side=tk.LEFT)

        self.labeltelefono = tk.Label(self.frame, text='Telefono')
        self.labeltelefono.pack(side=tk.LEFT)

        self.telefono = tk.Entry(self.frame)
        self.telefono.pack(side=tk.LEFT)

        self.boton_insertari = tk.Button(self.frame, text='Insertar', command=self.insertar)
        self.boton_insertari.pack(side=tk.LEFT)

        self.boton_borrari = tk.Button(self.frame, text='Borrar', command=self.eliminar)
        self.boton_borrari.pack(side=tk.LEFT)

        self.tamanio = tk.Label(self.info_frame, text='Estudiantes Ingresados: 0')
        self.tamanio.pack()

        self.raiz_info = tk.Label(self.info_frame, text='Primer Estudiante Ingresado: -')
        self.raiz_info.pack()

        self.labelbuscado = tk.Label(self.search_frame, text='ID')
        self.labelbuscado.pack(side=tk.LEFT)

        self.dato_buscado = tk.Entry(self.search_frame)
        self.dato_buscado.pack(side=tk.LEFT)

        self.boton_buscar = tk.Button(self.search_frame, text='Buscar', command=self.buscar)
        self.boton_buscar.pack(side=tk.LEFT)

        self.dato_encontrado = tk.Label(self.info_frame, text='')
        self.dato_encontrado.pack()

        self.boton_guardar = tk.Button(self.info_frame, text='Guardar', command=self.guardar)
        self.boton_guardar.pack()

        self.boton_listado = tk.Button(self.info_frame, text='Listado Ascendente', command=self.listado_ascendente)
        self.boton_listado.pack()

        self.boton_abrir = tk.Button(self.info_frame, text='Abrir', command=self.abrir)
        self.boton_abrir.pack()

    def insertar(self):
        valor = self.dato.get()
        nombre = self.nombre.get()
        edad = self.edad.get()
        telefono = self.telefono.get()
        if valor:
            nuevo_nodo = NodoArbolBinario(valor, nombre, edad, telefono)
            if self.raiz is None:
                self.raiz = nuevo_nodo
            else:
                self.insertar_nodo(self.raiz, nuevo_nodo)
            self.dibujar_arbol()
            self.info()
            self.dato.delete(0, tk.END)
            self.nombre.delete(0, tk.END)
            self.edad.delete(0, tk.END)
            self.telefono.delete(0, tk.END)

    def insertar_nodo(self, nodo, nuevo_nodo):
        if int(nuevo_nodo.data) < int(nodo.data):
            if nodo.izquierda is None:
                nodo.izquierda = nuevo_nodo
            else:
                self.insertar_nodo(nodo.izquierda, nuevo_nodo)
        else:
            if nodo.derecha is None:
                nodo.derecha = nuevo_nodo
            else:
                self.insertar_nodo(nodo.derecha, nuevo_nodo)

    def eliminar(self):
        valor_eliminar = self.dato.get()
        if valor_eliminar:
            self.raiz = self.eliminar_valor(self.raiz, valor_eliminar)
            self.dibujar_arbol()
            self.info()
            self.dato.delete(0, tk.END)
        else:
            self.dato_encontrado.config(text="Por favor ingresa un valor para eliminar")

    def eliminar_valor(self, nodo, valor):
        if nodo is None:
            return nodo
        if int(valor) < int(nodo.data):
            nodo.izquierda = self.eliminar_valor(nodo.izquierda, valor)
        elif int(valor) > int(nodo.data):
            nodo.derecha = self.eliminar_valor(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                temp = nodo.derecha
                nodo = None
                return temp
            elif nodo.derecha is None:
                temp = nodo.izquierda
                nodo = None
                return temp

            temp = self.encontrar_minimo(nodo.derecha)
            nodo.data = temp.data
            nodo.derecha = self.eliminar_valor(nodo.derecha, temp.data)
        return nodo

    @staticmethod
    def encontrar_minimo(nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def buscar(self):
        valor = self.dato_buscado.get()
        if valor:
            encontrado = self.buscar_valor(self.raiz, valor)
            if encontrado is not None:
                self.dato_encontrado.config(text=f'Estudiante ID: {encontrado.data} - NOMBRE: {encontrado.nombre} - '
                                                 f'EDAD: {encontrado.edad} - TELEFONO: {encontrado.telefono}')
            else:
                self.dato_encontrado.config(text=f'Valor {valor} no encontrado en el árbol')
        else:
            self.dato_encontrado.config(text='Porfavor ingresa un valor para buscar')

    def buscar_valor(self, nodo, valor):
        if nodo is None:
            return None
        elif int(nodo.data) == int(valor):
            return nodo
        elif int(valor) < int(nodo.data):
            return self.buscar_valor(nodo.izquierda, valor)
        else:
            return self.buscar_valor(nodo.derecha, valor)

    def dibujar_arbol(self):
        self.canvas.delete('all')
        if self.raiz:
            self.dibujar_nodo(self.canvas_width // 2, 50, self.raiz, self.canvas_width // 4)

    def dibujar_nodo(self, x, y, nodo, width):
        if nodo:
            self.canvas.create_rectangle(x - self.rect_width // 2, y - self.rect_height // 2, x + self.rect_width // 2,
                                         y + self.rect_height // 2, fill="lightblue", outline="black", tags="node")
            self.canvas.create_text(x, y, text=f'{str(nodo.data)}. {str(nodo.nombre)}', tags="node")
            if nodo.izquierda:
                self.flecha(x, y + self.rect_height // 2, x - width // 2, y + self.rect_height + self.rect_spacing)
                self.dibujar_nodo(x - width // 2, y + self.rect_height + self.rect_spacing, nodo.izquierda, width // 2)
            if nodo.derecha:
                self.flecha(x, y + self.rect_height // 2, x + width // 2, y + self.rect_height + self.rect_spacing)
                self.dibujar_nodo(x + width // 2, y + self.rect_height + self.rect_spacing, nodo.derecha, width // 2)

    def flecha(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, tags='node')

    def info(self):
        tamanio = self.arbol_tamanio(self.raiz)
        valor_raiz = self.raiz.data if self.raiz else '-'
        valor_nombre = self.raiz.nombre if self.raiz else '-'
        valor_edad = self.raiz.edad if self.raiz else '-'
        valor_telefono = self.raiz.telefono if self.raiz else '-'
        self.tamanio.config(text=f'Estudiantes Ingresados: {tamanio}')
        self.raiz_info.config(text=f'Primer estudiante Ingresado: ID: {valor_raiz} - NOMBRE: {valor_nombre} - '
                                   f'EDAD: {valor_edad} - TELEFONO: {valor_telefono}')

    def nivel_arbol(self, nodo):
        if nodo is None:
            return 0
        else:
            nivel_izquierdo = self.nivel_arbol(nodo.izquierda)
            nivel_derecha = self.nivel_arbol(nodo.derecha)

        return max(nivel_izquierdo, nivel_derecha) + 1

    def arbol_tamanio(self, nodo):
        if nodo is None:
            return 0
        else:
            return 1 + self.arbol_tamanio(nodo.izquierda) + self.arbol_tamanio(nodo.derecha)

    def guardar(self):
        filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if filename:
            with open(filename, 'w') as f:
                self.preorden_guardar(self.raiz, f)

    def preorden_guardar(self, nodo, file):
        if nodo:
            file.write(nodo.data + '\n')
            self.preorden_guardar(nodo.izquierda, file)
            self.preorden_guardar(nodo.derecha, file)

    def listado_ascendente(self):
        filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if filename:
            with open(filename, 'w') as f:
                self.listado(self.raiz, f)

    def listado(self, nodo, file):
        if nodo:
            self.preorden_guardar(nodo.izquierda, file)
            file.write(nodo.data + '\n')
            self.preorden_guardar(nodo.derecha, file)


    def abrir(self):
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "r") as f:
                self.raiz = None
                for line in f:
                    valor = line.strip()
                    self.insertar_desde_archivo(valor)
            self.dibujar_arbol()
            self.info()

    def insertar_desde_archivo(self, valor):
        if not self.raiz:
            self.raiz = NodoArbolBinario(valor)
        else:
            self.insertar_desde_archivo_recursivo(valor, self.raiz)

    def insertar_desde_archivo_recursivo(self, valor, nodo):
        if int(valor) < int(nodo.data):
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbolBinario(valor)
            else:
                self.insertar_desde_archivo_recursivo(valor, nodo.izquierda)
        elif int(valor) > int(nodo.data):
            if nodo.derecha is None:
                nodo.derecha = NodoArbolBinario(valor)
            else:
                self.insertar_desde_archivo_recursivo(valor, nodo.derecha)


def main():
    principal = tk.Tk()  # Se Crea la ventana principal
    principal.title('CENTRO EDUCATIVO NACIONES')
    principal.configure(bg='white')

    VentanaListado(principal)

    principal.mainloop()


if __name__ == '__main__':
    main()

