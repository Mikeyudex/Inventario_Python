from tkinter import ttk
from tkinter import *

import sqlite3

class product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Inventario Jupix')
        self.wind.geometry("600x600")


        # Frame container
        frame = LabelFrame(self.wind, text = 'Registra nuevo producto')
        frame.grid(row = 0, column = 0, columnspan =3, pady=20, padx=20)




        #Name input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1, pady = 10)

        #Input de modelo
        Label(frame, text = 'Modelo: ').grid(row = 2, column = 0)
        self.modelo = Entry(frame)
        self.modelo.grid(row = 2, column = 1)

        #Input de cantidad de productos

        Label(frame, text = 'Cantidad: ').grid(row = 3, column = 0)
        self.cantidad = Entry(frame)
        self.cantidad.grid(row = 3, column = 1, pady = 10)

        #Boton agregar producto
        ttk.Button(frame, text = 'Guardar producto', command = self.add_product).grid(row = 4, columnspan = 3, sticky = W + E)

        #Mensaje de datos guardados
        self.message = Label(text = '', fg = 'red', font = "Verdana 15")
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        #Dibujando la Tabla
        self.tree = ttk.Treeview(height = 10, columns = ("#1","#2"))
        self.tree.grid(row = 6, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Modelo', anchor = CENTER)
        self.tree.heading('#2', text = 'Cantidad', anchor = CENTER)

        #Botones de editar y borrar
        ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 7, column = 0, sticky = W + E, pady = 10)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 7, column = 1, sticky = W + E, pady = 10)

        #Llenando las filas de la tabla
        self.get_products()

    #Ejecutando consulta

    def run_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):

        #Limpiando la tabla de tree
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #consultando los datos en database
        query = 'SELECT * FROM product ORDER BY nombre DESC'
        db_rows = self.run_consulta(query)

        #rellenando los datos
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3]))

        #Validar que el usuario ingrese datos en los campos
    def validation(self):
        return len(self.name.get()) != 0 and len(self.modelo.get()) != 0 and len(self.cantidad.get()) !=0

        #Mostrar los datos que ingresa el usuario
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?)'
            parameters = (self.name.get(), self.modelo.get(), self.cantidad.get())
            self.run_consulta(query, parameters)
            #Muestra el mensaje en el Frame
            self.message['text'] = 'El producto {} ha sido agregado satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.modelo.delete(0, END)
            self.cantidad.delete(0, END)

        else:
            #Si no se inserta los datos se muestra este mensaje
            self.message['text'] = 'Todos los campos son requeridos'

        self.get_products()

    #Funcion para borrar item de la tabla
    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un producto'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE nombre = ?'
        self.run_consulta(query, (name, ))
        self.message['text'] = 'El producto {} ha sido eliminado correctamente'.format(name)
        self.get_products()

    #Editar los productos creados
    def edit_product(self):
        self.message['text'] = '' #Empezar con el texto del mensaje vacio
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un producto'
            return
        name = self.tree.item(self.tree.selection())['text']
        modelo_old = self.tree.item(self.tree.selection())['values'][0]
        cantidad_old = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'

        #nombre viejo
        Label(self.edit_wind, text = 'Nombre anterior: ').grid(row = 1, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 1, column = 2)

        #Nuevo nombre
        Label(self.edit_wind, text = 'Nombre nuevo: ').grid(row = 2, column = 1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row = 2, column = 2)


        #Modelo Anterior
        Label(self.edit_wind, text = 'Modelo Anterior: ').grid(row = 3, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = modelo_old), state = 'readonly').grid(row = 3, column = 2)

        #Nuevo modelo
        Label(self.edit_wind, text = 'Modelo nuevo: ').grid(row = 4, column = 1)
        nuevo_modelo = Entry(self.edit_wind)
        nuevo_modelo.grid(row = 4, column = 2)

        #Cantidad Anterior
        Label(self.edit_wind, text = 'Cantidad Anterior: ').grid(row = 5, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = cantidad_old), state = 'readonly').grid(row = 5, column = 2)

        #Nueva cantidad
        Label(self.edit_wind, text = 'Nueva cantidad: ').grid(row = 6, column = 1)
        nueva_cantidad = Entry(self.edit_wind)
        nueva_cantidad.grid(row = 6, column = 2)





        #Boton de guardar cambios
        Button(self.edit_wind, text = 'Guardar Cambios', command = lambda: self.edit_records(nuevo_nombre.get(), name, nuevo_modelo.get(), modelo_old, nueva_cantidad.get(), cantidad_old)).grid(row = 7, column = 2, sticky = W)

    def edit_records(self, nuevo_nombre, name, nuevo_modelo, modelo_old, nueva_cantidad, cantidad_old ):
        query = 'UPDATE product SET nombre = ?, modelo = ?, cantidad = ? WHERE nombre = ? AND modelo = ? AND cantidad = ? '
        parameters = (name, nuevo_nombre, modelo_old, nuevo_modelo, cantidad_old, nueva_cantidad ) #Parametros de la consulta
        self.run_consulta(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'El producto {} ha sido actualizado satisfactoriamente'.format(name)#El format nos sirve para colocar la variable que queremos mostrar dentro de los corchetes
        self.get_products()
        print("Nuevo nombre: ", nuevo_nombre)
        print("Nuevo Modelo: ", nuevo_modelo)
        print("Nueva cantidad: ", nueva_cantidad)


if __name__ == '__main__':
        window = Tk()
        application = product(window)
        window.mainloop()
