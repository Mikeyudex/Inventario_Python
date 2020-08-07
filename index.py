"""Desarrolado por Miguel García Yudex"""

from tkinter import ttk
from tkinter import *
from tkinter import messagebox, Scrollbar, Image
from datetime import date
from datetime import datetime
import time
import os



import sqlite3

class product:

    #Obtener la fecha actual
    fecha_actual = datetime.now()
    print("La fecha actual es: {}-{}-{}".format(fecha_actual.year, fecha_actual.month, fecha_actual.day))
    hoy = date.today()
    

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Inventario')
        self.wind.geometry("1280x800")
        self.wind.iconbitmap("jupix.ico")
        

        

        # Frame container Ingreso de productos
        frame = LabelFrame(self.wind, text = 'Registra nuevo producto', font = 'Verdana')
        frame.pack(expand = True, fill = "both")
        frame.config(width = 1280, height= 800, bd = 10, relief = "sunken")
        frame.grid(row = 0, column = 0, columnspan =4, pady=20, padx=10)

        

       

        #Name input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1, pady = 10)

        #Input de modelo
        Label(frame, text = 'Modelo: ').grid(row = 1, column = 2)
        self.modelo = Entry(frame)
        self.modelo.grid(row = 1, column = 3)

        #Input de cantidad de productos
        Label(frame, text = 'Cantidad: ').grid(row = 3, column = 0)
        self.cantidad = Entry(frame)
        self.cantidad.grid(row = 3, column = 1, pady = 10)

        #SKU input
        Label(frame, text = 'SKU: ').grid(row = 3, column = 2)
        self.sku = Entry(frame)
        self.sku.grid(row = 3, column = 3, pady = 10)

        #Proveedor Combobox
        Label(frame, text = 'Proveedor: ').grid(row = 1, column = 4)
        self.proveedor = ttk.Combobox(frame, 
                                        values = [
                                            'Dos Estrellas',
                                            'Itaka',
                                            'Villar',
                                            'Wurth',
                                            'Weicon'])
        self.proveedor.grid(row = 1, column = 5, pady = 10)

        
        

        #Precio
        Label(frame, text = 'Precio: ').grid(row = 3, column = 4)
        self.precio = Entry(frame)
        self.precio.grid(row = 3, column = 5, pady = 10)

        #Estado Combobox
        Label(frame, text = 'Estado: ').grid(row = 4, column = 0)
        self.estado = ttk.Combobox(frame, 
                                        values = [
                                            'Recepcionado',
                                            'Despachado',
                                                ])
        self.estado.grid(row = 4, column = 1, pady = 10)

        #Boton Guardar producto
        ttk.Button(frame, text = 'Guardar producto', command = self.add_product).grid(row = 5, columnspan = 6, sticky = W + E)

        #Mensaje de datos guardados
        self.message = Label(text = '', fg = 'red', font = "Verdana 15")
        self.message.grid(row = 6, column = 1, columnspan = 2, sticky = W + E)

        #Dibujando la Tabla
        self.tree = ttk.Treeview(height = 10, columns = ("#1","#2", "#3", "#4", "#5"))
        
        self.tree.grid(row = 7, column = 0, sticky = W + E, columnspan = 5, rowspan = 6, padx = 30)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Modelo', anchor = CENTER)
        self.tree.heading('#2', text = 'Cantidad', anchor = CENTER)
        self.tree.heading('#3', text = 'SKU', anchor = CENTER)
        self.tree.heading('#4', text = 'Proveedor', anchor = CENTER)
        self.tree.heading('#5', text = 'Precio', anchor = CENTER)
        yScr = ttk.Scrollbar(self.tree, orient = 'vertical', command = self.tree.yview)
        xScr = ttk.Scrollbar(self.tree, orient = 'horizontal', command = self.tree.xview)
        self.tree.configure(yscroll = yScr.set, xscroll = xScr.set)
        #yScr.grid(side = "RIGHT")
        #xScr.pack(side = "BOTTOM")
        
     
    
        #Botones de editar y borrar
        ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 15, column = 0, sticky = W + E, columnspan = 2)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 15, column = 2, sticky = W + E, columnspan = 3)

        #Llenando las filas de la tabla
        self.get_products()

        #Buscar por SKU
        Label(text = "Búsqueda de Productos", font = "Verdana 18 bold",).grid(row = 17, column = 0, pady = 5, columnspan = 2)
        Label(text = "Buscar Producto por SKU: ", font = "Verdana 16").grid(row = 18, column = 0, pady = 5, sticky = W + E)
        self.input = Entry(self.wind)
        self.input.grid(row = 18, column = 1)
        busqueda = ttk.Button(text = "Buscar", command = self.search)
        busqueda.grid(row = 20, column = 1, pady = 4)

        #Crear boton salir
        salir = ttk.Button(text = "Salir", command = self.salir)
        salir.grid(row = 20, column = 0, columnspan = 2, rowspan = 5, sticky = E)


    #Salir del programa
    def salir(self):
        messagebox.showinfo("Message", "Se cerrará la ventana de Inventario")
        self.wind.destroy()
        

    #Realizar busqueda por SKU
    def search(self):
        m = self.input.get()
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        resul = cursor.execute('SELECT * FROM product WHERE sku=?', (m,))
        rows = resul.fetchone()
        print("Producto buscado: ", rows)
        lista = Listbox(self.wind, height = 4)
        lista.grid(row = 17, column = 1)

        for row in rows:
            lista.insert(END, row)

        
        
    #Ejecutando consulta en DB
    def run_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #Obtener los productos
    def get_products(self):
        
        #Limpiando la tabla de tree
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        fecha = self.hoy #Fecha de hoy
        #consultando los datos en database por fecha Now
        
        query =  "SELECT * FROM product WHERE fecha = '{}'".format(fecha)

        db_rows = self.run_consulta(query)  #Retorna la consulta de BD
        

        #rellenando los datos
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4], row[5], row[7]))

        #Obteniendo el la cantidad de productos recibidos por dia

        fecha = self.hoy #Fecha de hoy
        #consultando los datos en database por fecha Now
        
        query =  "SELECT count(*) FROM product WHERE fecha = '{}'".format(fecha)

        db_rows = self.run_consulta(query)  #Retorna la consulta de BD

        total_recepcionado = list(db_rows)
        print(str(total_recepcionado[0]))

    
        #Frame de Estadisticas Recepcionado por dia
        
        frame_ingresados = LabelFrame(self.wind, text = 'Total')
        frame_ingresados.config(width = 100, height = 100)
        frame_ingresados.grid(row = 0, column = 4)
        self.recepcionados = Label(frame_ingresados, text = total_recepcionado, font = 'Verdana 20' )
        self.recepcionados.pack()

         
            
           

    #Validar que el usuario ingrese datos en los campos
    def validation(self):
        return len(self.name.get()) != 0 and len(self.modelo.get()) != 0 and len(self.cantidad.get()) !=0 and len(self.sku.get()) !=0 and len(self.proveedor.get()) !=0 and len(self.precio.get()) !=0

        #Mostrar los datos que ingresa el usuario
    def add_product(self):
        if self.validation():
            fecha_hoy = self.hoy
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.modelo.get(), self.cantidad.get(), self.sku.get(), self.proveedor.get(), fecha_hoy, self.precio.get(), self.estado.get())
            self.run_consulta(query, parameters)
            #Muestra el mensaje en el Frame
            self.message['text'] = 'El producto {} ha sido agregado satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.modelo.delete(0, END)
            self.cantidad.delete(0, END)
            self.sku.delete(0, END)
            self.proveedor.delete(0, END)
            self.precio.delete(0, END)
            self.estado.delete(0, END)
            messagebox.showinfo("Message", "Producto Agregado")

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
        parameters = (nuevo_nombre, nuevo_modelo, nueva_cantidad, name, modelo_old, cantidad_old) #Parametros de la consulta
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
