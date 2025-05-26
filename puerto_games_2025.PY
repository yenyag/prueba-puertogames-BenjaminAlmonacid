import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys

class PuertoGames:
    def __init__(self):
        print("🎮 Iniciando Puerto Games 2025...")
        
        self.root = tk.Tk()
        self.root.title("Puerto Games 2025 - Sistema Completo")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2c3e50')
        
        self.conexion = None
        self.plataformas = []
        self.orden_actual = "titulo"  # Por defecto ordenar por título
        
        if not self.conectar():
            return
            
        self.crear_interfaz()
        self.cargar_datos()
        
    def conectar(self):
        """Conecta a SQL Server con múltiples intentos"""
        print("🔌 Conectando a base de datos...")
        
        servidores = [
            "localhost",
            "localhost\\SQLEXPRESS", 
            ".\\SQLEXPRESS",
            "(localdb)\\MSSQLLocalDB",
            "."
        ]
        
        for servidor in servidores:
            try:
                print(f"🔄 Probando servidor: {servidor}")
                
                connection_string = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={servidor};
                DATABASE=PuertoGames2025;
                Trusted_Connection=yes;
                """
                
                self.conexion = pyodbc.connect(connection_string, timeout=5)
                
                # Probar con una consulta
                cursor = self.conexion.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                
                print(f"✅ ¡Conectado exitosamente a {servidor}!")
                return True
                
            except Exception as e:
                print(f"❌ Error con {servidor}: {str(e)}")
                continue
        
        self.mostrar_error_conexion()
        return False
    
    def mostrar_error_conexion(self):
        messagebox.showerror("Error de Conexión", 
                           "No se pudo conectar a la base de datos.\n" +
                           "Verifica que SQL Server esté ejecutándose.")
        self.root.destroy()
    
    def crear_interfaz(self):
        """Crea la interfaz de usuario"""
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(title_frame, 
                text="🎮 PUERTO GAMES 2025", 
                font=('Arial', 24, 'bold'),
                fg='#ecf0f1', bg='#2c3e50').pack()
        
        tk.Label(title_frame, 
                text="Sistema Completo de Gestión de Videojuegos", 
                font=('Arial', 12),
                fg='#bdc3c7', bg='#2c3e50').pack()
        
        # Frame de búsqueda y filtros
        search_frame = tk.Frame(self.root, bg='#34495e')
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Búsqueda
        tk.Label(search_frame, text="🔍 Buscar:", 
                font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        self.entry_buscar = tk.Entry(search_frame, font=('Arial', 12), width=25)
        self.entry_buscar.pack(side=tk.LEFT, padx=5, pady=10)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_en_tiempo_real)
        
        tk.Button(search_frame, text="🔍 Buscar", 
                 command=self.buscar, bg='#3498db', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Ordenamiento
        tk.Label(search_frame, text="📊 Ordenar por:", 
                font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
        self.combo_orden = ttk.Combobox(search_frame, font=('Arial', 10), 
                                       width=15, state='readonly')
        self.combo_orden['values'] = ['Título (A-Z)', 'Título (Z-A)', 
                                     'Precio (Menor-Mayor)', 'Precio (Mayor-Menor)',
                                     'Stock (Menor-Mayor)', 'Stock (Mayor-Menor)',
                                     'Plataforma (A-Z)', 'Plataforma (Z-A)']
        self.combo_orden.current(0)
        self.combo_orden.pack(side=tk.LEFT, padx=5, pady=10)
        self.combo_orden.bind('<<ComboboxSelected>>', self.cambiar_orden)
        
        # Botones de gestión
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Botones de videojuegos
        juegos_frame = tk.LabelFrame(buttons_frame, text="🎮 Gestión de Videojuegos", 
                                    font=('Arial', 10, 'bold'), 
                                    fg='#ecf0f1', bg='#2c3e50')
        juegos_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        botones_juegos = [
            ("➕ Agregar Juego", self.agregar_juego, '#27ae60'),
            ("✏️ Editar Juego", self.editar_juego, '#f39c12'),
            ("🗑️ Eliminar Juego", self.eliminar_juego, '#e74c3c'),
            ("📦 Modificar Stock", self.modificar_stock, '#8e44ad')
        ]
        
        for texto, comando, color in botones_juegos:
            tk.Button(juegos_frame, text=texto, command=comando,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     padx=15, pady=5).pack(side=tk.LEFT, padx=2)
        
        # Botones de plataformas
        plat_frame = tk.LabelFrame(buttons_frame, text="🎯 Gestión de Plataformas", 
                                  font=('Arial', 10, 'bold'), 
                                  fg='#ecf0f1', bg='#2c3e50')
        plat_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        botones_plat = [
            ("➕ Nueva Plataforma", self.agregar_plataforma, '#16a085'),
            ("✏️ Editar Plataforma", self.editar_plataforma, '#d68910'),
            ("🗑️ Eliminar Plataforma", self.eliminar_plataforma, '#c0392b')
        ]
        
        for texto, comando, color in botones_plat:
            tk.Button(plat_frame, text=texto, command=comando,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     padx=15, pady=5).pack(side=tk.LEFT, padx=2)
        
        # Botones de utilidades
        utils_frame = tk.LabelFrame(buttons_frame, text="📊 Estadísticas y Utilidades", 
                                   font=('Arial', 10, 'bold'), 
                                   fg='#ecf0f1', bg='#2c3e50')
        utils_frame.pack(side=tk.LEFT)
        
        botones_utils = [
            ("📊 Gráfico Plataformas", self.mostrar_grafico_plataformas, '#9b59b6'),
            ("💰 Gráfico Precios", self.mostrar_grafico_precios, '#e67e22'),
            ("📈 Estadísticas", self.mostrar_estadisticas, '#34495e'),
            ("🔄 Actualizar Todo", self.cargar_datos, '#3498db')
        ]
        
        for texto, comando, color in botones_utils:
            tk.Button(utils_frame, text=texto, command=comando,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     padx=15, pady=5).pack(side=tk.LEFT, padx=2)
        
        self.crear_tabla()
        
        # Barra de estado
        self.status_bar = tk.Label(self.root, text="✅ Conectado", 
                                  relief=tk.SUNKEN, anchor=tk.W,
                                  bg='#34495e', fg='#ecf0f1',
                                  font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def crear_tabla(self):
        """Crea la tabla de videojuegos"""
        table_frame = tk.Frame(self.root, bg='#2c3e50')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tabla
        columns = ('ID', 'Título', 'Precio', 'Stock', 'Plataforma')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set,
                                height=18)
        
        # Configurar encabezados
        self.tree.heading('ID', text='ID')
        self.tree.heading('Título', text='Título del Juego')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Plataforma', text='Plataforma')
        
        # Configurar columnas
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Título', width=350, anchor='w')
        self.tree.column('Precio', width=100, anchor='center')
        self.tree.column('Stock', width=80, anchor='center')
        self.tree.column('Plataforma', width=150, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Eventos
        self.tree.bind('<Double-1>', lambda e: self.editar_juego())
        
        # Tags para colores alternados
        self.tree.tag_configure('oddrow', background='#ecf0f1')
        self.tree.tag_configure('evenrow', background='#bdc3c7')
    
    def cambiar_orden(self, event=None):
        """Cambia el orden de visualización"""
        orden_seleccionado = self.combo_orden.get()
        
        if "Título (A-Z)" in orden_seleccionado:
            self.orden_actual = "titulo ASC"
        elif "Título (Z-A)" in orden_seleccionado:
            self.orden_actual = "titulo DESC"
        elif "Precio (Menor-Mayor)" in orden_seleccionado:
            self.orden_actual = "precio ASC"
        elif "Precio (Mayor-Menor)" in orden_seleccionado:
            self.orden_actual = "precio DESC"
        elif "Stock (Menor-Mayor)" in orden_seleccionado:
            self.orden_actual = "stock ASC"
        elif "Stock (Mayor-Menor)" in orden_seleccionado:
            self.orden_actual = "stock DESC"
        elif "Plataforma (A-Z)" in orden_seleccionado:
            self.orden_actual = "p.nombre ASC"
        elif "Plataforma (Z-A)" in orden_seleccionado:
            self.orden_actual = "p.nombre DESC"
        
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga todos los videojuegos con ordenamiento"""
        try:
            cursor = self.conexion.cursor()
            
            # Cargar plataformas
            cursor.execute("SELECT id_plataforma, nombre FROM Plataformas ORDER BY nombre")
            self.plataformas = cursor.fetchall()
            
            # Cargar videojuegos con orden
            query = f"""
                SELECT v.id_videojuego, v.titulo, v.precio, v.stock, p.nombre
                FROM Videojuegos v
                JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
                ORDER BY {self.orden_actual}
            """
            cursor.execute(query)
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos con colores alternados
            registros = cursor.fetchall()
            for i, registro in enumerate(registros):
                precio_formato = f"${registro[2]:,.0f}"
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.tree.insert('', 'end', values=(
                    registro[0], registro[1], precio_formato, 
                    registro[3], registro[4]
                ), tags=(tag,))
            
            self.status_bar.config(text=f"✅ {len(registros)} videojuegos cargados - Ordenado por: {self.combo_orden.get()}")
            cursor.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")
    
    def buscar(self):
        """Busca videojuegos por título o plataforma"""
        termino = self.entry_buscar.get().strip()
        if not termino:
            self.cargar_datos()
            return
        
        try:
            cursor = self.conexion.cursor()
            query = f"""
                SELECT v.id_videojuego, v.titulo, v.precio, v.stock, p.nombre
                FROM Videojuegos v
                JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
                WHERE v.titulo LIKE ? OR p.nombre LIKE ?
                ORDER BY {self.orden_actual}
            """
            cursor.execute(query, (f'%{termino}%', f'%{termino}%'))
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar resultados
            registros = cursor.fetchall()
            for i, registro in enumerate(registros):
                precio_formato = f"${registro[2]:,.0f}"
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.tree.insert('', 'end', values=(
                    registro[0], registro[1], precio_formato, 
                    registro[3], registro[4]
                ), tags=(tag,))
            
            self.status_bar.config(text=f"🔍 {len(registros)} resultados para '{termino}'")
            cursor.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {e}")
    
    def buscar_en_tiempo_real(self, event):
        """Búsqueda automática mientras se escribe"""
        self.root.after(300, self.buscar)
    
    # ==================== GESTIÓN DE VIDEOJUEGOS ====================
    
    def agregar_juego(self):
        """Agregar nuevo videojuego"""
        self.ventana_formulario_juego("Agregar Videojuego")
    
    def editar_juego(self):
        """Editar videojuego seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un videojuego para editar")
            return
        
        item = self.tree.item(seleccion[0])
        id_juego = item['values'][0]
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT titulo, precio, stock, id_plataforma 
                FROM Videojuegos WHERE id_videojuego = ?
            """, (id_juego,))
            datos = cursor.fetchone()
            cursor.close()
            
            if datos:
                self.ventana_formulario_juego("Editar Videojuego", datos, id_juego)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener datos: {e}")
    
    def eliminar_juego(self):
        """Eliminar videojuego seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un videojuego para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        id_juego = item['values'][0]
        titulo = item['values'][1]
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Estás seguro de eliminar '{titulo}'?\n\nEsta acción no se puede deshacer."):
            try:
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM Videojuegos WHERE id_videojuego = ?", (id_juego,))
                self.conexion.commit()
                cursor.close()
                
                messagebox.showinfo("Éxito", "Videojuego eliminado correctamente")
                self.cargar_datos()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")
    
    def modificar_stock(self):
        """Modificar stock de videojuego seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un videojuego para modificar stock")
            return
        
        item = self.tree.item(seleccion[0])
        id_juego = item['values'][0]
        titulo = item['values'][1]
        stock_actual = item['values'][3]
        
        # Ventana para modificar stock
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Modificar Stock - {titulo}")
        ventana.geometry("400x250")
        ventana.configure(bg='#34495e')
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (400 // 2)
        y = (ventana.winfo_screenheight() // 2) - (250 // 2)
        ventana.geometry(f"400x250+{x}+{y}")
        
        tk.Label(ventana, text=f"📦 Modificar Stock", font=('Arial', 16, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=20)
        
        tk.Label(ventana, text=f"Juego: {titulo}", font=('Arial', 12),
                fg='#ecf0f1', bg='#34495e').pack(pady=5)
        
        tk.Label(ventana, text=f"Stock actual: {stock_actual}", font=('Arial', 12, 'bold'),
                fg='#3498db', bg='#34495e').pack(pady=5)
        
        tk.Label(ventana, text="Nuevo stock:", font=('Arial', 12),
                fg='#ecf0f1', bg='#34495e').pack(pady=(20, 5))
        
        entry_stock = tk.Entry(ventana, font=('Arial', 14), width=10, justify='center')
        entry_stock.pack(pady=5)
        entry_stock.insert(0, str(stock_actual))
        entry_stock.select_range(0, tk.END)
        entry_stock.focus()
        
        def guardar_stock():
            try:
                nuevo_stock = int(entry_stock.get())
                if nuevo_stock < 0:
                    messagebox.showerror("Error", "El stock no puede ser negativo")
                    return
                
                cursor = self.conexion.cursor()
                cursor.execute("UPDATE Videojuegos SET stock = ? WHERE id_videojuego = ?", 
                              (nuevo_stock, id_juego))
                self.conexion.commit()
                cursor.close()
                
                messagebox.showinfo("Éxito", f"Stock actualizado a {nuevo_stock}")
                ventana.destroy()
                self.cargar_datos()
                
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar stock: {e}")
        
        buttons_frame = tk.Frame(ventana, bg='#34495e')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="💾 Guardar", command=guardar_stock,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancelar", command=ventana.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Enter para guardar
        entry_stock.bind('<Return>', lambda e: guardar_stock())
    
    def ventana_formulario_juego(self, titulo, datos=None, id_juego=None):
        """Ventana para agregar/editar videojuegos"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("500x400")
        ventana.configure(bg='#34495e')
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (500 // 2)
        y = (ventana.winfo_screenheight() // 2) - (400 // 2)
        ventana.geometry(f"500x400+{x}+{y}")
        
        tk.Label(ventana, text=titulo, font=('Arial', 16, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=20)
        
        form_frame = tk.Frame(ventana, bg='#34495e')
        form_frame.pack(padx=40, fill=tk.BOTH, expand=True)
        
        # Campo título
        tk.Label(form_frame, text="🎮 Título del juego:", font=('Arial', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(10, 5))
        entry_titulo = tk.Entry(form_frame, font=('Arial', 12), width=45)
        entry_titulo.pack(pady=(0, 15))
        
        # Campo precio
        tk.Label(form_frame, text="💰 Precio:", font=('Arial', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(0, 5))
        entry_precio = tk.Entry(form_frame, font=('Arial', 12), width=45)
        entry_precio.pack(pady=(0, 15))
        
        # Campo stock
        tk.Label(form_frame, text="📦 Stock:", font=('Arial', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(0, 5))
        entry_stock = tk.Entry(form_frame, font=('Arial', 12), width=45)
        entry_stock.pack(pady=(0, 15))
        
        # Campo plataforma
        tk.Label(form_frame, text="🎯 Plataforma:", font=('Arial', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(0, 5))
        combo_plataforma = ttk.Combobox(form_frame, font=('Arial', 12), 
                                       width=42, state='readonly')
        combo_plataforma['values'] = [p[1] for p in self.plataformas]
        combo_plataforma.pack(pady=(0, 20))
        
        # Llenar datos si es edición
        if datos:
            entry_titulo.insert(0, datos[0])
            entry_precio.insert(0, str(datos[1]))
            entry_stock.insert(0, str(datos[2]))
            
            for i, plat in enumerate(self.plataformas):
                if plat[0] == datos[3]:
                    combo_plataforma.current(i)
                    break
        
        def guardar():
            titulo_juego = entry_titulo.get().strip()
            precio = entry_precio.get().strip()
            stock = entry_stock.get().strip()
            plataforma_nombre = combo_plataforma.get()
            
            if not all([titulo_juego, precio, stock, plataforma_nombre]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                precio_float = float(precio)
                stock_int = int(stock)
                
                if precio_float <= 0:
                    messagebox.showerror("Error", "El precio debe ser mayor a 0")
                    return
                
                if stock_int < 0:
                    messagebox.showerror("Error", "El stock no puede ser negativo")
                    return
                
                # Obtener ID de plataforma
                id_plataforma = None
                for plat in self.plataformas:
                    if plat[1] == plataforma_nombre:
                        id_plataforma = plat[0]
                        break
                
                cursor = self.conexion.cursor()
                
                if id_juego:  # Editar
                    cursor.execute("""
                        UPDATE Videojuegos 
                        SET titulo = ?, precio = ?, stock = ?, id_plataforma = ?
                        WHERE id_videojuego = ?
                    """, (titulo_juego, precio_float, stock_int, id_plataforma, id_juego))
                    mensaje = "Videojuego actualizado correctamente"
                else:  # Agregar
                    cursor.execute("""
                        INSERT INTO Videojuegos (titulo, precio, stock, id_plataforma)
                        VALUES (?, ?, ?, ?)
                    """, (titulo_juego, precio_float, stock_int, id_plataforma))
                    mensaje = "Videojuego agregado correctamente"
                
                self.conexion.commit()
                cursor.close()
                
                messagebox.showinfo("Éxito", mensaje)
                ventana.destroy()
                self.cargar_datos()
                
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número y stock un entero")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
        
        # Botones
        buttons_frame = tk.Frame(ventana, bg='#34495e')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="💾 Guardar", command=guardar,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=25, pady=8).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancelar", command=ventana.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=25, pady=8).pack(side=tk.LEFT, padx=10)
        
        # Focus en primer campo
        entry_titulo.focus()
    
    # ==================== GESTIÓN DE PLATAFORMAS ====================
    
    def agregar_plataforma(self):
        """Agregar nueva plataforma"""
        self.ventana_formulario_plataforma("Agregar Plataforma")
    
    def editar_plataforma(self):
        """Editar plataforma"""
        self.ventana_lista_plataformas("editar")
    
    def eliminar_plataforma(self):
        """Eliminar plataforma"""
        self.ventana_lista_plataformas("eliminar")
    
    def ventana_formulario_plataforma(self, titulo, datos=None, id_plataforma=None):
        """Ventana para agregar/editar plataformas"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("400x200")
        ventana.configure(bg='#34495e')
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (400 // 2)
        y = (ventana.winfo_screenheight() // 2) - (200 // 2)
        ventana.geometry(f"400x200+{x}+{y}")
        
        tk.Label(ventana, text=titulo, font=('Arial', 16, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=20)
        
        tk.Label(ventana, text="🎯 Nombre de la plataforma:", font=('Arial', 12, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=(10, 5))
        
        entry_nombre = tk.Entry(ventana, font=('Arial', 12), width=30)
        entry_nombre.pack(pady=(0, 20))
        entry_nombre.focus()
        
        if datos:
            entry_nombre.insert(0, datos[0])
        
        def guardar():
            nombre = entry_nombre.get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre de la plataforma es obligatorio")
                return
            
            try:
                cursor = self.conexion.cursor()
                
                if id_plataforma:  # Editar
                    cursor.execute("UPDATE Plataformas SET nombre = ? WHERE id_plataforma = ?",
                                  (nombre, id_plataforma))
                    mensaje = "Plataforma actualizada correctamente"
                else:  # Agregar
                    cursor.execute("INSERT INTO Plataformas (nombre) VALUES (?)", (nombre,))
                    mensaje = "Plataforma agregada correctamente"
                
                self.conexion.commit()
                cursor.close()
                
                messagebox.showinfo("Éxito", mensaje)
                ventana.destroy()
                self.cargar_datos()  # Recargar para actualizar lista de plataformas
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
        
        # Botones
        buttons_frame = tk.Frame(ventana, bg='#34495e')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="💾 Guardar", command=guardar,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancelar", command=ventana.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Enter para guardar
        entry_nombre.bind('<Return>', lambda e: guardar())
    
    def ventana_lista_plataformas(self, accion):
        """Ventana para seleccionar plataforma para editar/eliminar"""
        ventana = tk.Toplevel(self.root)
        titulo = "Editar Plataforma" if accion == "editar" else "Eliminar Plataforma"
        ventana.title(titulo)
        ventana.geometry("500x400")
        ventana.configure(bg='#34495e')
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (500 // 2)
        y = (ventana.winfo_screenheight() // 2) - (400 // 2)
        ventana.geometry(f"500x400+{x}+{y}")
        
        tk.Label(ventana, text=titulo, font=('Arial', 16, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(pady=20)
        
        tk.Label(ventana, text="Selecciona una plataforma:", font=('Arial', 12),
                fg='#ecf0f1', bg='#34495e').pack(pady=(0, 10))
        
        # Lista de plataformas
        list_frame = tk.Frame(ventana, bg='#34495e')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, font=('Arial', 12), height=12,
                            yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Cargar plataformas con información de juegos
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT p.id_plataforma, p.nombre, COUNT(v.id_videojuego) as cantidad_juegos
                FROM Plataformas p
                LEFT JOIN Videojuegos v ON p.id_plataforma = v.id_plataforma
                GROUP BY p.id_plataforma, p.nombre
                ORDER BY p.nombre
            """)
            plataformas_info = cursor.fetchall()
            cursor.close()
            
            for plat in plataformas_info:
                listbox.insert(tk.END, f"{plat[1]} ({plat[2]} juegos)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar plataformas: {e}")
            ventana.destroy()
            return
        
        def ejecutar_accion():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una plataforma")
                return
            
            plataforma_seleccionada = plataformas_info[seleccion[0]]
            id_plat = plataforma_seleccionada[0]
            nombre_plat = plataforma_seleccionada[1]
            cantidad_juegos = plataforma_seleccionada[2]
            
            if accion == "editar":
                ventana.destroy()
                self.ventana_formulario_plataforma("Editar Plataforma", (nombre_plat,), id_plat)
            
            elif accion == "eliminar":
                if cantidad_juegos > 0:
                    messagebox.showerror("Error", 
                                       f"No se puede eliminar '{nombre_plat}' porque tiene {cantidad_juegos} juegos asociados.\n\n" +
                                       "Primero elimina o cambia los juegos de plataforma.")
                    return
                
                if messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Estás seguro de eliminar la plataforma '{nombre_plat}'?\n\n" +
                                      "Esta acción no se puede deshacer."):
                    try:
                        cursor = self.conexion.cursor()
                        cursor.execute("DELETE FROM Plataformas WHERE id_plataforma = ?", (id_plat,))
                        self.conexion.commit()
                        cursor.close()
                        
                        messagebox.showinfo("Éxito", "Plataforma eliminada correctamente")
                        ventana.destroy()
                        self.cargar_datos()
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al eliminar: {e}")
        
        # Botones
        buttons_frame = tk.Frame(ventana, bg='#34495e')
        buttons_frame.pack(pady=20)
        
        texto_boton = "✏️ Editar" if accion == "editar" else "🗑️ Eliminar"
        color_boton = '#f39c12' if accion == "editar" else '#e74c3c'
        
        tk.Button(buttons_frame, text=texto_boton, command=ejecutar_accion,
                 bg=color_boton, fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancelar", command=ventana.destroy,
                 bg='#7f8c8d', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        # Doble clic para ejecutar acción
        listbox.bind('<Double-1>', lambda e: ejecutar_accion())
    
    # ==================== GRÁFICOS Y ESTADÍSTICAS ====================
    
    def mostrar_grafico_plataformas(self):
        """Muestra gráfico de videojuegos por plataforma"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT p.nombre, COUNT(v.id_videojuego) as cantidad
                FROM Plataformas p
                LEFT JOIN Videojuegos v ON p.id_plataforma = v.id_plataforma
                GROUP BY p.id_plataforma, p.nombre
                ORDER BY cantidad DESC
            """)
            
            datos = cursor.fetchall()
            cursor.close()
            
            if not datos:
                messagebox.showinfo("Info", "No hay datos para mostrar")
                return
            
            self.crear_ventana_grafico("📊 Videojuegos por Plataforma", datos, "bar")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear gráfico: {e}")
    
    def mostrar_grafico_precios(self):
        """Muestra gráfico de distribución de precios"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT titulo, precio FROM Videojuegos ORDER BY precio DESC")
            datos = cursor.fetchall()
            cursor.close()
            
            if not datos:
                messagebox.showinfo("Info", "No hay datos para mostrar")
                return
            
            # Crear rangos de precios
            precios = [float(d[1]) for d in datos]
            max_precio = max(precios)
            min_precio = min(precios)
            
            # Definir rangos
            rangos = []
            step = (max_precio - min_precio) / 5
            for i in range(5):
                inicio = min_precio + (i * step)
                fin = min_precio + ((i + 1) * step)
                rangos.append((f"${inicio:.0f}-${fin:.0f}", inicio, fin))
            
            datos_rangos = []
            for nombre_rango, inicio, fin in rangos:
                cantidad = sum(1 for p in precios if inicio <= p < fin or (p == fin and fin == max_precio))
                datos_rangos.append((nombre_rango, cantidad))
            
            self.crear_ventana_grafico("💰 Distribución de Precios", datos_rangos, "pie")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear gráfico: {e}")
    
    def crear_ventana_grafico(self, titulo, datos, tipo):
        """Crea ventana con gráfico"""
        ventana_grafico = tk.Toplevel(self.root)
        ventana_grafico.title(titulo)
        ventana_grafico.geometry("900x700")
        ventana_grafico.configure(bg='white')
        
        fig = Figure(figsize=(12, 8), facecolor='white')
        ax = fig.add_subplot(111)
        
        nombres = [dato[0] for dato in datos]
        valores = [dato[1] for dato in datos]
        
        if tipo == "bar":
            colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', 
                      '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400']
            bars = ax.bar(nombres, valores, color=colores[:len(nombres)])
            
            ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Plataformas', fontsize=12)
            ax.set_ylabel('Cantidad de Videojuegos', fontsize=12)
            
            # Rotar etiquetas si son muchas
            if len(nombres) > 3:
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{valor}', ha='center', va='bottom', fontweight='bold')
        
        elif tipo == "pie":
            # Filtrar valores cero para el gráfico de pie
            datos_filtrados = [(n, v) for n, v in zip(nombres, valores) if v > 0]
            if datos_filtrados:
                nombres_f = [d[0] for d in datos_filtrados]
                valores_f = [d[1] for d in datos_filtrados]
                
                colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
                wedges, texts, autotexts = ax.pie(valores_f, labels=nombres_f, autopct='%1.1f%%',
                                                 colors=colores, startangle=90)
                
                # Mejorar apariencia del texto
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        
        fig.tight_layout()
        
        # Canvas
        canvas = FigureCanvasTkAgg(fig, ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón para cerrar
        tk.Button(ventana_grafico, text="❌ Cerrar", 
                 command=ventana_grafico.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(pady=10)
    
    def mostrar_estadisticas(self):
        """Muestra ventana con estadísticas generales"""
        try:
            cursor = self.conexion.cursor()
            
            # Estadísticas generales
            cursor.execute("SELECT COUNT(*) FROM Videojuegos")
            total_juegos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Plataformas")
            total_plataformas = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(precio) FROM Videojuegos")
            precio_promedio = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT MAX(precio) FROM Videojuegos")
            precio_max = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT MIN(precio) FROM Videojuegos")
            precio_min = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(stock) FROM Videojuegos")
            stock_total = cursor.fetchone()[0] or 0
            
            # Juego más caro
            cursor.execute("SELECT titulo FROM Videojuegos WHERE precio = (SELECT MAX(precio) FROM Videojuegos)")
            juego_mas_caro = cursor.fetchone()
            juego_mas_caro = juego_mas_caro[0] if juego_mas_caro else "N/A"
            
            # Plataforma con más juegos
            cursor.execute("""
                SELECT TOP 1 p.nombre, COUNT(v.id_videojuego) as cantidad
                FROM Plataformas p
                LEFT JOIN Videojuegos v ON p.id_plataforma = v.id_plataforma
                GROUP BY p.nombre
                ORDER BY cantidad DESC
            """)
            plataforma_top = cursor.fetchone()
            plataforma_top_nombre = plataforma_top[0] if plataforma_top else "N/A"
            plataforma_top_cantidad = plataforma_top[1] if plataforma_top else 0
            
            cursor.close()
            
            # Crear ventana de estadísticas
            ventana = tk.Toplevel(self.root)
            ventana.title("📈 Estadísticas Generales")
            ventana.geometry("600x500")
            ventana.configure(bg='#2c3e50')
            ventana.transient(self.root)
            
            # Centrar ventana
            ventana.update_idletasks()
            x = (ventana.winfo_screenwidth() // 2) - (600 // 2)
            y = (ventana.winfo_screenheight() // 2) - (500 // 2)
            ventana.geometry(f"600x500+{x}+{y}")
            
            tk.Label(ventana, text="📈 ESTADÍSTICAS GENERALES", 
                    font=('Arial', 18, 'bold'),
                    fg='#ecf0f1', bg='#2c3e50').pack(pady=20)
            
            # Frame para estadísticas
            stats_frame = tk.Frame(ventana, bg='#34495e', relief=tk.RAISED, bd=2)
            stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            estadisticas = [
                ("🎮 Total de Videojuegos:", f"{total_juegos:,}"),
                ("🎯 Total de Plataformas:", f"{total_plataformas:,}"),
                ("💰 Precio Promedio:", f"${precio_promedio:,.0f}"),
                ("💎 Precio Máximo:", f"${precio_max:,.0f}"),
                ("💸 Precio Mínimo:", f"${precio_min:,.0f}"),
                ("📦 Stock Total:", f"{stock_total:,} unidades"),
                ("👑 Juego Más Caro:", juego_mas_caro),
                ("🏆 Plataforma Top:", f"{plataforma_top_nombre} ({plataforma_top_cantidad} juegos)")
            ]
            
            for i, (etiqueta, valor) in enumerate(estadisticas):
                fila_frame = tk.Frame(stats_frame, bg='#34495e')
                fila_frame.pack(fill=tk.X, padx=20, pady=8)
                
                tk.Label(fila_frame, text=etiqueta, 
                        font=('Arial', 12, 'bold'),
                        fg='#bdc3c7', bg='#34495e', 
                        anchor='w').pack(side=tk.LEFT)
                
                tk.Label(fila_frame, text=valor, 
                        font=('Arial', 12, 'bold'),
                        fg='#3498db', bg='#34495e', 
                        anchor='e').pack(side=tk.RIGHT)
            
            # Botón cerrar
            tk.Button(ventana, text="❌ Cerrar", 
                     command=ventana.destroy,
                     bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                     padx=30, pady=8).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar estadísticas: {e}")

    def run(self):
        """Ejecutar la aplicación"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cerrar_aplicacion()
    
    def cerrar_aplicacion(self):
        """Cerrar aplicación correctamente"""
        if self.conexion:
            self.conexion.close()
            print("🔌 Conexión cerrada")
        self.root.destroy()
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    try:
        app = PuertoGames()
        app.run()
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")