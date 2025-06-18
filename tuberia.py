import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import subprocess
import sys
from datetime import datetime

# Diccionarios base actualizados
# Áreas de conductores por tipo de aislamiento (mm²)
areas_conductores = {
    "THW": {
        "14": 2.08, "12": 3.31, "10": 5.26, "8": 8.37, "6": 13.3, "4": 21.2,
        "3": 26.7, "2": 33.6, "1": 42.4, "1/0": 53.5, "2/0": 67.4, 
        "3/0": 85.0, "4/0": 107.2
    },
    "XHHW": {
        "14": 1.97, "12": 3.12, "10": 5.03, "8": 8.09, "6": 13.0, "4": 21.1,
        "3": 26.2, "2": 33.3, "1": 42.1, "1/0": 53.0, "2/0": 67.0,
        "3/0": 85.0, "4/0": 107.0
    },
    "THHN": {
        "14": 1.63, "12": 2.53, "10": 4.18, "8": 6.62, "6": 10.7, "4": 17.2,
        "3": 21.2, "2": 26.7, "1": 32.7, "1/0": 41.7, "2/0": 52.6,
        "3/0": 64.2, "4/0": 78.7
    }
}

# Tabla de tuberías con áreas totales (mm²)
tabla_tuberias = {
    "EMT": {
        "1/2": 196, "3/4": 336, "1": 558, "1 1/4": 832, 
        "1 1/2": 1033, "2": 1809
    },
    "PVC": {
        "1/2": 233, "3/4": 387, "1": 638, "1 1/4": 897, 
        "1 1/2": 1038, "2": 1632
    },
    "IMC": {
        "1/2": 243, "3/4": 408, "1": 682, "1 1/4": 987, 
        "1 1/2": 1220, "2": 1990
    },
    "RMC": {
        "1/2": 234, "3/4": 387, "1": 638, "1 1/4": 897, 
        "1 1/2": 1038, "2": 1632
    }
}

# Tipos disponibles
aislamientos = ["THW", "XHHW", "THHN"]
tipos_tuberia = ["EMT", "PVC", "IMC", "RMC"]

