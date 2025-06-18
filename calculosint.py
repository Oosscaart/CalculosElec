import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

class Calculos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cálculos Eléctricos - Hertz Ingeniería & Servicios Eléctricos")
     
        self.root.state('zoomed')  

        self.root.resizable(True, True)
        
       
        self.root.bind('<Escape>', self.cerrar_aplicacion)
        self.root.bind('<Alt-F4>', self.cerrar_aplicacion)
        
      
        self.font_normal = ('Century Gothic', 10)
        self.font_bold = ('Century Gothic', 10, 'bold')
        self.font_title = ('Century Gothic', 12, 'bold')
        self.font_subtitle = ('Century Gothic', 11, 'bold')
        self.font_small = ('Century Gothic', 9)
        self.font_mono = ('Courier New', 9)
        
        self.root.configure(bg='#f0f0f0')
        
   
        self.ampacidades_cobre_75 = {
            "14": 20, "12": 25, "10": 35, "8": 50, "6": 65,
            "4": 85, "3": 100, "2": 115, "1": 130,
            "1/0": 150, "2/0": 175, "3/0": 200, "4/0": 230,
            "250": 255, "300": 285, "350": 310, "400": 335,
            "500": 380, "600": 420, "750": 475, "1000": 545,
            "1250": 590, "1500": 625, "1750": 650, "2000": 665
        }

        self.ampacidades_cobre_60 = {
            "14": 15, "12": 20, "10": 30, "8": 40, "6": 55,
            "4": 70, "3": 85, "2": 95, "1": 110,
            "1/0": 125, "2/0": 145, "3/0": 165, "4/0": 195,
            "250": 215, "300": 240, "350": 260, "400": 280,
            "500": 320, "600": 355, "750": 400, "1000": 455,
            "1250": 495, "1500": 520, "1750": 545, "2000": 560
        }

        self.ampacidades_cobre_90 = {
            "14": 25, "12": 30, "10": 40, "8": 55, "6": 75,
            "4": 95, "3": 110, "2": 130, "1": 150,
            "1/0": 170, "2/0": 195, "3/0": 225, "4/0": 260,
            "250": 290, "300": 320, "350": 350, "400": 380,
            "500": 430, "600": 475, "750": 535, "1000": 615,
            "1250": 665, "1500": 700, "1750": 735, "2000": 750
        }

        self.ampacidades_aluminio = {
            "12": 20, "10": 25, "8": 30, "6": 40, "4": 55, "3": 65, 
            "2": 75, "1": 85, "1/0": 100, "2/0": 115, "3/0": 130, 
            "4/0": 150, "250": 170, "300": 190, "350": 210, 
            "400": 225, "500": 260, "600": 285, "750": 320, "1000": 375,
            "1250": 405, "1500": 435, "1750": 455, "2000": 470
        }
        
        self.ampacidades_charola_cobre_75 = {
            "8": 57, "6": 76, "4": 101, "3": 118, "2": 135, "1": 158,
            "1/0": 183, "2/0": 212, "3/0": 245, "4/0": 287,
            "250": 320, "300": 359, "350": 397, "400": 430,
            "500": 496, "600": 553, "700": 610, "750": 638,
            "800": 660, "900": 704, "1000": 750, "1250": 834,
            "1500": 909, "1750": 980, "2000": 1042
        }
        
        self.ampacidades_charola_cobre_90 = {
            "8": 66, "6": 89, "4": 117, "3": 138, "2": 158, "1": 185,
            "1/0": 214, "2/0": 247, "3/0": 287, "4/0": 335,
            "250": 374, "300": 419, "350": 464, "400": 503,
            "500": 580, "600": 647, "700": 714, "750": 747,
            "800": 773, "900": 826, "1000": 877, "1250": 975,
            "1500": 1063, "1750": 1146, "2000": 1219
        }
        
        self.ampacidades_charola_aluminio_75 = {
            "6": 59, "4": 78, "3": 92, "2": 106, "1": 123,
            "1/0": 143, "2/0": 165, "3/0": 192, "4/0": 224,
            "250": 251, "300": 282, "350": 312, "400": 339,
            "500": 392, "600": 440, "700": 488, "750": 512,
            "800": 532, "900": 568, "1000": 603, "1250": 669,
            "1500": 729, "1750": 787, "2000": 837
        }
        
        self.ampacidades_charola_aluminio_90 = {
            "6": 69, "4": 91, "3": 107, "2": 123, "1": 144,
            "1/0": 167, "2/0": 193, "3/0": 224, "4/0": 262,
            "250": 292, "300": 328, "350": 364, "400": 395,
            "500": 458, "600": 514, "700": 570, "750": 598,
            "800": 622, "900": 664, "1000": 705, "1250": 782,
            "1500": 852, "1750": 920, "2000": 979
        }

        self.calibre_tierra_fisica = {
            15: "14", 20: "12", 30: "10", 40: "10", 60: "10", 
            100: "8", 200: "6", 300: "4", 400: "3", 600: "2", 
            800: "1/0", 1000: "1/0", 1200: "2/0", 1600: "3/0", 
            2000: "4/0", 2500: "250", 3000: "250", 4000: "350", 
            5000: "400", 6000: "500"
        }

        self.historial = []
        
        self.interruptores_comerciales = [
            15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 125, 150, 
            175, 200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800, 
            1000, 1200, 1600, 2000, 2500, 3000, 4000, 5000, 6000
        ]

        self.impedancia_cobre = {
            "PVC": {
                "14": 8.9, "12": 5.6, "10": 3.6, "8": 2.26, "6": 1.44,
                "4": 0.95, "3": 0.75, "2": 0.62, "1": 0.52,
                "1/0": 0.43, "2/0": 0.36, "3/0": 0.29, "4/0": 0.24,
                "250": 0.217, "300": 0.194, "350": 0.174, "400": 0.161,
                "500": 0.141, "600": 0.131, "750": 0.118, "1000": 0.105,
                "1250": 0.094, "1500": 0.087, "1750": 0.082, "2000": 0.079
            },
            "Aluminio": {
                "14": 9.1, "12": 5.7, "10": 3.7, "8": 2.32, "6": 1.48,
                "4": 0.97, "3": 0.79, "2": 0.64, "1": 0.54,
                "1/0": 0.44, "2/0": 0.37, "3/0": 0.302, "4/0": 0.256,
                "250": 0.23, "300": 0.207, "350": 0.19, "400": 0.174,
                "500": 0.157, "600": 0.144, "750": 0.131, "1000": 0.118,
                "1250": 0.108, "1500": 0.101, "1750": 0.096, "2000": 0.093
            },
            "Acero": {
                "14": 9.3, "12": 5.9, "10": 3.8, "8": 2.38, "6": 1.52,
                "4": 1.01, "3": 0.82, "2": 0.68, "1": 0.56,
                "1/0": 0.46, "2/0": 0.39, "3/0": 0.315, "4/0": 0.268,
                "250": 0.24, "300": 0.213, "350": 0.197, "400": 0.184,
                "500": 0.164, "600": 0.154, "750": 0.141, "1000": 0.131,
                "1250": 0.124, "1500": 0.119, "1750": 0.116, "2000": 0.114
            }
        }

        self.impedancia_aluminio = {
            "PVC": {
                "12": 5.6, "10": 3.6, "8": 2.26, "6": 1.54,
                "4": 0.95, "3": 0.82, "2": 0.66, "1": 0.56,
                "1/0": 0.48, "2/0": 0.40, "3/0": 0.34, "4/0": 0.29,
                "250": 0.263, "300": 0.239, "350": 0.219, "400": 0.204,
                "500": 0.183, "600": 0.170, "750": 0.156, "1000": 0.140,
                "1250": 0.131, "1500": 0.125, "1750": 0.121, "2000": 0.119
            },
            "Aluminio": {
                "12": 5.7, "10": 3.7, "8": 2.32, "6": 1.58,
                "4": 0.98, "3": 0.85, "2": 0.68, "1": 0.58,
                "1/0": 0.50, "2/0": 0.42, "3/0": 0.35, "4/0": 0.30,
                "250": 0.270, "300": 0.245, "350": 0.225, "400": 0.210,
                "500": 0.188, "600": 0.175, "750": 0.161, "1000": 0.145,
                "1250": 0.136, "1500": 0.130, "1750": 0.126, "2000": 0.124
            },
            "Acero": {
                "12": 5.9, "10": 3.8, "8": 2.38, "6": 1.62,
                "4": 1.02, "3": 0.88, "2": 0.72, "1": 0.61,
                "1/0": 0.53, "2/0": 0.44, "3/0": 0.37, "4/0": 0.32,
                "250": 0.278, "300": 0.252, "350": 0.232, "400": 0.218,
                "500": 0.195, "600": 0.185, "750": 0.173, "1000": 0.156,
                "1250": 0.148, "1500": 0.143, "1750": 0.140, "2000": 0.138
            }
        }
        
        self.impedancia_charola_cobre = {
            "8": 2.0, "6": 1.3, "4": 0.85, "3": 0.68, "2": 0.56, "1": 0.47,
            "1/0": 0.39, "2/0": 0.33, "3/0": 0.26, "4/0": 0.22,
            "250": 0.195, "300": 0.175, "350": 0.157, "400": 0.145,
            "500": 0.127, "600": 0.118, "700": 0.109, "750": 0.106,
            "800": 0.103, "900": 0.098, "1000": 0.095, "1250": 0.085,
            "1500": 0.078, "1750": 0.074, "2000": 0.071
        }
        
        self.impedancia_charola_aluminio = {
            "6": 1.42, "4": 0.88, "3": 0.74, "2": 0.60, "1": 0.51,
            "1/0": 0.44, "2/0": 0.37, "3/0": 0.31, "4/0": 0.26,
            "250": 0.238, "300": 0.216, "350": 0.198, "400": 0.185,
            "500": 0.165, "600": 0.153, "700": 0.141, "750": 0.138,
            "800": 0.135, "900": 0.129, "1000": 0.126, "1250": 0.115,
            "1500": 0.108, "1750": 0.103, "2000": 0.100
        }
        
        self.setup_ui()
    
    def setup_ui(self):
       
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
      
        archivo_menu = tk.Menu(menubar, tearoff=0, font=self.font_normal)
        menubar.add_cascade(label="Archivo", menu=archivo_menu, font=self.font_normal)
        archivo_menu.add_command(label="Exportar a PDF", command=self.exportar_a_pdf)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir (Esc)", command=self.cerrar_aplicacion)
        
       
        herramientas_menu = tk.Menu(menubar, tearoff=0, font=self.font_normal)
        menubar.add_cascade(label="Herramientas", menu=herramientas_menu, font=self.font_normal)
        herramientas_menu.add_command(label="Limpiar campos", command=self.limpiar_campos)
        herramientas_menu.add_command(label="Limpiar historial", command=self.limpiar_historial)
        
       
        ayuda_menu = tk.Menu(menubar, tearoff=0, font=self.font_normal)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu, font=self.font_normal)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        
       
        title_frame = tk.Frame(self.root, bg='#2c3e50', pady=20)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="SISTEMA DE CÁLCULOS ELÉCTRICOS", 
                              font=self.font_title, fg='white', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="NOM-001-SEDE-2012 • Hertz Ingeniería & Servicios Eléctricos S.A de C.V", 
                                 font=self.font_normal, fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()

        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
    
        main_frame.grid_columnconfigure(0, weight=2, minsize=400)
        main_frame.grid_columnconfigure(1, weight=3, minsize=500)
        main_frame.grid_columnconfigure(2, weight=2, minsize=350)
        main_frame.grid_rowconfigure(0, weight=1)
        
        
        left_frame = tk.Frame(main_frame, bg='#f0f0f0')
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
     
        form_main_frame = tk.LabelFrame(left_frame, text="Datos del Circuito Eléctrico", 
                                       font=self.font_subtitle, bg='#f0f0f0', fg='#2c3e50', 
                                       padx=15, pady=15)
        form_main_frame.pack(fill='both', expand=True, pady=(0, 15))
      
        self.setup_formulario_principal(form_main_frame)

        
        center_frame = tk.Frame(main_frame, bg='#f0f0f0')
        center_frame.grid(row=0, column=1, sticky='nsew', padx=10)
        
        
        self.resultado_frame = tk.LabelFrame(center_frame, text="Resultados del Cálculo", 
                                           font=self.font_subtitle, bg='#f0f0f0', fg='#2c3e50', 
                                           padx=15, pady=15)
        self.resultado_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        resultado_text_frame = tk.Frame(self.resultado_frame)
        resultado_text_frame.pack(fill='both', expand=True)
        
        self.resultado_text = tk.Text(resultado_text_frame, font=self.font_mono, 
                                    bg='white', wrap=tk.WORD, state='disabled',
                                    relief='sunken', bd=2)
        resultado_scrollbar = tk.Scrollbar(resultado_text_frame, command=self.resultado_text.yview)
        self.resultado_text.config(yscrollcommand=resultado_scrollbar.set)
        
        self.resultado_text.pack(side='left', fill='both', expand=True)
        resultado_scrollbar.pack(side='right', fill='y')
        
       
        self.info_normativa_frame = tk.LabelFrame(center_frame, text="Información Normativa", 
                                                font=self.font_subtitle, bg='#f0f0f0', fg='#2c3e50',
                                                padx=10, pady=10)
        self.info_normativa_frame.pack(fill='both', expand=True)
        
      
        canvas_normativa = tk.Canvas(self.info_normativa_frame, bg='#f0f0f0', height=150)
        scrollbar_normativa = tk.Scrollbar(self.info_normativa_frame, orient="vertical", command=canvas_normativa.yview)
        scrollable_normativa = tk.Frame(canvas_normativa, bg='#f0f0f0')
        
        scrollable_normativa.bind(
            "<Configure>",
            lambda e: canvas_normativa.configure(scrollregion=canvas_normativa.bbox("all"))
        )
        
        canvas_normativa.create_window((0, 0), window=scrollable_normativa, anchor="nw")
        canvas_normativa.configure(yscrollcommand=scrollbar_normativa.set)
        
      
        def _on_mousewheel(event):
            canvas_normativa.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas_normativa.bind("<MouseWheel>", _on_mousewheel)
        
        canvas_normativa.pack(side="left", fill="both", expand=True)
        scrollbar_normativa.pack(side="right", fill="y")
        
        
        tipo_frame = tk.Frame(scrollable_normativa, bg='#e3f2fd', relief='raised', bd=1)
        tipo_frame.pack(fill='x', pady=(0, 10), padx=5)
        
        tk.Label(tipo_frame, text="TIPO DE CARGA:", font=self.font_bold, 
                bg='#e3f2fd', fg='#1976d2').pack(anchor='w', padx=5, pady=2)
        self.tipo_carga_label = tk.Label(tipo_frame, text="-", font=self.font_normal, 
                                       bg='#e3f2fd', fg='#424242')
        self.tipo_carga_label.pack(anchor='w', padx=15)
        
        tk.Label(tipo_frame, text="TIPO DE INSTALACIÓN:", font=self.font_bold, 
                bg='#e3f2fd', fg='#1976d2').pack(anchor='w', padx=5, pady=2)
        self.tipo_instalacion_label = tk.Label(tipo_frame, text="-", font=self.font_normal, 
                                             bg='#e3f2fd', fg='#424242')
        self.tipo_instalacion_label.pack(anchor='w', padx=15)
        
        tk.Label(tipo_frame, text="AISLAMIENTO DEL CONDUCTOR:", font=self.font_bold, 
                bg='#e3f2fd', fg='#1976d2').pack(anchor='w', padx=5, pady=2)
        tk.Label(tipo_frame, text="THW (75 °C)", font=self.font_normal, 
                bg='#e3f2fd', fg='#424242').pack(anchor='w', padx=15, pady=(0, 5))
        
     
        normativa_aplicada_frame = tk.Frame(scrollable_normativa, bg='#fff3e0', relief='raised', bd=1)
        normativa_aplicada_frame.pack(fill='x', pady=(0, 10), padx=5)
        
        tk.Label(normativa_aplicada_frame, text="NORMATIVA APLICADA:", font=self.font_bold, 
                bg='#fff3e0', fg='#e65100').pack(anchor='w', padx=5, pady=2)
        
        normativa_text = """• Art. 450-3: Protección de transformadores (125% I)
• Art. 250-122: Selección de tierra física con base en el interruptor
• Tabla 310-15(b)(16): Ampacidades a 75 °C
• Tabla de impedancias por tipo de canalización y material conductor
• Art. 430-22: Protección de motores (125% I)
• Art. 460-8: Protección de capacitores (135% I)
• Art. 445-5: Protección de generadores (115% I)
• Art. 210-19 FPN 4: Caída máx 3% circuitos derivados
• Art. 215-2 FPN 2: Caída máx 2% alimentadores
• Art. 220-11: Factores de demanda para alimentadores
• Art. 240-12: Coordinación selectiva de protecciones"""
        
        tk.Label(normativa_aplicada_frame, text=normativa_text, font=self.font_small, 
                bg='#fff3e0', fg='#424242', justify='left').pack(anchor='w', padx=15, pady=(0, 5))
        
  
        leyenda_normativa_frame = tk.Frame(scrollable_normativa, bg='#f3e5f5', relief='raised', bd=1)
        leyenda_normativa_frame.pack(fill='x', padx=5)
        
        tk.Label(leyenda_normativa_frame, text="LEYENDA METODOLÓGICA:", font=self.font_bold, 
                bg='#f3e5f5', fg='#4a148c').pack(anchor='w', padx=5, pady=2)
        
        leyenda_text = """• La corriente por conductor se basa en el interruptor (I / n)
• El calibre se selecciona por ampacidad ≥ corriente por conductor
• La caída de tensión se calcula con impedancia según canalización y material
• La tierra física se selecciona según interruptor (Art. 250-122)
• Metodología: Corriente → Factor → Interruptor → Calibre
• Alimentadores: Factores de demanda según Art. 220-11 aplicados
• Derivados: Sin factores de demanda (carga completa)
• Límites caída: 2% alimentadores, 3% derivados"""
        
        tk.Label(leyenda_normativa_frame, text=leyenda_text, font=self.font_small, 
                bg='#f3e5f5', fg='#424242', justify='left').pack(anchor='w', padx=15, pady=(0, 5))

        
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.grid(row=0, column=2, sticky='nsew', padx=(10, 0))
        
        historial_frame = tk.LabelFrame(right_frame, text="Historial y Referencias", 
                                       font=self.font_subtitle, bg='#f0f0f0', fg='#2c3e50', 
                                       padx=10, pady=10)
        historial_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        historial_text_frame = tk.Frame(historial_frame)
        historial_text_frame.pack(fill='both', expand=True)
        
        self.historial_text = tk.Text(historial_text_frame, font=self.font_small, 
                                    bg='#f8f9fa', wrap=tk.WORD, state='disabled',
                                    relief='sunken', bd=2)
        historial_scrollbar = tk.Scrollbar(historial_text_frame, command=self.historial_text.yview)
        self.historial_text.config(yscrollcommand=historial_scrollbar.set)
        
        self.historial_text.pack(side='left', fill='both', expand=True)
        historial_scrollbar.pack(side='right', fill='y')
        
       
        historial_btn_frame = tk.Frame(historial_frame, bg='#f0f0f0')
        historial_btn_frame.pack(fill='x', pady=(10, 0))
        
        limpiar_historial_btn = tk.Button(historial_btn_frame, text="Limpiar Historial", 
                                        command=self.limpiar_historial, font=self.font_normal,
                                        bg='#e74c3c', fg='white', relief='raised', bd=2,
                                        cursor='hand2')
        limpiar_historial_btn.pack(fill='x')
        
        
        servicios_frame = tk.LabelFrame(right_frame, text="Servicios Adicionales", 
                                       font=self.font_subtitle, bg='#f0f0f0', fg='#2c3e50',
                                       padx=10, pady=10)
        servicios_frame.pack(fill='x')
        
       
        exportar_btn = tk.Button(servicios_frame, text="📄 Memoria Técnica PDF", 
                                command=self.exportar_a_pdf, font=self.font_normal,
                                bg='#e74c3c', fg='white', relief='raised', bd=2,
                                cursor='hand2')
        exportar_btn.pack(fill='x')
        
        
        self.actualizar_historial_completo()
        self.mostrar_normativa_inicial()

    def setup_formulario_principal(self, parent):
        
        form_frame = tk.LabelFrame(parent, text="Datos del Circuito Eléctrico", font=self.font_subtitle, 
                                  bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        form_frame.pack(fill='both', expand=True, pady=(0, 10))

       
        tk.Label(form_frame, text="Tipo de circuito:", font=self.font_bold, bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        self.tipo_circuito_var = tk.StringVar(value="monofasico")
        tipo_circuito_frame = tk.Frame(form_frame, bg='#f0f0f0')
        tipo_circuito_frame.grid(row=0, column=1, sticky='w', pady=5)
        tk.Radiobutton(tipo_circuito_frame, text="Monofásico", variable=self.tipo_circuito_var, 
                      value="monofasico", bg='#f0f0f0', font=self.font_normal,
                      command=self.actualizar_campos_equipo).pack(side='left')
        tk.Radiobutton(tipo_circuito_frame, text="Trifásico", variable=self.tipo_circuito_var, 
                      value="trifasico", bg='#f0f0f0', font=self.font_normal,
                      command=self.actualizar_campos_equipo).pack(side='left')
      
        tk.Label(form_frame, text="Tipo de carga:", font=self.font_bold, bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.tipo_carga_var = tk.StringVar(value="derivado")
        tipo_carga_frame = tk.Frame(form_frame, bg='#f0f0f0')
        tipo_carga_frame.grid(row=1, column=1, sticky='w', pady=5)
        tk.Radiobutton(tipo_carga_frame, text="Circuito derivado", variable=self.tipo_carga_var, 
                      value="derivado", bg='#f0f0f0', font=self.font_normal).pack(side='left')
        tk.Radiobutton(tipo_carga_frame, text="Alimentador", variable=self.tipo_carga_var, 
                      value="alimentador", bg='#f0f0f0', font=self.font_normal).pack(side='left')
        
        tk.Label(form_frame, text="Tipo de equipo:", font=self.font_bold, bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        self.tipo_equipo_var = tk.StringVar(value="Motor")
        self.tipo_equipo_combo = ttk.Combobox(form_frame, textvariable=self.tipo_equipo_var, 
                                             width=18, font=self.font_normal)
        self.tipo_equipo_combo['values'] = ("Motor", "Transformador", "Potencia", "Interruptor", "Capacitor", "Generador")
        self.tipo_equipo_combo.grid(row=2, column=1, sticky='w', pady=5)
        self.tipo_equipo_combo.bind('<<ComboboxSelected>>', self.actualizar_factores)
        
        
        tk.Label(form_frame, text="Factor de potencia (cos φ):", font=self.font_bold, bg='#f0f0f0').grid(row=3, column=0, sticky='w', pady=5)
        self.fp_var = tk.StringVar(value="0.85")
        self.fp_entry = tk.Entry(form_frame, textvariable=self.fp_var, width=20, font=self.font_normal)
        self.fp_entry.grid(row=3, column=1, sticky='w', pady=5)
        
        
        tk.Label(form_frame, text="Potencia:", font=self.font_bold, bg='#f0f0f0').grid(row=4, column=0, sticky='w', pady=5)
        potencia_frame = tk.Frame(form_frame, bg='#f0f0f0')
        potencia_frame.grid(row=4, column=1, sticky='w', pady=5)
        
        self.potencia_var = tk.StringVar()
        tk.Entry(potencia_frame, textvariable=self.potencia_var, width=12, font=self.font_normal).pack(side='left', padx=(0, 5))
        
        self.unidad_potencia_var = tk.StringVar(value="W")
        self.unidad_combo = ttk.Combobox(potencia_frame, textvariable=self.unidad_potencia_var, 
                                        width=8, font=self.font_normal)
        self.unidad_combo['values'] = ("W", "kW", "kVA", "A", "HP")
        self.unidad_combo.pack(side='left')
        self.unidad_combo.bind('<<ComboboxSelected>>', self.cambiar_unidad_potencia)
        
        # Tensión nominal
        tk.Label(form_frame, text="Tensión nominal (V):", font=self.font_bold, bg='#f0f0f0').grid(row=5, column=0, sticky='w', pady=5)
        self.voltaje_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.voltaje_var, width=20, font=self.font_normal).grid(row=5, column=1, sticky='w', pady=5)
        
        # Material del conductor
        tk.Label(form_frame, text="Material del conductor:", font=self.font_bold, bg='#f0f0f0').grid(row=6, column=0, sticky='w', pady=5)
        self.material_var = tk.StringVar(value="cobre")
        material_frame = tk.Frame(form_frame, bg='#f0f0f0')
        material_frame.grid(row=6, column=1, sticky='w', pady=5)
        tk.Radiobutton(material_frame, text="Cobre", variable=self.material_var, 
                      value="cobre", bg='#f0f0f0', font=self.font_normal).pack(side='left')
        tk.Radiobutton(material_frame, text="Aluminio", variable=self.material_var, 
                      value="aluminio", bg='#f0f0f0', font=self.font_normal).pack(side='left')
        
        # Longitud del circuito
        tk.Label(form_frame, text="Longitud del circuito (m):", font=self.font_bold, bg='#f0f0f0').grid(row=7, column=0, sticky='w', pady=5)
        self.longitud_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.longitud_var, width=20, font=self.font_normal).grid(row=7, column=1, sticky='w', pady=5)
        
        # Conductores por fase
        tk.Label(form_frame, text="Conductores por fase:", font=self.font_bold, bg='#f0f0f0').grid(row=8, column=0, sticky='w', pady=5)
        self.num_conductores_var = tk.StringVar(value="1")
        tk.Entry(form_frame, textvariable=self.num_conductores_var, width=20, font=self.font_normal).grid(row=8, column=1, sticky='w', pady=5)
        
        # Tipo de instalación
        tk.Label(form_frame, text="Tipo de instalación:", font=self.font_bold, bg='#f0f0f0').grid(row=9, column=0, sticky='w', pady=5)
        self.canalizacion_var = tk.StringVar(value="PVC")
        canalizacion_combo = ttk.Combobox(form_frame, textvariable=self.canalizacion_var, 
                                         width=18, font=self.font_normal)
        canalizacion_combo['values'] = ("PVC", "Acero", "Charola")
        canalizacion_combo.grid(row=9, column=1, sticky='w', pady=5)
        canalizacion_combo.bind('<<ComboboxSelected>>', self.actualizar_info_canalizacion)
        
        # Información de canalización
        self.info_charola_label = tk.Label(form_frame, text="✓ Conduit PVC - Tabla 310-15(b)(16)", 
                                          font=self.font_small, bg='#f0f0f0', fg='#27ae60', 
                                          wraplength=200)
        self.info_charola_label.grid(row=10, column=1, sticky='w', pady=2)
        
        # Temperatura del conductor
        tk.Label(form_frame, text="Temperatura del conductor:", font=self.font_bold, bg='#f0f0f0').grid(row=11, column=0, sticky='w', pady=5)
        self.temperatura_conductor_var = tk.StringVar(value="75 °C")
        temperatura_combo = ttk.Combobox(form_frame, textvariable=self.temperatura_conductor_var, 
                                        width=18, font=self.font_normal)
        temperatura_combo['values'] = ("60 °C", "75 °C", "90 °C")
        temperatura_combo.grid(row=11, column=1, sticky='w', pady=5)
        
        # Campos específicos por equipo
        self.campos_especificos_frame = tk.Frame(form_frame, bg='#f0f0f0')
        self.campos_especificos_frame.grid(row=12, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Botones de acción
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=15)
        
        # Botón principal de calcular - MÁS PROMINENTE
        calcular_btn = tk.Button(button_frame, text="🧮 CALCULAR", 
                               command=self.calcular, font=('Century Gothic', 12, 'bold'),
                               bg='#e74c3c', fg='white', relief='raised', bd=4,
                               cursor='hand2', height=3, pady=10)
        calcular_btn.pack(fill='x', pady=(0, 10))
        
        # Botones secundarios
        secondary_buttons = tk.Frame(button_frame, bg='#f0f0f0')
        secondary_buttons.pack(fill='x', pady=(0, 5))
        
        limpiar_btn = tk.Button(secondary_buttons, text="🗑️ LIMPIAR", 
                              command=self.limpiar_campos, font=self.font_bold,
                              bg='#95a5a6', fg='white', relief='raised', bd=2,
                              cursor='hand2', height=2)
        limpiar_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        exportar_btn = tk.Button(secondary_buttons, text="📄 EXPORTAR PDF", 
                               command=self.exportar_a_pdf, font=self.font_bold,
                               bg='#8e44ad', fg='white', relief='raised', bd=2,
                               cursor='hand2', height=2)
        exportar_btn.pack(side='left', fill='x', expand=True, padx=5)
        
        # Botones terciarios
        tertiary_buttons = tk.Frame(button_frame, bg='#f0f0f0')
        tertiary_buttons.pack(fill='x')
        
        calcular_tuberia_btn = tk.Button(tertiary_buttons, text="🔧 Tubería", 
                                       command=self.calcular_tuberia, font=self.font_normal,
                                       bg='#27ae60', fg='white', relief='raised', bd=2,
                                       cursor='hand2')
        calcular_tuberia_btn.pack(side='left', fill='x', expand=True, padx=(0, 2))
        
        calcular_charola_btn = tk.Button(tertiary_buttons, text="📐 Charola", 
                                       command=self.calcular_charola, font=self.font_normal,
                                       bg='#f39c12', fg='white', relief='raised', bd=2,
                                       cursor='hand2')
        calcular_charola_btn.pack(side='left', fill='x', expand=True, padx=2)

    def mostrar_normativa_inicial(self):
        """Muestra la normativa aplicada en el panel de información."""
        pass  # El contenido ya está en la interfaz

    # Mantener todas las funciones originales de cálculo sin cambios
    def actualizar_info_canalizacion(self, event=None):
        canalizacion = self.canalizacion_var.get()
        
        if canalizacion == "Charola":
            self.info_charola_label.config(text="✓ Charola Portacables - Tabla 310-15(b)(20)", fg='#c0392b')
        elif canalizacion == "PVC":
            self.info_charola_label.config(text="✓ Conduit PVC - Tabla 310-15(b)(16)", fg='#27ae60')
        elif canalizacion == "Acero":
            self.info_charola_label.config(text="✓ Conduit Acero - Tabla 310-15(b)(16)", fg='#2c3e50')

    def es_instalacion_charola(self):
        canalizacion = self.canalizacion_var.get()
        return canalizacion == "Charola"

    def obtener_ampacidades_correctas(self, material, temp_conductor):
        es_charola = self.es_instalacion_charola()
        
        if es_charola:
            if material == "cobre":
                if temp_conductor == "75 °C":
                    return self.ampacidades_charola_cobre_75, "Tabla 310-15(b)(20) - Charola"
                elif temp_conductor == "90 °C":
                    return self.ampacidades_charola_cobre_90, "Tabla 310-15(b)(20) - Charola"
                else:
                    return self.ampacidades_charola_cobre_75, "Tabla 310-15(b)(20) - Charola (60°C no disponible, usando 75°C)"
            else:
                if temp_conductor == "75 °C":
                    return self.ampacidades_charola_aluminio_75, "Tabla 310-15(b)(20) - Charola"
                elif temp_conductor == "90 °C":
                    return self.ampacidades_charola_aluminio_90, "Tabla 310-15(b)(20) - Charola"
                else:
                    return self.ampacidades_charola_aluminio_75, "Tabla 310-15(b)(20) - Charola (60°C no disponible, usando 75°C)"
        else:
            if material == "cobre":
                if temp_conductor == "60 °C":
                    return self.ampacidades_cobre_60, "Tabla 310-15(b)(16) - Conduit"
                elif temp_conductor == "75 °C":
                    return self.ampacidades_cobre_75, "Tabla 310-15(b)(16) - Conduit"
                else:
                    return self.ampacidades_cobre_90, "Tabla 310-15(b)(16) - Conduit"
            else:
                return self.ampacidades_aluminio, "Tabla 310-15(b)(16) - Conduit"

    def obtener_impedancias_correctas(self, material, canalizacion):
        es_charola = self.es_instalacion_charola()
        
        if es_charola:
            if material == "cobre":
                return self.impedancia_charola_cobre, "Charola Portacables"
            else:
                return self.impedancia_charola_aluminio, "Charola Portacables"
        else:
            if material == "cobre":
                return self.impedancia_cobre[canalizacion], f"Conduit {canalizacion}"
            else:
                return self.impedancia_aluminio[canalizacion], f"Conduit {canalizacion}"

    def seleccionar_tierra_fisica(self, corriente_interruptor):
        for limite in sorted(self.calibre_tierra_fisica.keys()):
            if corriente_interruptor <= limite:
                return self.calibre_tierra_fisica[limite]
        return "500"

    def actualizar_factores(self, event=None):
        tipo = self.tipo_equipo_var.get()
        
        factores = {
            "Motor": "0.85",
            "Transformador": "0.95", 
            "Potencia": "1.0",
            "Interruptor": "1.0",
            "Capacitor": "0.1",
            "Generador": "0.8"
        }
        
        if tipo in factores:
            self.fp_var.set(factores[tipo])
        
        self.actualizar_campos_equipo()

    def actualizar_campos_equipo(self):
        for widget in self.campos_especificos_frame.winfo_children():
            widget.destroy()
        
        tipo_equipo = self.tipo_equipo_var.get()
        
        self.eficiencia_var = tk.StringVar(value="0.90")
        self.perdidas_var = tk.StringVar(value="0")
        self.kva_capacitor_var = tk.StringVar(value="0")
        self.temperatura_ambiente_var = tk.StringVar(value="30")
        
        if tipo_equipo == "Motor":
            tk.Label(self.campos_especificos_frame, text="Eficiencia del motor:", 
                    font=self.font_normal, bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=2)
            tk.Entry(self.campos_especificos_frame, textvariable=self.eficiencia_var, 
                    width=15, font=self.font_normal).grid(row=0, column=1, sticky='w', pady=2)
            
            tk.Label(self.campos_especificos_frame, text="Temp. ambiente (°C):", 
                    font=self.font_normal, bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=2)
            tk.Entry(self.campos_especificos_frame, textvariable=self.temperatura_ambiente_var, 
                    width=15, font=self.font_normal).grid(row=1, column=1, sticky='w', pady=2)
                    
        self.actualizar_unidades_disponibles()

    def actualizar_unidades_disponibles(self):
        tipo_equipo = self.tipo_equipo_var.get()
        
        if tipo_equipo == "Motor":
            unidades = ("W", "kW", "HP", "A")
        elif tipo_equipo == "Transformador":
            unidades = ("W", "kW", "kVA", "A")
        elif tipo_equipo == "Capacitor":
            unidades = ("kVAR", "A")
        elif tipo_equipo == "Generador":
            unidades = ("W", "kW", "kVA", "A")
        else:
            unidades = ("W", "kW", "A")
        
        self.unidad_combo['values'] = unidades
        
        if self.unidad_potencia_var.get() not in unidades:
            self.unidad_potencia_var.set(unidades[0])

    def cambiar_unidad_potencia(self, event=None):
        unidad = self.unidad_potencia_var.get()
        
        if unidad in ["A", "kVAR"]:
            self.fp_entry.config(state='disabled')
        else:
            self.fp_entry.config(state='normal')

    def calcular_corriente_por_equipo(self, tipo_equipo, valor, unidad, voltaje, tipo_circuito, factor_potencia):
        if unidad == "A":
            return float(valor), f"Corriente ingresada directamente: {valor} A"
        
        eficiencia = float(self.eficiencia_var.get()) if hasattr(self, 'eficiencia_var') else 0.90
        valor = float(valor)
        
        # Aplicar factor de demanda para alimentadores
        factor_demanda = self.obtener_factor_demanda()
        
        if tipo_equipo == "Motor":
            if unidad == "HP":
                potencia_mecanica = valor * 746
                potencia_electrica = potencia_mecanica / eficiencia
                formula = f"Motor: P_eléctrica = (HP × 746) / η = ({valor} × 746) / {eficiencia} = {potencia_electrica:.0f} W"
            elif unidad in ["W", "kW"]:
                potencia_electrica = valor * (1000 if unidad == "kW" else 1)
                formula = f"Motor: P_eléctrica = {valor} {unidad} = {potencia_electrica:.0f} W"
            
            # Aplicar factor de demanda si es alimentador
            if factor_demanda < 1.0:
                potencia_electrica *= factor_demanda
                formula += f"\nFactor de demanda aplicado: {factor_demanda} (Alimentador)"
                formula += f"\nP_demanda = {potencia_electrica:.0f} W"
            
            if tipo_circuito == "monofasico":
                corriente = potencia_electrica / (voltaje * factor_potencia)
                formula += f"\nI = P / (V × cos φ) = {potencia_electrica:.0f} / ({voltaje} × {factor_potencia}) = {corriente:.2f} A"
            else:
                corriente = potencia_electrica / (math.sqrt(3) * voltaje * factor_potencia)
                formula += f"\nI = P / (√3 × V × cos φ) = {potencia_electrica:.0f} / (√3 × {voltaje} × {factor_potencia}) = {corriente:.2f} A"
            
            return corriente, formula
            
        elif tipo_equipo == "Transformador":
            if unidad == "kVA":
                potencia_aparente = valor * 1000
                
                # Aplicar factor de demanda si es alimentador
                if factor_demanda < 1.0:
                    potencia_aparente *= factor_demanda
                    formula = f"Transformador: S = {valor} kVA × {factor_demanda} (Factor demanda) = {potencia_aparente:.0f} VA"
                else:
                    formula = f"Transformador: S = {valor} kVA = {potencia_aparente:.0f} VA"
                
                if tipo_circuito == "monofasico":
                    corriente = potencia_aparente / voltaje
                    formula += f"\nI = S / V = {potencia_aparente:.0f} / {voltaje} = {corriente:.2f} A"
                else:
                    corriente = potencia_aparente / (math.sqrt(3) * voltaje)
                    formula += f"\nI = S / (√3 × V) = {potencia_aparente:.0f} / (√3 × {voltaje}) = {corriente:.2f} A"
            elif unidad in ["W", "kW"]:
                potencia_activa = valor * (1000 if unidad == "kW" else 1)
                
                # Aplicar factor de demanda si es alimentador
                if factor_demanda < 1.0:
                    potencia_activa *= factor_demanda
                    formula = f"Transformador: P = {valor} {unidad} × {factor_demanda} (Factor demanda) = {potencia_activa:.0f} W"
                else:
                    formula = f"Transformador: P = {valor} {unidad} = {potencia_activa:.0f} W"
                
                if tipo_circuito == "monofasico":
                    corriente = potencia_activa / (voltaje * factor_potencia)
                    formula += f"\nI = P / (V × cos φ) = {potencia_activa:.0f} / ({voltaje} × {factor_potencia}) = {corriente:.2f} A"
                else:
                    corriente = potencia_activa / (math.sqrt(3) * voltaje * factor_potencia)
                    formula += f"\nI = P / (√3 × V × cos φ) = {potencia_activa:.0f} / (√3 × {voltaje} × {factor_potencia}) = {corriente:.2f} A"
            
            return corriente, formula
        elif tipo_equipo == "Capacitor":
            # IMPLEMENTACIÓN ESPECÍFICA PARA CAPACITORES
            if unidad == "kVAR":
                potencia_reactiva = valor * 1000  # Convertir kVAR a VAR
                
                # Aplicar factor de demanda si es alimentador
                if factor_demanda < 1.0:
                    potencia_reactiva *= factor_demanda
                    formula = f"Capacitor: Q = {valor} kVAR × {factor_demanda} (Factor demanda) = {potencia_reactiva:.0f} VAR"
                else:
                    formula = f"Capacitor: Q = {valor} kVAR = {potencia_reactiva:.0f} VAR"
                
                if tipo_circuito == "monofasico":
                    corriente = potencia_reactiva / voltaje
                    formula += f"\nI = Q / V = {potencia_reactiva:.0f} / {voltaje} = {corriente:.2f} A"
                else:
                    corriente = potencia_reactiva / (math.sqrt(3) * voltaje)
                    formula += f"\nI = Q / (√3 × V) = {potencia_reactiva:.0f} / (√3 × {voltaje}) = {corriente:.2f} A"
                
                return corriente, formula
                
            elif unidad == "A":
                return float(valor), f"Corriente ingresada directamente: {valor} A"
            else:
                raise ValueError("Para capacitores use únicamente kVAR o A como unidad")
        else:
            # CARGAS GENÉRICAS (Potencia, Generador, etc.)
            potencia = valor * (1000 if unidad == "kW" else 1)
            
            # Aplicar factor de demanda si es alimentador
            if factor_demanda < 1.0:
                potencia *= factor_demanda
                formula = f"Carga: P = {valor} {unidad} × {factor_demanda} (Factor demanda) = {potencia:.0f} W"
            else:
                formula = f"Carga: P = {valor} {unidad} = {potencia:.0f} W"
            
            if tipo_circuito == "monofasico":
                corriente = potencia / (voltaje * factor_potencia)
                formula += f"\nI = P / (V × cos φ) = {potencia:.0f} / ({voltaje} × {factor_potencia}) = {corriente:.2f} A"
            else:
                corriente = potencia / (math.sqrt(3) * voltaje * factor_potencia)
                formula += f"\nI = P / (√3 × V × cos φ) = {potencia:.0f} / (√3 × {voltaje} × {factor_potencia}) = {corriente:.2f} A"
            
            return corriente, formula
    def obtener_factor_demanda(self):
        """Obtiene el factor de demanda según el tipo de carga y equipo."""
        tipo_carga = self.tipo_carga_var.get()
        tipo_equipo = self.tipo_equipo_var.get()
        
        if tipo_carga == "alimentador":
            # Factores de demanda según Art. 220-11 y Tabla 220-11
            if tipo_equipo == "Motor":
                return 0.75  # Factor típico para múltiples motores
            elif tipo_equipo == "Transformador":
                return 0.85  # Factor para cargas diversas en alimentadores
            else:
                return 0.80  # Factor general para alimentadores
        else:
            return 1.0  # Sin factor de demanda para circuitos derivados

    def recomendar_calibre(self, corriente, material, num_conductores=1, temp_conductor="75 °C", es_corriente_directa=False, tipo_equipo="Motor", es_corriente_interruptor=False):
        ampacidades, fuente_tabla = self.obtener_ampacidades_correctas(material, temp_conductor)

        if not es_corriente_interruptor:
            if tipo_equipo == "Motor":
                factor = 1.25
                factor_aplicado = "1.25 (Art. 430-22 NOM - OBLIGATORIO para motores)"
            elif tipo_equipo == "Transformador":
                factor = 1.25
                factor_aplicado = "1.25 (Art. 450-3 NOM - OBLIGATORIO para transformadores)"
            elif tipo_equipo == "Capacitor":
                factor = 1.35
                factor_aplicado = "1.35 (Art. 460-8 NOM - OBLIGATORIO para capacitores)"
            elif tipo_equipo == "Generador":
                factor = 1.15
                factor_aplicado = "1.15 (Art. 445-5 NOM - OBLIGATORIO para generadores)"
            else:
                factor = 1.25
                factor_aplicado = "1.25 (OBLIGATORIO para cargas generales)"
            
            corriente_para_calibre = corriente * factor
        else:
            factor = 1.0
            factor_aplicado = "N/A (ya considerado en interruptor)"
            corriente_para_calibre = corriente

        corriente_por_conductor = corriente_para_calibre / num_conductores

        calibres_ordenados = [
            "14", "12", "10", "8", "6", "4", "3", "2", "1",
            "1/0", "2/0", "3/0", "4/0", "250", "300", "350",
            "400", "500", "600", "700", "750", "800", "900", "1000", "1250", "1500", "1750", "2000"
        ]

        for calibre in calibres_ordenados:
            if calibre in ampacidades and ampacidades[calibre] >= corriente_por_conductor:
                return calibre, ampacidades[calibre], corriente_por_conductor, corriente_para_calibre, factor_aplicado, fuente_tabla

        calibre_maximo = max(ampacidades.keys(), key=lambda x: ampacidades[x])
        return calibre_maximo, ampacidades[calibre_maximo], corriente_por_conductor, corriente_para_calibre, factor_aplicado, fuente_tabla

    def seleccionar_interruptor(self, corriente, tipo_equipo, corriente_para_calibre):
        if tipo_equipo == "Motor":
            if corriente <= 30:
                corriente_interruptor = corriente * 2.5
                tipo_proteccion = "Termomagnético Tipo D"
                curva_caracteristica = "Tipo D (arranque de motores)"
                factor_aplicado = "250% de I_motor (Art. 430-52)"
            else:
                corriente_interruptor = corriente * 1.75
                tipo_proteccion = "Termomagnético Tipo C"
                curva_caracteristica = "Tipo C (motores grandes)"
                factor_aplicado = "175% de I_motor (Art. 430-52)"
                
        elif tipo_equipo == "Transformador":
            if corriente <= 9:
                corriente_interruptor = corriente * 1.67
                factor_aplicado = "167% de I_trafo (Art. 450-3)"
            else:
                corriente_interruptor = corriente * 1.25
                factor_aplicado = "125% de I_trafo (Art. 450-3)"
            tipo_proteccion = "Termomagnético Tipo C"
            curva_caracteristica = "Tipo C (cargas resistivas)"
            
        elif tipo_equipo == "Capacitor":
            corriente_interruptor = corriente * 1.65
            tipo_proteccion = "Termomagnético Tipo C"
            curva_caracteristica = "Tipo C (cargas capacitivas)"
            factor_aplicado = "165% de I_capacitor (Art. 460-8)"
            
        elif tipo_equipo == "Generador":
            corriente_interruptor = corriente * 1.15
            tipo_proteccion = "Termomagnético Tipo C"
            curva_caracteristica = "Tipo C (fuente de alimentación)"
            factor_aplicado = "115% de I_generador (Art. 445-4)"
            
        else:
            corriente_interruptor = corriente_para_calibre
            tipo_proteccion = "Termomagnético Tipo C"
            curva_caracteristica = "Tipo C (uso general)"
            factor_aplicado = "125% de I_carga (aplicado en calibre)"

        interruptor_seleccionado = None
        for capacidad in self.interruptores_comerciales:
            if capacidad >= corriente_interruptor:
                interruptor_seleccionado = capacidad
                break
        
        if interruptor_seleccionado is None:
            interruptor_seleccionado = self.interruptores_comerciales[-1]
        
        num_polos = "1P" if hasattr(self, 'tipo_circuito_var') and self.tipo_circuito_var.get() == "monofasico" else "3P"
        
        advertencia_interruptor = ""
        if interruptor_seleccionado < corriente_interruptor:
            advertencia_interruptor = "⚠️ ADVERTENCIA: No hay interruptor comercial suficiente para la protección requerida"
        elif tipo_equipo == "Motor" and interruptor_seleccionado > corriente * 3:
            advertencia_interruptor = "⚠️ NOTA: Verificar coordinación con protección de sobrecarga del motor"
        
        return {
            'capacidad': interruptor_seleccionado,
            'tipo_proteccion': tipo_proteccion,
            'curva_caracteristica': curva_caracteristica,
            'num_polos': num_polos,
            'corriente_proteccion': corriente_interruptor,
            'factor_aplicado': factor_aplicado,
            'advertencia': advertencia_interruptor
        }

    def calcular(self):
        try:
            tipo_circuito = self.tipo_circuito_var.get()
            tipo_carga = self.tipo_carga_var.get()
            tipo_equipo = self.tipo_equipo_var.get()
            valor_potencia = self.potencia_var.get().strip()
            unidad_potencia = self.unidad_potencia_var.get()
            voltaje = float(self.voltaje_var.get())
            material = self.material_var.get()
            longitud = float(self.longitud_var.get())
            num_conductores = int(self.num_conductores_var.get())
            canalizacion = self.canalizacion_var.get()
            temp_conductor = self.temperatura_conductor_var.get()
            
            if not all([valor_potencia, self.voltaje_var.get(), 
                    self.longitud_var.get(), self.num_conductores_var.get()]):
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
                return
            
            if unidad_potencia not in ["A", "kVAR"]:
                factor_potencia = float(self.fp_var.get()) if self.fp_var.get() else 0.9
                if not (0.1 <= factor_potencia <= 1.0):
                    messagebox.showerror("Error", "Factor de potencia debe estar entre 0.1 y 1.0")
                    return
            else:
                factor_potencia = 1.0
            
            corriente, formula_corriente = self.calcular_corriente_por_equipo(
                tipo_equipo, valor_potencia, unidad_potencia, voltaje, tipo_circuito, factor_potencia
            )
            
            es_corriente_directa = unidad_potencia == "A"
            
            # PASO 1: Calcular factor normativo para protección
            if tipo_equipo == "Motor":
                factor_proteccion = 1.25
                factor_aplicado_texto = "1.25 (Art. 430-22 NOM - OBLIGATORIO para motores)"
            elif tipo_equipo == "Transformador":
                factor_proteccion = 1.25
                factor_aplicado_texto = "1.25 (Art. 450-3 NOM - OBLIGATORIO para transformadores)"
            elif tipo_equipo == "Capacitor":
                factor_proteccion = 1.35
                factor_aplicado_texto = "1.35 (Art. 460-8 NOM - OBLIGATORIO para capacitores)"
            elif tipo_equipo == "Generador":
                factor_proteccion = 1.15
                factor_aplicado_texto = "1.15 (Art. 445-5 NOM - OBLIGATORIO para generadores)"
            else:
                factor_proteccion = 1.25
                factor_aplicado_texto = "1.25 (OBLIGATORIO para cargas generales)"
            
            corriente_para_proteccion = corriente * factor_proteccion
            
            # PASO 2: Seleccionar interruptor basado en corriente con factor
            interruptor_info = self.seleccionar_interruptor(corriente, tipo_equipo, corriente_para_proteccion)
            
            # PASO 3: Usar corriente del interruptor para calcular calibre (SIN volver a aplicar factor)
            corriente_interruptor = interruptor_info['capacidad']
            corriente_por_conductor_final = corriente_interruptor / num_conductores
            
            # PASO 4: Seleccionar calibre basado en corriente del interruptor
            calibre_recomendado, ampacidad_calibre, corriente_por_conductor, _, factor_aplicado, fuente_tabla = self.recomendar_calibre(
                corriente=corriente_interruptor,
                material=material,
                num_conductores=num_conductores,
                temp_conductor=temp_conductor,
                es_corriente_directa=False,
                tipo_equipo=tipo_equipo,
                es_corriente_interruptor=True
            )

            es_charola = self.es_instalacion_charola()
            
            if es_charola:
                if material == "cobre":
                    tabla_impedancias = self.impedancia_charola_cobre
                    tipo_instalacion = "Charola Portacables (Tabla 310-15(b)(20))"
                else:
                    tabla_impedancias = self.impedancia_charola_aluminio
                    tipo_instalacion = "Charola Portacables (Tabla 310-15(b)(20))"
                
                if calibre_recomendado not in tabla_impedancias:
                    messagebox.showerror("Error", f"Calibre {calibre_recomendado} no disponible para charola en Tabla 310-15(b)(20).")
                    return
                
                z_individual = tabla_impedancias[calibre_recomendado]
            else:
                canalizacion_clave = canalizacion
                if canalizacion not in ["PVC", "Acero"]:
                    canalizacion_clave = "PVC"
                    
                if material == "cobre":
                    if canalizacion_clave in self.impedancia_cobre:
                        tabla_impedancias = self.impedancia_cobre[canalizacion_clave]
                        tipo_instalacion = f"Conduit {canalizacion_clave} (Tabla 310-15(b)(16))"
                    else:
                        messagebox.showerror("Error", f"Tipo de canalización '{canalizacion_clave}' no encontrado para cobre.")
                        return
                else:
                    if canalizacion_clave in self.impedancia_aluminio:
                        tabla_impedancias = self.impedancia_aluminio[canalizacion_clave]
                        tipo_instalacion = f"Conduit {canalizacion_clave} (Tabla 310-15(b)(16))"
                    else:
                        messagebox.showerror("Error", f"Tipo de canalización '{canalizacion_clave}' no encontrado para aluminio.")
                        return
                
                if calibre_recomendado not in tabla_impedancias:
                    messagebox.showerror("Error", f"Calibre {calibre_recomendado} no encontrado para {material.capitalize()} en {canalizacion_clave}.")
                    return
                
                z_individual = tabla_impedancias[calibre_recomendado]
                
            if tipo_circuito == "monofasico":
                caida_v = (2 * z_individual * corriente * longitud / 1000) / num_conductores
                formula_caida = f"Monofásico: ΔV = (2 × Z × I × L / 1000) / n"
                calculo_caida = f"ΔV = (2 × {z_individual} × {corriente:.2f} × {longitud} / 1000) / {num_conductores}"
            else:
                caida_v = (math.sqrt(3) * z_individual * corriente * longitud / 1000) / num_conductores
                formula_caida = f"Trifásico: ΔV = (√3 × Z × I × L / 1000) / n"
                calculo_caida = f"ΔV = (√3 × {z_individual} × {corriente:.2f} × {longitud} / 1000) / {num_conductores}"
            
            caida_p = (caida_v / voltaje) * 100
            
            mensaje_advertencia = ""
            margen_seguridad = ((ampacidad_calibre - corriente_por_conductor_final) / corriente_por_conductor_final) * 100
            
            if corriente_por_conductor_final > ampacidad_calibre:
                mensaje_advertencia = "❌ ERROR CRÍTICO: El calibre es INSUFICIENTE para la corriente requerida"
            elif margen_seguridad < 5:
                mensaje_advertencia = "⚠️ ADVERTENCIA: El calibre está muy cerca del límite de ampacidad"
            elif margen_seguridad < 15:
                mensaje_advertencia = "⚠️ PRECAUCIÓN: Margen de seguridad mínimo"
            else:
                mensaje_advertencia = f"✅ CORRECTO: Margen de seguridad del {margen_seguridad:.1f}%"
            
            # Calcular calibre de tierra física y mostrar resultados
            calibre_tierra = self.seleccionar_tierra_fisica(interruptor_info['capacidad'])
            
            # Actualizar labels de tipo de carga e instalación
            self.actualizar_tipo_instalacion_info(tipo_equipo, tipo_circuito, tipo_carga, canalizacion)
            
            self.mostrar_resultados_completos(caida_p, caida_v, tipo_carga, valor_potencia, unidad_potencia,
                                    corriente, corriente_para_proteccion, voltaje, calibre_recomendado, 
                                    material, longitud, num_conductores, canalizacion, tipo_circuito, z_individual, 
                                    factor_potencia, tipo_equipo, formula_corriente, 
                                    formula_caida, calculo_caida, ampacidad_calibre,
                                    corriente_por_conductor_final, mensaje_advertencia, temp_conductor, 
                                    es_corriente_directa, factor_aplicado_texto, interruptor_info, fuente_tabla, tipo_instalacion, es_charola, calibre_tierra)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en valores ingresados: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def actualizar_tipo_instalacion_info(self, tipo_equipo, tipo_circuito, tipo_carga, canalizacion):
        """Actualiza la información de tipo de carga e instalación."""
        factor_demanda = self.obtener_factor_demanda()
        factor_texto = f" (Factor demanda: {factor_demanda})" if factor_demanda < 1.0 else ""
        
        tipo_carga_texto = f"{tipo_equipo} {tipo_circuito} {tipo_carga.upper()}{factor_texto}"
        
        if tipo_carga == "alimentador":
            tipo_instalacion_texto = f"Alimentador principal en canalización {'portacables' if canalizacion == 'Charola' else 'cerrada'} - Límite caída: 2% (Art. 215-2)"
        else:
            tipo_instalacion_texto = f"Circuito derivado en canalización {'portacables' if canalizacion == 'Charola' else 'cerrada'} - Límite caída: 3% (Art. 210-19)"
        
        self.tipo_carga_label.config(text=tipo_carga_texto)
        self.tipo_instalacion_label.config(text=tipo_instalacion_texto)

    def mostrar_resultados_completos(self, caida_p, caida_v, tipo_carga, valor_potencia, unidad_potencia,
                            corriente, corriente_para_calibre, voltaje, calibre_recomendado, 
                            material, longitud, num_conductores, canalizacion, tipo_circuito, z_individual, 
                            factor_potencia, tipo_equipo, formula_corriente, 
                            formula_caida, calculo_caida, ampacidad_calibre,
                            corriente_por_conductor, mensaje_advertencia, temp_conductor, 
                            es_corriente_directa, factor_aplicado, interruptor_info, fuente_tabla, tipo_instalacion, es_charola, calibre_tierra):
        self.resultado_text.config(state='normal')
        self.resultado_text.delete('1.0', tk.END)
        
        resultado = f"RESULTADO DEL CÁLCULO - {tipo_equipo.upper()} {tipo_circuito.upper()}\n"
        resultado += "=" * 60 + "\n\n"
        
        # DATOS PRINCIPALES - Directos al grano
        resultado += f"CORRIENTE: {corriente:.2f} A\n"
        resultado += f"CORRIENTE CORREGIDA: {corriente_para_calibre:.2f} A (Factor {factor_aplicado.split('(')[1].split(' ')[0]})\n"
        resultado += f"INTERRUPTOR: {interruptor_info['capacidad']} A {interruptor_info['num_polos']} - {interruptor_info['tipo_proteccion']}\n"
        
        if num_conductores > 1:
            resultado += f"CORRIENTE POR CONDUCTOR: {corriente_por_conductor:.2f} A ({interruptor_info['capacidad']}A ÷ {num_conductores})\n"
        
        if num_conductores > 1:
            resultado += f"CALIBRE: {num_conductores} × {calibre_recomendado} AWG {material} ({ampacidad_calibre} A c/u)\n"
        else:
            resultado += f"CALIBRE: {calibre_recomendado} AWG {material} ({ampacidad_calibre} A)\n"
            
        resultado += f"TIERRA FÍSICA: {calibre_tierra} AWG {material} (Tabla 250-122)\n"
        resultado += f"CAÍDA DE TENSIÓN: {caida_p:.2f}% ({caida_v:.3f} V)"
        
        # Evaluación normativa CON LÍMITES CORRECTOS
        limite = 2 if tipo_carga == "alimentador" else 3
        normativa_ref = "Art. 215-2 FPN 2" if tipo_carga == "alimentador" else "Art. 210-19 FPN 4"
        
        if caida_p <= limite:
            resultado += f" ✅ CUMPLE (máx {limite}% - {normativa_ref})\n\n"
        else:
            resultado += f" ❌ EXCEDE {limite}% PERMITIDO ({normativa_ref})\n\n"
        
        # DATOS DEL CIRCUITO CON IDENTIFICACIÓN DE TIPO
        resultado += f"ENTRADA: {valor_potencia} {unidad_potencia}"
        if unidad_potencia not in ["A", "kVAR"] and factor_potencia != 1.0:
            resultado += f", FP: {factor_potencia}"
        resultado += f" | {voltaje} V | {longitud} m\n"
        
        # TIPO DE INSTALACIÓN MEJORADO
        tipo_instalacion_final = "CHAROLA" if es_charola else f"CONDUIT {canalizacion.upper()}"
        tipo_carga_texto = "ALIMENTADOR PRINCIPAL" if tipo_carga == "alimentador" else "CIRCUITO DERIVADO"
        resultado += f"TIPO: {tipo_carga_texto} | INSTALACIÓN: {tipo_instalacion_final} ({fuente_tabla.split(' - ')[0]})\n"
        
        # Factor de demanda si aplica
        factor_demanda = self.obtener_factor_demanda()
        if factor_demanda < 1.0:
            resultado += f"FACTOR DE DEMANDA: {factor_demanda} aplicado ({tipo_carga})\n"
        
        resultado += f"TEMPERATURA: {temp_conductor} | IMPEDANCIA: {z_individual} Ω/km ({canalizacion.upper()})\n\n"
        
        # CÁLCULOS APLICADOS
        resultado += f"FÓRMULAS APLICADAS:\n"
        if ":" in formula_corriente:
            formula_simple = formula_corriente.split('\n')[-1]
        else:
            formula_simple = f"I = {corriente:.2f} A"
        resultado += f"• Corriente: {formula_simple}\n"
        resultado += f"• Caída: {formula_caida} = {caida_v:.3f} V\n"
        resultado += f"• Factor seguridad: {factor_aplicado}\n"
        resultado += f"• Factor protección: {interruptor_info['factor_aplicado']}\n\n"
        
        # ADVERTENCIAS (solo si las hay)
        advertencias = []
        if mensaje_advertencia and ("ERROR" in mensaje_advertencia or "ADVERTENCIA" in mensaje_advertencia):
            advertencias.append(mensaje_advertencia)
        if interruptor_info.get('advertencia'):
            advertencias.append(interruptor_info['advertencia'])
        
        # Advertencias específicas para ALIMENTADORES
        if tipo_carga == "alimentador":
            if tipo_equipo == "Transformador":
                relacion = interruptor_info['capacidad'] / ampacidad_calibre
                if relacion > 3.5:
                    advertencias.append(f"⚠️ ALIMENTADOR: Coordinación I/C alta ({relacion:.1f}). Verificar compatibilidad con curva de arranque del transformador.")
                advertencias.append("⚠️ ALIMENTADOR: Verificar capacidad de cortocircuito del interruptor principal")
                advertencias.append("⚠️ ALIMENTADOR: Coordinación temporal con protecciones aguas arriba requerida")
                advertencias.append("⚠️ ALIMENTADOR: Considerar corriente de magnetización (inrush) en transformadores")
            elif tipo_equipo == "Motor":
                advertencias.append("⚠️ ALIMENTADOR: Factor de demanda aplicado según Art. 220-11")
                advertencias.append("⚠️ ALIMENTADOR: Verificar coordinación selectiva con protecciones derivadas")
            else:
                advertencias.append("⚠️ ALIMENTADOR: Aplicar estudio de coordinación de protecciones (Art. 240-12)")
                advertencias.append("⚠️ ALIMENTADOR: Verificar conductor de tierra del sistema (Art. 250-24)")
        
        # Advertencia contextual específica para transformadores en derivados
        elif tipo_equipo == "Transformador" and tipo_carga == "derivado":
            relacion = interruptor_info['capacidad'] / ampacidad_calibre
            if relacion > 3.5:
                advertencias.append(f"⚠️ DERIVADO: La coordinación I/C es alta ({relacion:.1f}). Verifica compatibilidad del interruptor con la curva de arranque del transformador.")
        
        if advertencias:
            resultado += f"⚠️ ADVERTENCIAS Y CONSIDERACIONES NORMATIVAS:\n"
            for adv in advertencias:
                resultado += f"• {adv}\n"
            resultado += "\n"
        
        # VERIFICACIONES TÉCNICAS
        margen_conductor = ((ampacidad_calibre - corriente_por_conductor) / corriente_por_conductor) * 100
        resultado += f"VERIFICACIONES:\n"
        resultado += f"• Margen conductor: {margen_conductor:.0f}% ({ampacidad_calibre}A vs {corriente_por_conductor:.1f}A req.)\n"
        
        relacion = interruptor_info['capacidad']/ampacidad_calibre
        if relacion <= 2.0:
            resultado += f"• Coordinación I/C: {relacion:.1f} ✅ CORRECTA\n"
        else:
            resultado += f"• Coordinación I/C: {relacion:.1f} ⚠️ REVISAR\n"
        
        # RECOMENDACIONES ESPECÍFICAS POR TIPO DE CARGA
        resultado += f"RECOMENDACIONES NORMATIVAS:\n"
        
        if tipo_carga == "alimentador":
            if tipo_equipo == "Motor":
                resultado += f"• Instalar protección por sobrecarga (relé térmico) en cada motor\n"
                resultado += f"• Aplicar factor de demanda 0.75 para múltiples motores (Art. 430-24)\n"
                resultado += f"• Coordinación selectiva con protecciones derivadas requerida\n"
            elif tipo_equipo == "Transformador":
                resultado += f"• Estudio de coordinación de protecciones obligatorio (Art. 240-12)\n"
                resultado += f"• Verificar capacidad de cortocircuito en barras principales\n"
                resultado += f"• Conexión a tierra del sistema según Art. 250-24\n"
            else:
                resultado += f"• Aplicar factores de demanda según Tabla 220-11\n"
                resultado += f"• Coordinación de protecciones en cascada\n"
                resultado += f"• Verificar conductor de tierra del sistema\n"
        else:  # circuito derivado
            if tipo_equipo == "Motor":
                resultado += f"• Instalar protección por sobrecarga (relé térmico)\n"
                resultado += f"• Verificar arranque según curva característica\n"
            elif tipo_equipo == "Transformador":
                resultado += f"• Considerar corriente de magnetización (inrush)\n"
                resultado += f"• Protección primaria y secundaria coordinadas\n"
            elif tipo_equipo == "Capacitor":
                resultado += f"• Verificar armónicos en el sistema\n"
                resultado += f"• Protección contra sobretensiones requerida\n"
        
        self.resultado_text.insert('1.0', resultado)
        self.resultado_text.config(state='disabled')
        
        self.agregar_historial_completo(tipo_circuito, tipo_carga, valor_potencia, unidad_potencia, 
                         corriente, corriente_para_calibre, voltaje, calibre_recomendado, material, 
                         longitud, num_conductores, canalizacion, z_individual, factor_potencia, 
                         tipo_equipo, formula_corriente, formula_caida, calculo_caida, caida_v, caida_p, 
                         ampacidad_calibre, corriente_por_conductor, mensaje_advertencia, temp_conductor,
                         factor_aplicado, interruptor_info, fuente_tabla, tipo_instalacion, es_charola, calibre_tierra)

    def agregar_historial_completo(self, tipo_circuito, tipo_carga, valor_potencia, unidad_potencia, 
                         corriente, corriente_para_proteccion, voltaje, calibre_recomendado, material, longitud, num_conductores, 
                         canalizacion, z_individual, factor_potencia, tipo_equipo, 
                         formula_corriente, formula_caida, calculo_caida, caida_v, caida_p, ampacidad_calibre,
                         corriente_por_conductor_final, mensaje_advertencia, temp_conductor, factor_aplicado_texto, 
                         interruptor_info, fuente_tabla, tipo_instalacion, es_charola, calibre_tierra):
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        corriente_interruptor = interruptor_info['capacidad']
        
        entrada_historial = {
            'timestamp': timestamp,
            'tipo_circuito': tipo_circuito,
            'tipo_carga': tipo_carga,
            'valor_potencia': valor_potencia,
            'unidad_potencia': unidad_potencia,
            'corriente': corriente,
            'corriente_para_proteccion': corriente_para_proteccion,
            'corriente_interruptor': corriente_interruptor,
            'voltaje': voltaje,
            'calibre': calibre_recomendado,
            'material': material,
            'longitud': longitud,
            'num_conductores': num_conductores,
            'canalizacion': canalizacion,
            'z': z_individual,
            'factor_potencia': factor_potencia,
            'tipo_equipo': tipo_equipo,
            'formula_corriente': formula_corriente,
            'formula_caida': formula_caida,
            'calculo_caida': calculo_caida,
            'caida_v': caida_v,
            'caida_p': caida_p,
            'ampacidad_calibre': ampacidad_calibre,
            'corriente_por_conductor_final': corriente_por_conductor_final,
            'mensaje_advertencia': mensaje_advertencia,
            'temp_conductor': temp_conductor,
            'factor_aplicado_texto': factor_aplicado_texto,
            'interruptor_info': interruptor_info,
            'fuente_tabla': fuente_tabla,
            'tipo_instalacion': tipo_instalacion,
            'es_charola': es_charola,
            'calibre_tierra': calibre_tierra
        }
        
        self.historial.append(entrada_historial)
        self.actualizar_historial_completo()

    def actualizar_historial_completo(self):
        self.historial_text.config(state='normal')
        self.historial_text.delete('1.0', tk.END)
        
        historial_texto = "HISTORIAL DE CÁLCULOS RECIENTES\n"
        historial_texto += "=" * 50 + "\n\n"
        
        for i, entrada in enumerate(reversed(self.historial[-6:]), 1):
            historial_texto += f"#{len(self.historial) - i + 1} - {entrada['timestamp']} - {entrada['tipo_equipo'].upper()}\n"
            historial_texto += "-" * 40 + "\n"
            
            # Identificar tipo de carga
            tipo_carga_hist = entrada.get('tipo_carga', 'derivado')
            tipo_carga_icon = "🏭" if tipo_carga_hist == "alimentador" else "🔌"
            
            historial_texto += f"{tipo_carga_icon} TIPO: {tipo_carga_hist.upper()}\n"
            historial_texto += f"🎯 SOLUCIÓN: {entrada['calibre']} AWG, "
            
            try:
                if isinstance(entrada['interruptor_info'], dict):
                    capacidad_interruptor = entrada['interruptor_info']['capacidad']
                else:
                    capacidad_interruptor = entrada.get('corriente_interruptor', 'N/A')
            except:
                capacidad_interruptor = 'N/A'
                
            historial_texto += f"{capacidad_interruptor}A, Tierra: {entrada.get('calibre_tierra', 'N/A')} AWG\n"
            historial_texto += f"📊 DATOS: {entrada['corriente']:.1f}A → {entrada['corriente_para_proteccion']:.1f}A → INT: {capacidad_interruptor}A\n"
            
            # Límite correcto según tipo de carga
            limite = 2 if tipo_carga_hist == 'alimentador' else 3
            normativa = "Art. 215-2" if tipo_carga_hist == 'alimentador' else "Art. 210-19"
            
            historial_texto += f"🔧 CALIBRE: Basado en corriente del interruptor ({capacidad_interruptor}A), {entrada['caida_p']:.1f}%"
            
            if entrada['caida_p'] <= limite:
                historial_texto += f" ✅ CUMPLE (máx {limite}% {normativa})\n"
            else:
                historial_texto += f" ❌ EXCEDE {limite}% ({normativa})\n"
            
            historial_texto += f"⚡ ENTRADA: {entrada['valor_potencia']} {entrada['unidad_potencia']}, {entrada['voltaje']}V, {entrada['longitud']}m\n"
            
            if entrada.get('es_charola', False):
                historial_texto += f"🔧 CHAROLA portacables\n"
            else:
                historial_texto += f"🔧 CONDUIT {entrada['canalizacion']}\n"
            
            # Mostrar factor de demanda si aplica
            if tipo_carga_hist == 'alimentador':
                historial_texto += f"📈 Factor demanda aplicado para {tipo_carga_hist}\n"
            
            if entrada['mensaje_advertencia'] and ("ERROR" in entrada['mensaje_advertencia'] or "ADVERTENCIA" in entrada['mensaje_advertencia']):
                historial_texto += f"⚠️ {entrada['mensaje_advertencia']}\n"
            
            historial_texto += "\n"
        
        if len(self.historial) > 6:
            historial_texto += f"... y {len(self.historial) - 6} cálculos anteriores\n\n"
        
        # Referencias técnicas condensadas
        historial_texto += "REFERENCIAS RÁPIDAS NOM-001-SEDE-2012:\n"
        historial_texto += "=" * 50 + "\n\n"
        
        
        historial_texto += "🔥 TABLA 250-122 - TIERRA FÍSICA:\n"
        historial_texto += "15-20A→12-14AWG | 30-60A→10AWG | 100A→8AWG\n"
        historial_texto += "200A→6AWG | 300A→4AWG | 400A→3AWG\n\n"
        
        historial_texto += "⚡ FACTORES DE SEGURIDAD:\n"
        historial_texto += "• MOTORES: 1.25× (Art. 430-22)\n"
        historial_texto += "• TRANSFORMADORES: 1.25× (Art. 450-3)\n"
        historial_texto += "• CAPACITORES: 1.35× (Art. 460-8)\n"
        historial_texto += "• GENERADORES: 1.15× (Art. 445-5)\n\n"
        
        historial_texto += "📋 FACTORES DE PROTECCIÓN:\n"
        historial_texto += "• MOTORES ≤30A: 2.5× (Tipo D)\n"
        historial_texto += "• MOTORES >30A: 1.75× (Tipo C)\n"
        historial_texto += "• TRANSFORMADORES ≤9A: 1.67×\n"
        historial_texto += "• TRANSFORMADORES >9A: 1.25×\n\n"
        
        historial_texto += "📏 LÍMITES DE CAÍDA DE TENSIÓN:\n"
        historial_texto += "• Circuitos derivados: 3% máx (Art. 210-19 FPN 4)\n"
        historial_texto += "• Alimentadores: 2% máx (Art. 215-2 FPN 2)\n\n"
        
        historial_texto += "📈 FACTORES DE DEMANDA (Art. 220-11):\n"
        historial_texto += "• Alimentadores - Motores: 0.75\n"
        historial_texto += "• Alimentadores - Transformadores: 0.85\n" 
        historial_texto += "• Alimentadores - Cargas generales: 0.80\n"
        historial_texto += "• Circuitos derivados: 1.0 (sin factor)\n\n"
        
        historial_texto += "🔧 TABLAS IMPLEMENTADAS:\n"
        historial_texto += "• 310-15(b)(16): Conduit (estándar)\n"
        historial_texto += "• 310-15(b)(20): Charola portacables\n"
        historial_texto += "• 250-122: Conductor tierra física\n"
        
        self.historial_text.insert('1.0', historial_texto)
        self.historial_text.config(state='disabled')
        self.historial_text.see('1.0')

    def limpiar_campos(self):
        self.potencia_var.set("")
        self.unidad_potencia_var.set("W")
        self.voltaje_var.set("")
        self.fp_var.set("0.85")
        self.longitud_var.set("")
        self.num_conductores_var.set("1")
        self.tipo_circuito_var.set("monofasico")
        self.tipo_carga_var.set("derivado")
        self.material_var.set("cobre")
        self.canalizacion_var.set("PVC")
        self.tipo_equipo_var.set("Motor")
        self.temperatura_conductor_var.set("75 °C")
        
        if hasattr(self, 'eficiencia_var'):
            self.eficiencia_var.set("0.90")
        if hasattr(self, 'perdidas_var'):
            self.perdidas_var.set("0")
        if hasattr(self, 'kva_capacitor_var'):
            self.kva_capacitor_var.set("0")
        if hasattr(self, 'temperatura_ambiente_var'):
            self.temperatura_ambiente_var.set("30")
        
        self.info_charola_label.config(text="✓ Conduit PVC - Tabla 310-15(b)(16)")
        
        self.resultado_text.config(state='normal')
        self.resultado_text.delete('1.0', tk.END)
        self.resultado_text.insert('1.0', 'Ingrese los datos del circuito y presione "CALCULAR" para obtener los resultados.')
        self.resultado_text.config(state='disabled')
        
        # Limpiar información de tipo de carga
        self.tipo_carga_label.config(text="-")
        self.tipo_instalacion_label.config(text="-")
        
        self.actualizar_campos_equipo()

    def calcular_tuberia(self):
        messagebox.showinfo("Calcular Tubería", "Función de cálculo de tubería - Por implementar")
        
    def calcular_charola(self):
        self.canalizacion_var.set("Charola")
        self.actualizar_info_canalizacion()
        
        info_msg = """CÁLCULO PARA CHAROLA PORTACABLES - METODOLOGÍA MEJORADA
        
CONFIGURACIÓN AUTOMÁTICA:
• Tabla aplicada: 310-15(b)(20)
• Instalación: Charola portacables
• Conductores: Sostenidos por mensajero
• Máximo: 3 conductores por fase

NUEVA METODOLOGÍA NORMATIVA:
1. Corriente nominal del equipo
2. Factor de seguridad normativo
3. Selección de interruptor comercial
4. Calibre basado en corriente del interruptor
5. SIN duplicar factores de seguridad

Presione 'CALCULAR' para experimentar la metodología mejorada."""
        
        messagebox.showinfo("Configuración para Charola", info_msg)

    def exportar_a_pdf(self):
        try:
            # Verificar que hay cálculos
            if not self.historial:
                messagebox.showwarning("Advertencia", "No hay cálculos para exportar. Realice al menos un cálculo.")
                return
            
            # Importar el módulo exportador
            try:
                from exportador import ExportadorPDF
            except ImportError:
                messagebox.showerror(
                    "Error de Importación", 
                    "No se pudo importar el módulo exportador.py\n\n"
                    "Verifique que el archivo exportador.py esté en la misma carpeta."
                )
                return
            
            # Crear instancia del exportador
            exportador = ExportadorPDF(self.historial)
            
            # Ejecutar la exportación
            resultado = exportador.exportar_reporte(self.root)
            
            if resultado:
                messagebox.showinfo("Éxito", "Memoria técnica exportada exitosamente en formato PDF.")
            else:
                messagebox.showwarning("Cancelado", "La exportación fue cancelada.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado al exportar a PDF: {str(e)}")

    def cerrar_aplicacion(self, event=None):
        """Cierra la aplicación de forma segura."""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea cerrar la aplicación?"):
            self.root.quit()

    def mostrar_acerca_de(self):
        """Muestra información acerca del programa."""
        info = """Sistema de Cálculos Eléctricos
        
Versión: 2.0
Desarrollado para: Hertz Ingeniería & Servicios Eléctricos S.A de C.V

CARACTERÍSTICAS:
• Cálculos según NOM-001-SEDE-2012
• Metodología normativa actualizada
• Soporte para charola portacables y conduit
• Exportación a PDF de reportes completos
• Historial de cálculos con referencias técnicas

CONTROLES:
• Escape: Cerrar aplicación
• Alt+F4: Cerrar aplicación

NORMATIVAS APLICADAS:
• Art. 430-22: Protección de motores
• Art. 450-3: Protección de transformadores  
• Art. 250-122: Conductor de tierra física
• Tabla 310-15(b)(16): Ampacidades en conduit
• Tabla 310-15(b)(20): Ampacidades en charola

© 2024 Hertz Ingeniería & Servicios Eléctricos"""
        
        messagebox.showinfo("Acerca de", info)
        
    def limpiar_historial(self):
        self.historial.clear()
        self.historial_text.config(state='normal')
        self.historial_text.delete('1.0', tk.END)
        self.historial_text.insert('1.0', """Historial limpiado.

🆕 NUEVA METODOLOGÍA IMPLEMENTADA

CAMBIO FUNDAMENTAL EN LA LÓGICA:
✅ Método anterior: Corriente → Factor → Calibre → Interruptor
✅ Método NUEVO: Corriente → Factor → Interruptor → Calibre

FLUJO CORRECTO IMPLEMENTADO:
1️⃣ Calcular corriente nominal del equipo (I_carga)
2️⃣ Aplicar factor normativo (I_protección = I_carga × Factor)
3️⃣ Seleccionar interruptor comercial superior a I_protección
4️⃣ Calcular corriente por conductor (I_conductor = I_interruptor ÷ n.º)
5️⃣ Buscar calibre SIN volver a aplicar factor de seguridad
6️⃣ Mostrar leyenda explicativa del método

VENTAJAS DE LA NUEVA METODOLOGÍA:
• Evita doble aplicación de factores de seguridad
• Calibre coherente con capacidad real del interruptor
• Cumplimiento estricto de NOM-001-SEDE-2012
• Coordinación perfecta conductor-interruptor
• Cálculo más preciso y normativo

NUEVAS LEYENDAS EN RESULTADOS:
• "Calibre determinado a partir del interruptor seleccionado"
• "Corriente por conductor ya considera factor normativo"
• "Selección basada en corriente del interruptor"

FUNCIONALIDADES ADICIONALES:
✅ Tabla 250-122 para conductor de tierra física
✅ División automática entre múltiples conductores  
✅ Tabla 310-15(b)(20) para charola portacables
✅ Resultados optimizados y concisos
✅ Exportación completa a PDF

Realice un cálculo para experimentar la nueva metodología normativa.""")
        self.historial_text.config(state='disabled')

# Función principal para ejecutar la aplicación
def main():
    """Función principal que inicia la aplicación."""
    try:
        root = tk.Tk()
        app = Calculos(root)
        
        # Configurar el cierre de ventana
        root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
        
       
        root.mainloop()
        
    except Exception as e:
        # En caso de error crítico, mostrar mensaje
        try:
            messagebox.showerror("Error Crítico", 
                               f"Error al iniciar la aplicación:\n{str(e)}\n\nContacte al soporte técnico.")
        except:
            print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()