class CalculadoraTuberias:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cálculos Eléctricos - Hertz Ingeniería & Servicios Eléctricos")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True, True)
        
        # Configurar fuente global compatible
        self.configurar_fuentes_globales()
        
        # Validación adicional para asegurar fuente válida
        if not hasattr(self, 'fuente_principal') or not self.fuente_principal:
            self.fuente_principal = "Arial"
            print("🔧 Validación adicional: forzando Arial")
        
        print(f"🎯 Fuente final confirmada: '{self.fuente_principal}'")
        
        # Configurar fuentes específicas con validación
        self.font_texto = (self.fuente_principal, 10)
        self.font_subtitulo = (self.fuente_principal, 12, "bold")
        self.font_titulo = (self.fuente_principal, 14, "bold")
        
        print(f"📝 Fuentes configuradas:")
        print(f"   - Texto: {self.font_texto}")
        print(f"   - Subtítulo: {self.font_subtitulo}")
        print(f"   - Título: {self.font_titulo}")
        
        # Lista para almacenar conductores agregados
        self.conductores = []
        
        # Variables de estado
        self.ultima_tuberia_recomendada = None
        
        self.crear_interfaz()
        
    def configurar_fuentes_globales(self):
        """Configura fuente global con detección robusta"""
        # Lista de fuentes a probar en orden de preferencia
        fuentes_candidatas = ["Century Gothic", "Calibri", "Segoe UI", "Arial", "Helvetica"]
        fuente_principal = "Arial"  # Valor por defecto seguro
        
        print("🔍 Detectando fuentes disponibles...")
        
        # Obtener lista de fuentes del sistema
        try:
            root_temp = tk.Tk()
            fuentes_sistema = list(font.families())
            root_temp.destroy()
            
            print(f"📋 Fuentes disponibles en el sistema: {len(fuentes_sistema)}")
            
            # Buscar Century Gothic específicamente
            for fuente_disponible in fuentes_sistema:
                if "Century Gothic" in fuente_disponible:
                    fuente_principal = "Century Gothic"
                    print("✅ Century Gothic encontrada y seleccionada")
                    break
            else:
                # Si no se encuentra Century Gothic, usar Arial
                print("⚠️  Century Gothic no encontrada, usando Arial")
                fuente_principal = "Arial"
                
        except Exception as e:
            print(f"❌ Error al detectar fuentes: {e}")
            fuente_principal = "Arial"
        
        # Validación final
        if not isinstance(fuente_principal, str) or len(fuente_principal) == 0:
            fuente_principal = "Arial"
            print("🔧 Fallback final a Arial")
        
        print(f"🎯 Fuente seleccionada: '{fuente_principal}'")
        
        # Establecer fuente por defecto
        try:
            default_font = font.nametofont("TkDefaultFont")
            default_font.configure(family=fuente_principal, size=10)
            self.root.option_add("*Font", f"{fuente_principal} 10")
        except Exception as e:
            print(f"❌ Error al configurar fuente por defecto: {e}")
            fuente_principal = "Arial"
        
        # Configurar estilos TTK
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos específicos con manejo de errores
        try:
            self.style.configure("TCombobox", 
                                fieldbackground="white", 
                                background="white", 
                                font=(fuente_principal, 10))
            
            self.style.configure("Treeview", 
                                font=(fuente_principal, 10))
            
            self.style.configure("Treeview.Heading", 
                                font=(fuente_principal, 10, "bold"))
            
            self.style.configure("TLabelFrame", 
                                font=(fuente_principal, 10, "bold"))
            
            self.style.configure("TLabelFrame.Label", 
                                font=(fuente_principal, 10, "bold"))
        except Exception as e:
            print(f"❌ Error al configurar estilos TTK: {e}")
        
        # Guardar fuente principal para uso en widgets
        self.fuente_principal = fuente_principal
        print(f"💾 self.fuente_principal = '{self.fuente_principal}'")
        
    def crear_interfaz(self):
        # Header con fondo azul oscuro
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Título principal con fuente compatible
        titulo = tk.Label(header_frame, text="SISTEMA DE CÁLCULOS ELÉCTRICOS", 
                         font=(self.fuente_principal, 24, "bold"), bg="#2c3e50", fg="white")
        titulo.pack(pady=(20, 5))
        
        # Subtítulo con fuente compatible
        subtitulo = tk.Label(header_frame, text="NOM-001-SEDE-2012 • Hertz Ingeniería & Servicios Eléctricos S.A de C.V", 
                           font=(self.fuente_principal, 12), bg="#2c3e50", fg="white")
        subtitulo.pack()
        
        # Módulo actual con fuente compatible
        modulo = tk.Label(header_frame, text="CÁLCULO DE TUBERÍAS ELÉCTRICAS", 
                         font=(self.fuente_principal, 14, "bold"), bg="#2c3e50", fg="#3498db")
        modulo.pack(pady=(10, 0))
        
        # Contenedor principal con tres columnas
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurar grid del contenedor principal
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # COLUMNA 1: Datos de Entrada
        self.crear_columna_datos(main_container)
        
        # COLUMNA 2: Resultados del Cálculo
        self.crear_columna_resultados(main_container)
        
        # COLUMNA 3: Información Técnica
        self.crear_columna_info(main_container)
        
    def crear_columna_datos(self, parent):
        # Frame principal de datos con altura fija
        datos_frame = tk.LabelFrame(parent, text="Datos del Cálculo de Tubería", 
                                   font=self.font_subtitulo, bg="white", 
                                   relief="groove", bd=2, padx=15, pady=15)
        datos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        datos_frame.config(height=700)  # Altura fija para evitar colapso
        datos_frame.pack_propagate(False)  # Evitar que se colapse
        
        # Configurar expansión interna
        datos_frame.grid_columnconfigure(0, weight=1)
        
        # Sección de agregar conductores
        conductor_frame = tk.LabelFrame(datos_frame, text="Datos del Conductor", 
                                       font=(self.fuente_principal, 10, "bold"), bg="white")
        conductor_frame.pack(fill="x", pady=(0, 20), padx=10)
        conductor_frame.grid_columnconfigure(1, weight=1)
        
        # Aislamiento
        tk.Label(conductor_frame, text="Aislamiento:", bg="white", 
                font=(self.fuente_principal, 10)).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.cb_aislamiento = ttk.Combobox(conductor_frame, values=aislamientos, 
                                          state="readonly", width=15)
        self.cb_aislamiento.set("THW")
        self.cb_aislamiento.bind("<<ComboboxSelected>>", self.on_aislamiento_change)
        self.cb_aislamiento.grid(row=0, column=1, sticky="ew", padx=10, pady=8)
        
        # Calibre
        tk.Label(conductor_frame, text="Calibre:", bg="white", 
                font=(self.fuente_principal, 10)).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.cb_calibre = ttk.Combobox(conductor_frame, state="readonly", width=15)
        self.cb_calibre.bind("<<ComboboxSelected>>", self.validar_campos)
        self.cb_calibre.grid(row=1, column=1, sticky="ew", padx=10, pady=8)
        
        # Cantidad
        tk.Label(conductor_frame, text="Cantidad:", bg="white", 
                font=(self.fuente_principal, 10)).grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.entry_cantidad = tk.Entry(conductor_frame, width=15, font=(self.fuente_principal, 10))
        self.entry_cantidad.bind("<KeyRelease>", self.validar_campos)
        self.entry_cantidad.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        
        # Botón agregar con esquema de colores profesional
        self.btn_agregar = tk.Button(conductor_frame, text="Agregar Conductor", 
                                    command=self.agregar_conductor, 
                                    bg="#1e3a8a", fg="white",
                                    activebackground="#1e40af", activeforeground="white",
                                    font=(self.fuente_principal, 10, "bold"), 
                                    relief="flat", cursor="hand2", pady=8,
                                    state="disabled")
        self.btn_agregar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=15)
        
        # Separador visual
        ttk.Separator(datos_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Inicializar calibres para THW por defecto
        self.on_aislamiento_change()
        
        # Lista de conductores agregados
        lista_frame = tk.LabelFrame(datos_frame, text="Conductores Agregados", 
                                   font=(self.fuente_principal, 10, "bold"), bg="white")
        lista_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Crear Treeview más compacto
        columns = ("Aisla.", "Calibre", "Cant.", "Área(mm²)")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=4)
        
        # Configurar columnas más pequeñas
        self.tree.heading("Aisla.", text="Aisla.")
        self.tree.heading("Calibre", text="Calibre")
        self.tree.heading("Cant.", text="Cant.")
        self.tree.heading("Área(mm²)", text="Área(mm²)")
        
        self.tree.column("Aisla.", width=60, anchor="center")
        self.tree.column("Calibre", width=60, anchor="center")
        self.tree.column("Cant.", width=50, anchor="center")
        self.tree.column("Área(mm²)", width=80, anchor="center")
        
        self.tree.pack(fill="x", padx=10, pady=10)
        
        # Frame para botones de lista con esquema profesional
        botones_lista_frame = tk.Frame(lista_frame, bg="white")
        botones_lista_frame.pack(fill="x", padx=10, pady=10)
        
        btn_eliminar = tk.Button(botones_lista_frame, text="Eliminar", 
                                command=self.eliminar_conductor, 
                                bg="#ef4444", fg="white",
                                activebackground="#dc2626", activeforeground="white",
                                font=(self.fuente_principal, 9, "bold"), 
                                relief="flat", cursor="hand2", width=10)
        btn_eliminar.pack(side="left", padx=(0, 5))
        
        btn_limpiar = tk.Button(botones_lista_frame, text="Limpiar Todo", 
                               command=self.limpiar_todo, 
                               bg="#6b7280", fg="white",
                               activebackground="#4b5563", activeforeground="white",
                               font=(self.fuente_principal, 9, "bold"), 
                               relief="flat", cursor="hand2", width=10)
        btn_limpiar.pack(side="left", padx=5)
        
        # Separador visual
        ttk.Separator(datos_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Configuración de tubería
        config_frame = tk.LabelFrame(datos_frame, text="Configuración", 
                                    font=(self.fuente_principal, 10, "bold"), bg="white")
        config_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        tk.Label(config_frame, text="Tipo de tubería:", bg="white", 
                font=(self.fuente_principal, 10)).pack(anchor="w", padx=10, pady=(10, 5))
        self.cb_tuberia = ttk.Combobox(config_frame, values=tipos_tuberia, 
                                      state="readonly", width=20)
        self.cb_tuberia.set("EMT")
        self.cb_tuberia.pack(fill="x", padx=10, pady=5)
        
        self.var_auto = tk.BooleanVar(value=True)
        cb_auto = tk.Checkbutton(config_frame, text="Selección automática", 
                                variable=self.var_auto, bg="white", 
                                font=(self.fuente_principal, 10))
        cb_auto.pack(anchor="w", padx=10, pady=(5, 10))
        
        # === BOTÓN CALCULAR - POSICIÓN GARANTIZADA ===
        print("=== CREANDO BOTÓN CALCULAR ===")
        
        # Separador antes del botón
        ttk.Separator(datos_frame, orient='horizontal').pack(fill='x', pady=(10, 15))
        
        # Frame específico para el botón calcular con fondo de color para debug
        calcular_frame = tk.Frame(datos_frame, bg="#f0f0f0", relief="solid", bd=1)
        calcular_frame.pack(fill="x", pady=10, padx=10)
        
        # Etiqueta de debug
        debug_label = tk.Label(calcular_frame, text="ZONA DEL BOTÓN CALCULAR", 
                              bg="#f0f0f0", font=(self.fuente_principal, 8))
        debug_label.pack(pady=2)
        
        # BOTÓN CALCULAR PRINCIPAL
        self.btn_calcular = tk.Button(calcular_frame, 
                                     text="🔧 CALCULAR TUBERÍA", 
                                     command=self.calcular_tuberia, 
                                     bg="#1e3a8a",  # Azul profesional
                                     fg="white",
                                     activebackground="#1e40af", 
                                     activeforeground="white",
                                     font=(self.fuente_principal, 12, "bold"), 
                                     relief="flat", 
                                     cursor="hand2", 
                                     height=2,
                                     state="normal")
        self.btn_calcular.pack(fill="x", padx=5, pady=10)
        
        print("✓ BOTÓN CALCULAR CREADO Y EMPAQUETADO")
        
        # Separador después del botón
        ttk.Separator(datos_frame, orient='horizontal').pack(fill='x', pady=(15, 10))
        
        # Frame para botones adicionales
        botones_frame = tk.Frame(datos_frame, bg="white")
        botones_frame.pack(fill="x", pady=10, padx=10)
        
        # Botón exportar
        btn_exportar = tk.Button(botones_frame, text="📄 Exportar", 
                                command=self.exportar_reporte, 
                                bg="#10b981", fg="white",
                                activebackground="#059669", activeforeground="white",
                                font=(self.fuente_principal, 10, "bold"), 
                                relief="flat", cursor="hand2", pady=8)
        btn_exportar.pack(fill="x", pady=2)
        
        # Botón de regreso
        btn_regreso = tk.Button(botones_frame, text="← REGRESAR AL MENÚ", 
                              command=self.regresar_menu, 
                              bg="#6b7280", fg="white",
                              activebackground="#4b5563", activeforeground="white",
                              font=(self.fuente_principal, 10, "bold"), 
                              relief="flat", cursor="hand2", pady=8)
        btn_regreso.pack(fill="x", pady=2)
        
        # Validar estado inicial del botón calcular
        self.validar_boton_calcular()
        print("=== COLUMNA DATOS COMPLETADA ===")
        
    def crear_columna_resultados(self, parent):
        # Frame de resultados
        resultados_frame = tk.LabelFrame(parent, text="Resultados del Cálculo", 
                                        font=self.font_subtitulo, bg="white",
                                        relief="groove", bd=2, padx=15, pady=15)
        resultados_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        
        # Área de texto para resultados con fuente compatible
        self.text_resultado = tk.Text(resultados_frame, wrap="word", 
                                    font=(self.fuente_principal, 9), bg="#f8f9fa",
                                    relief="sunken", bd=1, padx=10, pady=10)
        self.text_resultado.pack(fill="both", expand=True)
        
        # Scrollbar para resultados
        scrollbar_result = ttk.Scrollbar(resultados_frame, orient="vertical", 
                                        command=self.text_resultado.yview)
        self.text_resultado.configure(yscrollcommand=scrollbar_result.set)
        scrollbar_result.pack(side="right", fill="y")
        
        # Mensaje inicial con mejor formato
        mensaje_inicial = """CALCULADORA DE TUBERÍAS NOM-001-SEDE-2012

INSTRUCCIONES DE USO:
═══════════════════════════════════════════════

1. Seleccione el aislamiento del conductor
2. Escoja el calibre del conductor  
3. Ingrese la cantidad de conductores
4. Presione 'Agregar Conductor'
5. Repita para todos los conductores
6. Seleccione tipo de tubería
7. Presione 'CALCULAR' para obtener resultados

📐 FÓRMULAS PRINCIPALES:
══════════════════════════════════════════════

1. Área total = Σ(Área individual × Cantidad)
2. Área disponible = Área tubería × Factor llenado
3. % Llenado = (Área total / Área tubería) × 100
4. Criterio: Área total ≤ Área disponible

⚡ EJEMPLO RÁPIDO:
═══════════════════════════════════════════════

Problema: ¿Qué tubería EMT necesito para 3 conductores #12 THW?

Solución:
• Área individual #12 THW: 3.31 mm²
• Área total: 3.31 × 3 = 9.93 mm²
• Factor (3 conductores): 53%
• Tubería EMT 1/2": 196 × 0.53 = 103.88 mm²
• Verificación: 9.93 ≤ 103.88 ✓ CUMPLE
• % Llenado: (9.93/196) × 100 = 5.07%
• Resultado: EMT 1/2" es suficiente

CARACTERÍSTICAS DEL SISTEMA:
═══════════════════════════════════════════════

El sistema calculará automáticamente:
• Área total ocupada por conductores
• Factor de llenado según norma
• Tubería recomendada
• Cumplimiento normativo
• Tabla resumen de todas las opciones

Tipos de aislamiento disponibles:
• THW: Resistente al calor y humedad
• XHHW: Resistente al calor, humedad y aceite
• THHN: Nylon termoplástico de alta resistencia

Tipos de tubería disponibles:
• EMT: Electrical Metallic Tubing
• PVC: Cloruro de Polivinilo
• IMC: Intermediate Metal Conduit  
• RMC: Rigid Metal Conduit"""
        
        self.text_resultado.insert(1.0, mensaje_inicial)
        
    def crear_columna_info(self, parent):
        # Frame de información
        info_frame = tk.LabelFrame(parent, text="Información Técnica", 
                                  font=self.font_subtitulo, bg="white",
                                  relief="groove", bd=2, padx=15, pady=15)
        info_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # Información normativa con fuente compatible
        info_text = tk.Text(info_frame, wrap="word", font=(self.fuente_principal, 9), 
                          bg="#ecf0f1", relief="flat", height=20, padx=10, pady=10)
        info_text.pack(fill="both", expand=True)
        
        info_content = """REFERENCIAS NOM-001-SEDE-2012:
══════════════════════════════════════════════

📐 FÓRMULAS DE CÁLCULO:
═══════════════════════════════════════════

1️⃣ ÁREA TOTAL DE CONDUCTORES:
   Área_total = Σ(Área_individual × Cantidad)
   
   Ejemplo: 3 conductores #12 THW
   Área_total = 3.31 mm² × 3 = 9.93 mm²

2️⃣ ÁREA DISPONIBLE EN TUBERÍA:
   Área_disponible = Área_tubería × Factor_llenado
   
   Ejemplo: Tubería EMT 1/2" con 3 conductores
   Área_disponible = 196 mm² × 0.53 = 103.88 mm²

3️⃣ PORCENTAJE DE LLENADO:
   % Llenado = (Área_total / Área_tubería) × 100
   
   Ejemplo: 9.93 mm² en tubería 196 mm²
   % Llenado = (9.93 / 196) × 100 = 5.07%

4️⃣ CRITERIO DE CUMPLIMIENTO:
   CUMPLE si: Área_total ≤ Área_disponible
   
   Verificación: 9.93 mm² ≤ 103.88 mm² ✓ CUMPLE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FACTORES DE LLENADO:
Art. 310-15(b)(2)(A), Tabla 1:
• 1 conductor: 100% (Factor = 1.00)
• 2 conductores: 31% (Factor = 0.31)
• 3+ conductores: 53% (Factor = 0.53)

⚠️ FACTORES DE REDUCCIÓN:
Art. 310-15(b)(2)(a):
• Más de 9 conductores requieren factores
  de reducción adicionales por agrupamiento

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 COMPARATIVA DE AISLAMIENTOS:
THW vs XHHW vs THHN (Conductor #12):
• THW: 3.31 mm² (Mayor área)
• XHHW: 3.12 mm² (Área intermedia)  
• THHN: 2.53 mm² (Menor área, mayor densidad)

📏 CAPACIDADES DE TUBERÍAS:
Área total disponible (mm²):

EMT: 196 - 1809 mm²
PVC: 233 - 1632 mm²
IMC: 243 - 1990 mm²
RMC: 234 - 1632 mm²

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ EJEMPLO COMPLETO:
Calcular tubería para:
- 4 conductores #10 THHN
- Área individual: 4.18 mm²
- Área total: 4.18 × 4 = 16.72 mm²
- Factor (4 conductores): 53%
- Tubería EMT 1/2": 196 × 0.53 = 103.88 mm²
- Verificación: 16.72 ≤ 103.88 ✓ CUMPLE
- % Llenado: (16.72/196) × 100 = 8.53%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PROCESO DE SELECCIÓN:
1. Calcular área total de conductores
2. Determinar factor de llenado (1, 2, 3+ cond.)
3. Evaluar cada tubería disponible
4. Seleccionar menor que cumple criterio
5. Verificar cumplimiento normativo

🚨 CONSIDERACIONES ESPECIALES:
• Temperatura ambiente: 30°C
• Conductores de cobre
• No incluye conductores de tierra
• Para >9 conductores: factores adicionales
• Instalación en ambiente seco

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CRITERIOS DE DECISIÓN:
• Costo vs capacidad
• Facilidad de instalación
• Futuras ampliaciones
• Condiciones ambientales
• Requisitos mecánicos"""
        
        info_text.insert(1.0, info_content)
        info_text.configure(state="disabled")
        
    def on_aislamiento_change(self, event=None):
        """Actualiza los calibres disponibles según el aislamiento seleccionado"""
        aislamiento = self.cb_aislamiento.get()
        if aislamiento in areas_conductores:
            calibres = list(areas_conductores[aislamiento].keys())
            self.cb_calibre.configure(values=calibres)
            self.cb_calibre.set("")  # Limpiar selección
        self.validar_campos()
    
    def validar_campos(self, event=None):
        """Valida que todos los campos estén completos y válidos"""
        try:
            aislamiento = self.cb_aislamiento.get()
            calibre = self.cb_calibre.get()
            cantidad_str = self.entry_cantidad.get().strip()
            
            # Validar que hay aislamiento y calibre
            if not aislamiento or not calibre:
                self.btn_agregar.configure(state="disabled")
                return
            
            # Validar cantidad
            if not cantidad_str:
                self.btn_agregar.configure(state="disabled")
                return
            
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                self.btn_agregar.configure(state="disabled")
                return
            
            # Si todo es válido, habilitar botón
            self.btn_agregar.configure(state="normal")
            
        except ValueError:
            self.btn_agregar.configure(state="disabled")
    
    def validar_boton_calcular(self):
        """Habilita el botón calcular solo si hay conductores agregados"""
        # Verificar que el botón exista antes de intentar modificarlo
        if not hasattr(self, 'btn_calcular'):
            print("ERROR: btn_calcular no existe aún")
            return
        
        cantidad_conductores = len(self.conductores)
        print(f"Validando botón calcular. Conductores: {cantidad_conductores}")
        
        if cantidad_conductores > 0:
            self.btn_calcular.configure(state="normal", bg="#1e3a8a")
            print(f"Botón CALCULAR habilitado - {cantidad_conductores} conductores")
        else:
            self.btn_calcular.configure(state="normal", bg="#6b7280")  # Gris cuando no hay conductores
            print("Botón CALCULAR visible pero sin conductores")
    
    def agregar_conductor(self):
        try:
            aislamiento = self.cb_aislamiento.get()
            calibre = self.cb_calibre.get()
            cantidad = int(self.entry_cantidad.get())
            
            if not aislamiento or not calibre:
                messagebox.showerror("Error", "Seleccione aislamiento y calibre")
                return
            
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            # Obtener área unitaria
            area_unitaria = areas_conductores[aislamiento].get(calibre, 0)
            area_total = area_unitaria * cantidad
            
            # Agregar a la lista
            conductor = {
                "aislamiento": aislamiento,
                "calibre": calibre,
                "cantidad": cantidad,
                "area_unitaria": area_unitaria,
                "area_total": area_total
            }
            
            self.conductores.append(conductor)
            
            # Agregar al Treeview
            self.tree.insert("", "end", values=(
                aislamiento, calibre, cantidad, f"{area_total:.1f}"
            ))
            
            # Limpiar entrada
            self.cb_calibre.set("")
            self.entry_cantidad.delete(0, tk.END)
            
            # Validar estado de botones
            self.validar_campos()  # Para el botón agregar
            self.validar_boton_calcular()  # Para el botón calcular
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")
    
    def eliminar_conductor(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un conductor para eliminar")
            return
        
        # Obtener índice del elemento seleccionado
        index = self.tree.index(selection[0])
        
        # Eliminar de la lista y del Treeview
        del self.conductores[index]
        self.tree.delete(selection[0])
        
        # Validar estado del botón calcular
        self.validar_boton_calcular()
    
    def limpiar_todo(self):
        """Limpia todos los conductores agregados"""
        if messagebox.askyesno("Confirmar", "¿Desea limpiar todos los conductores?"):
            self.conductores.clear()
            # Limpiar Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Validar estado de botones
            self.validar_boton_calcular()
            
            # Limpiar área de resultados con formato mejorado
            self.text_resultado.delete(1.0, tk.END)
            mensaje_inicial = """CONDUCTORES ELIMINADOS

═══════════════════════════════════════════════

Todos los conductores han sido eliminados de la lista.

Para continuar:
1. Agregue nuevos conductores usando el formulario
2. Complete todos los campos requeridos
3. Presione 'Agregar Conductor'
4. Repita para todos los conductores necesarios
5. Presione 'CALCULAR' para obtener resultados

El sistema está listo para un nuevo cálculo."""
            self.text_resultado.insert(1.0, mensaje_inicial)
    
    def calcular_area_total(self):
        total = 0
        for conductor in self.conductores:
            total += conductor["area_total"]
        return total
    
    def obtener_limite_norma(self, cantidad_total):
        if cantidad_total == 1:
            return 1.00
        elif cantidad_total == 2:
            return 0.31
        else:
            return 0.53
    
    def verificar_factores_reduccion(self, cantidad_total):
        """Verifica si se requieren factores de reducción adicionales"""
        if cantidad_total > 9:
            return True, "Se requieren factores de reducción por más de 9 conductores"
        return False, ""
    
    def calcular_tuberia(self):
        if not self.conductores:
            messagebox.showwarning("Advertencia", "Agregue al menos un conductor")
            return
        
        # Calcular área total
        area_total = self.calcular_area_total()
        cantidad_total = sum(c["cantidad"] for c in self.conductores)
        
        # Obtener límite según norma y tipo de tubería
        limite = self.obtener_limite_norma(cantidad_total)
        tipo_tuberia = self.cb_tuberia.get()
        
        # Verificar factores de reducción adicionales
        requiere_reduccion, mensaje_reduccion = self.verificar_factores_reduccion(cantidad_total)
        
        resultado = f"REPORTE DE CÁLCULO DE TUBERÍA {tipo_tuberia}\n"
        resultado += f"NOM-001-SEDE-2012\n"
        resultado += f"{'='*55}\n"
        resultado += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        resultado += f"CONDUCTORES EN EL CÁLCULO:\n"
        resultado += f"{'-'*35}\n"
        for i, c in enumerate(self.conductores, 1):
            resultado += f"{i}. {c['aislamiento']} #{c['calibre']} × {c['cantidad']} conductor(es)\n"
            resultado += f"   Área: {c['area_unitaria']:.2f} mm² × {c['cantidad']} = {c['area_total']:.2f} mm²\n\n"
        
        resultado += f"RESUMEN DEL CÁLCULO:\n"
        resultado += f"{'-'*25}\n"
        resultado += f"• Total de conductores: {cantidad_total}\n"
        resultado += f"• Área total requerida: {area_total:.2f} mm²\n"
        resultado += f"• Factor de llenado NOM: {limite*100:.0f}%\n"
        
        # Agregar fórmulas utilizadas
        resultado += f"\n📐 FÓRMULAS APLICADAS:\n"
        resultado += f"{'-'*25}\n"
        resultado += f"1. Área total = Σ(Área individual × Cantidad)\n"
        if len(self.conductores) > 1:
            formula_detalle = " + ".join([f"({c['area_unitaria']:.2f} × {c['cantidad']})" for c in self.conductores])
            resultado += f"   = {formula_detalle} = {area_total:.2f} mm²\n"
        else:
            c = self.conductores[0]
            resultado += f"   = {c['area_unitaria']:.2f} × {c['cantidad']} = {area_total:.2f} mm²\n"
        
        resultado += f"\n2. Área disponible = Área tubería × Factor ({limite:.2f})\n"
        resultado += f"3. % Llenado = (Área total / Área tubería) × 100\n"
        resultado += f"4. Criterio: Área total ≤ Área disponible\n"
        
        # Agregar referencia normativa exacta
        if cantidad_total == 1:
            resultado += f"\n• Referencia: Art. 310-15(b)(2)(A), Tabla 1 - NOM-001-SEDE-2012\n"
            resultado += f"  (Un conductor: 100% del área de tubería)\n"
        elif cantidad_total == 2:
            resultado += f"\n• Referencia: Art. 310-15(b)(2)(A), Tabla 1 - NOM-001-SEDE-2012\n"
            resultado += f"  (Dos conductores: 31% del área de tubería)\n"
        else:
            resultado += f"\n• Referencia: Art. 310-15(b)(2)(A), Tabla 1 - NOM-001-SEDE-2012\n"
            resultado += f"  (Tres o más conductores: 53% del área de tubería)\n"
        
        # Advertencia para más de 9 conductores
        if requiere_reduccion:
            resultado += f"\n⚠️  ADVERTENCIA NORMATIVA:\n"
            resultado += f"   {mensaje_reduccion}\n"
            resultado += f"   Consulte Art. 310-15(b)(2)(a) para factores\n"
            resultado += f"   de reducción por agrupamiento.\n"
        
        resultado += f"\n"
        
        if self.var_auto.get():
            resultado += f"ANÁLISIS DE TUBERÍAS {tipo_tuberia}:\n"
            resultado += f"{'-'*35}\n"
            
            tuberia_seleccionada = None
            tuberias_que_cumplen = []
            tabla_resumen = []
            
            for diametro, area_total_tub in tabla_tuberias[tipo_tuberia].items():
                area_disponible = area_total_tub * limite
                porcentaje_llenado = (area_total / area_total_tub) * 100
                
                resultado += f"{tipo_tuberia} {diametro}\":\n"
                resultado += f"  Área total: {area_total_tub:.0f} mm²\n"
                resultado += f"  Área disponible: {area_disponible:.0f} mm² ({limite*100:.0f}%)\n"
                resultado += f"  Cálculo: {area_total_tub:.0f} × {limite:.2f} = {area_disponible:.0f} mm²\n"
                resultado += f"  Llenado actual: {porcentaje_llenado:.1f}%\n"
                resultado += f"  Cálculo: ({area_total:.1f}/{area_total_tub:.0f}) × 100 = {porcentaje_llenado:.1f}%\n"
                
                if area_total <= area_disponible:
                    estado = "✓ CUMPLE"
                    resultado += f"  Estado: {estado}\n\n"
                    tuberias_que_cumplen.append((diametro, area_total_tub, porcentaje_llenado))
                    if tuberia_seleccionada is None:
                        tuberia_seleccionada = (diametro, area_total_tub, porcentaje_llenado)
                else:
                    estado = "✗ NO CUMPLE"
                    resultado += f"  Estado: {estado} (excede factor de llenado)\n\n"
                
                # Agregar a tabla resumen
                tabla_resumen.append({
                    'diametro': diametro,
                    'area_total': area_total_tub,
                    'area_disponible': area_disponible,
                    'porcentaje': porcentaje_llenado,
                    'estado': estado
                })
            
            # TABLA RESUMEN
            resultado += f"TABLA RESUMEN - TUBERÍAS {tipo_tuberia}:\n"
            resultado += f"{'='*60}\n"
            resultado += f"{'Diámetro':<10} {'Área Total':<12} {'Disponible':<12} {'Llenado':<10} {'Estado':<15}\n"
            resultado += f"{'-'*60}\n"
            for tuberia in tabla_resumen:
                resultado += f"{tuberia['diametro']:<10} {tuberia['area_total']:.0f} mm²{'':<4} {tuberia['area_disponible']:.0f} mm²{'':<4} {tuberia['porcentaje']:.1f}%{'':<6} {tuberia['estado']:<15}\n"
            resultado += f"{'='*60}\n\n"
            
            resultado += f"RESULTADO FINAL:\n"
            resultado += f"{'-'*20}\n"
            if tuberia_seleccionada:
                diametro, area_tub, porcentaje = tuberia_seleccionada
                area_disponible_rec = area_tub * limite
                
                # Formato mejorado de recomendación
                resultado += f"🎯 TUBERÍA RECOMENDADA: {tipo_tuberia} {diametro}\"\n"
                resultado += f"   • Área total: {area_tub:.0f} mm²\n"
                resultado += f"   • Disponible: {area_disponible_rec:.0f} mm² (Factor {limite:.2f})\n"
                resultado += f"   • Llenado: {porcentaje:.1f}%\n"
                resultado += f"   • Estado: ✓ CUMPLE NOM-001-SEDE-2012\n\n"
                
                if len(tuberias_que_cumplen) > 1:
                    resultado += f"ALTERNATIVAS VÁLIDAS:\n"
                    for i, (diam, area, porc) in enumerate(tuberias_que_cumplen[1:], 2):
                        area_disp_alt = area * limite
                        resultado += f"   {i}. {tipo_tuberia} {diam}\" • Área: {area:.0f} mm² • Disponible: {area_disp_alt:.0f} mm² • Llenado: {porc:.1f}% • ✓ CUMPLE\n"
                    resultado += f"\n"
                
                resultado += f"ESPECIFICACIÓN TÉCNICA:\n"
                resultado += f"Instalar tubería conduit {tipo_tuberia} de {diametro}\" \n"
                resultado += f"conforme al Art. 310-15(b)(2)(A), Tabla 1 - NOM-001-SEDE-2012.\n"
                
                if requiere_reduccion:
                    resultado += f"\nNOTA IMPORTANTE:\n"
                    resultado += f"Verificar factores de reducción adicionales por\n"
                    resultado += f"agrupamiento de conductores (Art. 310-15(b)(2)(a))."
                
                self.ultima_tuberia_recomendada = f"{tipo_tuberia} {diametro}\""
                
                # Agregar indicador visual de cumplimiento
                self.mostrar_estado_cumplimiento("✓ CUMPLE", "#10b981")
            else:
                resultado += f"⚠️ ADVERTENCIA CRÍTICA:\n"
                resultado += f"   Ninguna tubería {tipo_tuberia} estándar cumple con la norma\n"
                resultado += f"   RECOMENDACIONES:\n"
                resultado += f"   • Usar tubería de mayor capacidad\n"
                resultado += f"   • Reducir número de conductores\n"
                resultado += f"   • Cambiar tipo de aislamiento (menor área)\n"
                resultado += f"   • Distribuir en múltiples tuberías\n"
                self.ultima_tuberia_recomendada = "NINGUNA CUMPLE"
                
                # Agregar indicador visual de no cumplimiento
                self.mostrar_estado_cumplimiento("✗ NO CUMPLE", "#ef4444")
                
                # Mostrar alerta
                messagebox.showwarning("Advertencia", 
                                     f"Ninguna tubería {tipo_tuberia} cumple con los requisitos.\n"
                                     f"Consulte las recomendaciones en el reporte.")
        
        # Mostrar resultado
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(1.0, resultado)
    
    def mostrar_estado_cumplimiento(self, texto, color):
        """Muestra un indicador visual del estado de cumplimiento"""
        # Crear o actualizar etiqueta de estado
        if hasattr(self, 'label_estado'):
            self.label_estado.destroy()
        
        # Encontrar el frame de resultados para agregar la etiqueta
        resultado_frame = self.text_resultado.master
        self.label_estado = tk.Label(resultado_frame, text=texto, 
                                   fg="white", bg=color,
                                   font=(self.fuente_principal, 12, "bold"),
                                   relief="flat", pady=10)
        self.label_estado.pack(side="bottom", fill="x", padx=10, pady=5)
    
    def exportar_reporte(self):
        """Exporta el reporte actual a un archivo de texto"""
        if not self.conductores:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Exportar Reporte de Cálculo"
            )
            
            if filename:
                contenido = self.text_resultado.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(contenido)
                messagebox.showinfo("Éxito", f"Reporte exportado exitosamente:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def regresar_menu(self):
        """Función para regresar al menú principal"""
        try:
            self.root.destroy()
            # Intentar ejecutar calculosint.py
            subprocess.run([sys.executable, "calculosint.py"], check=True)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo calculosint.py")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Error al ejecutar calculosint.py")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

def main():
    root = tk.Tk()
    app = CalculadoraTuberias(root)
    root.mainloop()

if __name__ == "__main__":
    main()