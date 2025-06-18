import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
from tkinter import font

class NOMElectricalInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("NOM-001-SEDE-2012 - Normativa Eléctrica Mexicana")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8fafc')
        
        # Variables de estado
        self.active_section = tk.StringVar(value="overview")
        self.expanded_faq = tk.IntVar(value=-1)
        self.progress_value = tk.IntVar(value=50)
        
        # Configurar estilos
        self.setup_styles()
        
        # Datos de la aplicación
        self.setup_electrical_data()
        
        # Crear la interfaz
        self.create_interface()

    def setup_styles(self):
        """Configurar estilos personalizados para tema eléctrico"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones de navegación
        style.configure(
            "Navigation.TButton",
            padding=(15, 10),
            font=('Segoe UI', 10),
            borderwidth=1,
            relief="solid"
        )
        
        style.configure(
            "NavigationActive.TButton",
            background='#fef3c7',  # Amarillo eléctrico suave
            foreground='#d97706',  # Naranja eléctrico
            borderwidth=2,
            relief="solid"
        )
        
        # Estilo para el header
        style.configure(
            "Header.TFrame",
            background='white',
            relief="solid",
            borderwidth=1
        )
        
        # Estilo para tarjetas
        style.configure(
            "Card.TFrame",
            background='white',
            relief="solid",
            borderwidth=1,
            padding=20
        )

    def setup_electrical_data(self):
        """Configurar datos específicos de normativa eléctrica"""
        self.sections = [
            {"id": "overview", "title": "Visión General", "icon": "⚡"},
            {"id": "objectives", "title": "Objetivos", "icon": "🛡️"},
            {"id": "scope", "title": "Alcance", "icon": "🏗️"},
            {"id": "requirements", "title": "Requisitos Clave", "icon": "📋"},
            {"id": "formulas", "title": "Fórmulas y Cálculos", "icon": "🧮"},
            {"id": "implementation", "title": "Implementación", "icon": "⚙️"},
            {"id": "tables", "title": "Tablas Normativas", "icon": "📊"}
        ]
        
        self.electrical_principles = [
            {
                "title": "🛡️ Seguridad Eléctrica",
                "description": "Protección de personas y bienes contra riesgos eléctricos",
                "color": "#fee2e2",
                "details": "Aplicación de factores de seguridad y protecciones adecuadas"
            },
            {
                "title": "⚙️ Coordinación Protecciones",
                "description": "Selección correcta de conductor e interruptor",
                "color": "#dbeafe",
                "details": "Garantizar que las protecciones operen antes que el conductor"
            },
            {
                "title": "📉 Control Caída de Tensión",
                "description": "Mantener voltaje dentro de límites permitidos",
                "color": "#dcfce7",
                "details": "Máximo 3% alimentadores, 2% circuitos derivados"
            }
        ]
        
        self.key_articles = [
            {
                "article": "Art. 430-22",
                "title": "Protección Motores",
                "description": "Factor 125% para conductores de motores",
                "formula": "I_conductor = I_motor × 1.25",
                "color": "#fef3c7"
            },
            {
                "article": "Art. 450-3",
                "title": "Protección Transformadores",
                "description": "Protección primaria 125%-167% según kVA",
                "formula": "I_prot = (kVA × 1000) / (V × √3) × Factor",
                "color": "#fecaca"
            },
            {
                "article": "Art. 460-8",
                "title": "Protección Capacitores",
                "description": "Factor 135% para conductores de capacitores",
                "formula": "I_conductor = I_capacitor × 1.35",
                "color": "#e9d5ff"
            },
            {
                "article": "Art. 250-122",
                "title": "Conductor Tierra Física",
                "description": "Selección según capacidad del interruptor",
                "formula": "Calibre según Tabla 250-122",
                "color": "#bfdbfe"
            },
            {
                "article": "Art. 210-19",
                "title": "Caída de Tensión Circuitos",
                "description": "Máximo 3% en alimentadores, 2% derivados",
                "formula": "ΔV ≤ 3% alimentadores, ≤ 2% derivados",
                "color": "#a7f3d0"
            }
        ]
        
        self.electrical_formulas = [
            {
                "name": "Corriente Monofásica",
                "formula": "I = P / (V × cos φ)",
                "variables": "I=Corriente(A), P=Potencia(W), V=Voltaje(V), cos φ=Factor de potencia",
                "example": "Motor 5HP, 220V, cos φ=0.8: I = 3730/(220×0.8) = 21.2 A"
            },
            {
                "name": "Corriente Trifásica",
                "formula": "I = P / (√3 × V × cos φ)",
                "variables": "I=Corriente(A), P=Potencia(W), V=Voltaje(V), cos φ=Factor de potencia",
                "example": "Motor 10HP, 440V, cos φ=0.85: I = 7460/(1.732×440×0.85) = 11.5 A"
            },
            {
                "name": "Caída de Tensión Monofásica",
                "formula": "ΔV = (2 × Z × I × L) / (1000 × n)",
                "variables": "ΔV=Caída(V), Z=Impedancia(Ω/km), I=Corriente(A), L=Longitud(m), n=Conductores/fase",
                "example": "Calibre 12 AWG, 50m, 20A: ΔV = (2×6.6×20×50)/(1000×1) = 13.2V"
            },
            {
                "name": "Caída de Tensión Trifásica",
                "formula": "ΔV = (√3 × Z × I × L) / (1000 × n)",
                "variables": "ΔV=Caída(V), Z=Impedancia(Ω/km), I=Corriente(A), L=Longitud(m), n=Conductores/fase",
                "example": "Calibre 10 AWG, 80m, 30A: ΔV = (1.732×4.15×30×80)/(1000×1) = 12.9V"
            }
        ]
        
        self.normative_tables = [
            {
                "table": "310-15(b)(16)",
                "title": "Ampacidad en Conduit",
                "description": "Corriente permitida para conductores en conduit",
                "usage": "Selección de calibre según corriente calculada"
            },
            {
                "table": "310-15(b)(20)",
                "title": "Ampacidad en Charola",
                "description": "Corriente permitida para conductores en charola",
                "usage": "Mayor ampacidad que conduit, hasta 30% más"
            },
            {
                "table": "250-122",
                "title": "Conductor Tierra Física",
                "description": "Calibre mínimo según capacidad del interruptor",
                "usage": "Protección y seguridad del sistema eléctrico"
            },
            {
                "table": "310-104",
                "title": "Factores de Corrección",
                "description": "Factores por temperatura y agrupamiento",
                "usage": "Ajuste de ampacidad según condiciones de instalación"
            }
        ]
        
        self.faqs = [
            {
                "question": "¿Qué diferencia hay entre la NOM-001-SEDE-2012 y el NEC?",
                "answer": "La NOM-001-SEDE-2012 está basada en el NEC (National Electrical Code) pero adaptada a las condiciones y requerimientos específicos de México. Incluye modificaciones para voltajes, frecuencias y condiciones ambientales locales."
            },
            {
                "question": "¿Cuándo debo aplicar el factor 125% en conductores?",
                "answer": "El factor 125% se aplica principalmente en: motores (Art. 430-22), cargas continuas por más de 3 horas, y algunos casos de transformadores y capacitores según sus artículos específicos."
            },
            {
                "question": "¿Cómo calculo la caída de tensión permitida?",
                "answer": "Para alimentadores: máximo 3% del voltaje nominal. Para circuitos derivados: máximo 2%. La suma total no debe exceder 5%. Se calcula con las fórmulas específicas según el sistema (monofásico o trifásico)."
            },
            {
                "question": "¿Qué calibre de tierra física debo usar?",
                "answer": "Se determina según la Tabla 250-122 basándose en la capacidad del interruptor principal del circuito. Por ejemplo: interruptor 100A requiere conductor tierra calibre 8 AWG mínimo."
            }
        ]

    def create_interface(self):
        """Crear la interfaz principal"""
        # Header
        self.create_header()
        
        # Container principal
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Crear sidebar y contenido principal
        self.create_sidebar(main_container)
        self.create_main_content(main_container)

    def create_header(self):
        """Crear el header de la aplicación"""
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Container del header
        header_container = ttk.Frame(header_frame)
        header_container.pack(fill=tk.X, padx=20, pady=15)
        
        # Logo y título (lado izquierdo)
        left_frame = ttk.Frame(header_container)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Icono eléctrico
        icon_label = tk.Label(
            left_frame, 
            text="⚡", 
            font=('Segoe UI', 20),
            bg='#f59e0b',  # Amarillo/naranja eléctrico
            fg='white',
            width=3,
            height=1
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Títulos
        title_frame = ttk.Frame(left_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(
            title_frame,
            text="NOM-001-SEDE-2012",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Normativa Eléctrica Mexicana",
            font=('Segoe UI', 10),
            bg='white',
            fg='#6b7280'
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Controles (lado derecho)
        right_frame = ttk.Frame(header_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Campo de búsqueda
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        search_entry = ttk.Entry(
            search_frame,
            font=('Segoe UI', 10),
            width=25
        )
        search_entry.pack(side=tk.LEFT)
        search_entry.insert(0, "Buscar artículo o tabla...")
        
        # Botón calculadora
        calc_btn = ttk.Button(
            right_frame,
            text="🧮 Calculadora",
            command=self.open_calculator
        )
        calc_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de descarga
        download_btn = ttk.Button(
            right_frame,
            text="📥 Descargar NOM",
            command=self.download_nom
        )
        download_btn.pack(side=tk.LEFT)

    def create_sidebar(self, parent):
        """Crear el sidebar de navegación"""
        self.sidebar_frame = ttk.Frame(parent, style="Card.TFrame")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.sidebar_frame.configure(width=300)
        
        # Título del sidebar
        sidebar_title = tk.Label(
            self.sidebar_frame,
            text="Contenido",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        sidebar_title.pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        # Botones de navegación
        self.nav_buttons = {}
        for section in self.sections:
            btn_frame = ttk.Frame(self.sidebar_frame)
            btn_frame.pack(fill=tk.X, padx=20, pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=f"{section['icon']} {section['title']}",
                font=('Segoe UI', 10),
                bg='#fef3c7',
                fg='#92400e',
                border=1,
                relief="solid",
                anchor="w",
                padx=15,
                pady=10,
                command=lambda s=section['id']: self.change_section(s)
            )
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#fde68a'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#fef3c7') if self.active_section.get() != section['id'] else None)
            
            self.nav_buttons[section['id']] = btn
        
        # Separador
        separator = ttk.Separator(self.sidebar_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=20, pady=20)
        
        # Indicador de cumplimiento
        compliance_frame = ttk.Frame(self.sidebar_frame)
        compliance_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        compliance_title = tk.Label(
            compliance_frame,
            text="Estado de Cumplimiento",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        )
        compliance_title.pack(anchor=tk.W)
        
        # Semáforo de cumplimiento
        status_frame = ttk.Frame(compliance_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(status_frame, text="✅ Seguridad", bg='white', fg='#059669', font=('Segoe UI', 9)).pack(anchor=tk.W)
        tk.Label(status_frame, text="⚠️ Caída tensión", bg='white', fg='#d97706', font=('Segoe UI', 9)).pack(anchor=tk.W)
        tk.Label(status_frame, text="✅ Protecciones", bg='white', fg='#059669', font=('Segoe UI', 9)).pack(anchor=tk.W)
        
        # Barra de progreso
        progress_frame = ttk.Frame(self.sidebar_frame)
        progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        progress_label = tk.Label(
            progress_frame,
            text="Progreso de lectura",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        )
        progress_label.pack(anchor=tk.W)
        
        progress_info = tk.Label(
            progress_frame,
            text="4/7",
            font=('Segoe UI', 9),
            bg='white',
            fg='#6b7280'
        )
        progress_info.pack(anchor=tk.E)
        
        progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_value,
            maximum=100,
            length=250
        )
        progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Actualizar botón activo inicial
        self.update_active_button()

    def create_main_content(self, parent):
        """Crear el área de contenido principal"""
        # Frame principal con scroll
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para scroll vertical
        self.canvas = tk.Canvas(self.main_frame, bg='#f8fafc', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Vincular mousewheel al canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Contenido inicial
        self.update_content()

    def _on_mousewheel(self, event):
        """Manejar scroll con rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def change_section(self, section_id):
        """Cambiar sección activa"""
        self.active_section.set(section_id)
        self.update_active_button()
        self.update_content()
        
        # Actualizar progreso
        section_index = next(i for i, s in enumerate(self.sections) if s['id'] == section_id)
        progress = int((section_index + 1) / len(self.sections) * 100)
        self.progress_value.set(progress)

    def update_active_button(self):
        """Actualizar estilo del botón activo"""
        for section_id, btn in self.nav_buttons.items():
            if section_id == self.active_section.get():
                btn.configure(bg='#fed7aa', fg='#c2410c', relief="solid")
            else:
                btn.configure(bg='#fef3c7', fg='#92400e', relief="solid")

    def update_content(self):
        """Actualizar contenido principal según sección activa"""
        # Limpiar contenido anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Obtener sección activa
        section = self.active_section.get()
        
        if section == "overview":
            self.create_overview_content()
        elif section == "objectives":
            self.create_objectives_content()
        elif section == "scope":
            self.create_scope_content()
        elif section == "requirements":
            self.create_requirements_content()
        elif section == "formulas":
            self.create_formulas_content()
        elif section == "implementation":
            self.create_implementation_content()
        elif section == "tables":
            self.create_tables_content()
        
        # Crear sección FAQ al final
        self.create_faq_section()

    def create_overview_content(self):
        """Crear contenido de visión general"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Hero section
        hero_frame = tk.Frame(content_frame, bg='#fed7aa', relief="solid", borderwidth=1)
        hero_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = tk.Label(
            hero_frame,
            text="NOM-001-SEDE-2012",
            font=('Segoe UI', 24, 'bold'),
            bg='#fed7aa',
            fg='#c2410c'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        subtitle_label = tk.Label(
            hero_frame,
            text="Normativa Oficial Mexicana - Instalaciones Eléctricas",
            font=('Segoe UI', 16, 'bold'),
            bg='#fed7aa',
            fg='#ea580c'
        )
        subtitle_label.pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        desc_label = tk.Label(
            hero_frame,
            text="Establece las condiciones técnicas mínimas para instalaciones eléctricas seguras en México.\nAplica a sistemas eléctricos en edificaciones habitacionales, comerciales, industriales y del sector público.\nBasada en el National Electrical Code (NEC) con adaptaciones para condiciones mexicanas.",
            font=('Segoe UI', 11),
            bg='#fed7aa',
            fg='#7c2d12',
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Principios fundamentales
        principles_label = tk.Label(
            content_frame,
            text="Principios Fundamentales de Seguridad Eléctrica",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        principles_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Grid de principios
        principles_frame = ttk.Frame(content_frame)
        principles_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        for i, principle in enumerate(self.electrical_principles):
            row = i // 3
            col = i % 3
            
            principle_frame = tk.Frame(principles_frame, bg=principle["color"], relief="solid", borderwidth=1)
            principle_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            title_label = tk.Label(
                principle_frame,
                text=principle["title"],
                font=('Segoe UI', 12, 'bold'),
                bg=principle["color"],
                fg='#1f2937'
            )
            title_label.pack(pady=(15, 5), padx=15)
            
            desc_label = tk.Label(
                principle_frame,
                text=principle["description"],
                font=('Segoe UI', 10),
                bg=principle["color"],
                fg='#374151',
                wraplength=200,
                justify=tk.CENTER
            )
            desc_label.pack(pady=5, padx=15)
            
            details_label = tk.Label(
                principle_frame,
                text=principle["details"],
                font=('Segoe UI', 9),
                bg=principle["color"],
                fg='#6b7280',
                wraplength=200,
                justify=tk.CENTER
            )
            details_label.pack(pady=(0, 15), padx=15)
        
        # Configurar grid weights
        for i in range(3):
            principles_frame.columnconfigure(i, weight=1)

    def create_requirements_content(self):
        """Crear contenido de requisitos clave"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = tk.Label(
            content_frame,
            text="Artículos Clave de la NOM-001-SEDE-2012",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        desc_label = tk.Label(
            content_frame,
            text="Artículos más utilizados en cálculos eléctricos y selección de equipos de protección.",
            font=('Segoe UI', 11),
            bg='white',
            fg='#6b7280',
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Artículos clave
        for article in self.key_articles:
            article_frame = tk.Frame(content_frame, bg=article["color"], relief="solid", borderwidth=2)
            article_frame.pack(fill=tk.X, padx=20, pady=8)
            
            # Header del artículo
            header_frame = ttk.Frame(article_frame)
            header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
            
            # Información del artículo
            info_frame = ttk.Frame(header_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            article_num = tk.Label(
                info_frame,
                text=article["article"],
                font=('Segoe UI', 12, 'bold'),
                bg=article["color"],
                fg='#1f2937'
            )
            article_num.pack(anchor=tk.W)
            
            article_title = tk.Label(
                info_frame,
                text=article["title"],
                font=('Segoe UI', 11, 'bold'),
                bg=article["color"],
                fg='#374151'
            )
            article_title.pack(anchor=tk.W, pady=(2, 0))
            
            article_desc = tk.Label(
                info_frame,
                text=article["description"],
                font=('Segoe UI', 10),
                bg=article["color"],
                fg='#6b7280'
            )
            article_desc.pack(anchor=tk.W, pady=(5, 0))
            
            # Fórmula
            formula_frame = tk.Frame(article_frame, bg='white', relief="solid", borderwidth=1)
            formula_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
            
            formula_label = tk.Label(
                formula_frame,
                text=f"Fórmula: {article['formula']}",
                font=('Courier New', 10, 'bold'),
                bg='white',
                fg='#059669',
                padx=10,
                pady=8
            )
            formula_label.pack(anchor=tk.W)

    def create_formulas_content(self):
        """Crear contenido de fórmulas y cálculos"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = tk.Label(
            content_frame,
            text="Fórmulas Eléctricas Fundamentales",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        desc_label = tk.Label(
            content_frame,
            text="Fórmulas esenciales para cálculos de corriente, caída de tensión y dimensionamiento de conductores.",
            font=('Segoe UI', 11),
            bg='white',
            fg='#6b7280',
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Fórmulas
        for i, formula in enumerate(self.electrical_formulas):
            formula_frame = tk.Frame(content_frame, bg='#f0f9ff', relief="solid", borderwidth=2)
            formula_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Nombre de la fórmula
            name_label = tk.Label(
                formula_frame,
                text=formula["name"],
                font=('Segoe UI', 14, 'bold'),
                bg='#f0f9ff',
                fg='#0c4a6e'
            )
            name_label.pack(anchor=tk.W, padx=15, pady=(15, 5))
            
            # Fórmula matemática
            math_frame = tk.Frame(formula_frame, bg='white', relief="solid", borderwidth=1)
            math_frame.pack(fill=tk.X, padx=15, pady=5)
            
            math_label = tk.Label(
                math_frame,
                text=formula["formula"],
                font=('Courier New', 16, 'bold'),
                bg='white',
                fg='#dc2626',
                padx=20,
                pady=10
            )
            math_label.pack()
            
            # Variables
            variables_label = tk.Label(
                formula_frame,
                text=f"Variables: {formula['variables']}",
                font=('Segoe UI', 9),
                bg='#f0f9ff',
                fg='#374151',
                wraplength=700,
                justify=tk.LEFT
            )
            variables_label.pack(anchor=tk.W, padx=15, pady=5)
            
            # Ejemplo
            example_frame = tk.Frame(formula_frame, bg='#ecfdf5', relief="solid", borderwidth=1)
            example_frame.pack(fill=tk.X, padx=15, pady=(5, 15))
            
            example_label = tk.Label(
                example_frame,
                text=f"Ejemplo: {formula['example']}",
                font=('Segoe UI', 9, 'italic'),
                bg='#ecfdf5',
                fg='#059669',
                wraplength=700,
                justify=tk.LEFT,
                padx=10,
                pady=8
            )
            example_label.pack(anchor=tk.W)

    def create_tables_content(self):
        """Crear contenido de tablas normativas"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = tk.Label(
            content_frame,
            text="Tablas Normativas Principales",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        desc_label = tk.Label(
            content_frame,
            text="Tablas más utilizadas para selección de conductores, protecciones y cálculos eléctricos.",
            font=('Segoe UI', 11),
            bg='white',
            fg='#6b7280',
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Tablas
        colors = ['#f0f9ff', '#fef3c7', '#ecfdf5', '#fdf2f8']
        
        for i, table in enumerate(self.normative_tables):
            table_frame = tk.Frame(content_frame, bg=colors[i % len(colors)], relief="solid", borderwidth=2)
            table_frame.pack(fill=tk.X, padx=20, pady=8)
            
            # Número de tabla
            table_num = tk.Label(
                table_frame,
                text=f"Tabla {table['table']}",
                font=('Segoe UI', 14, 'bold'),
                bg=colors[i % len(colors)],
                fg='#1f2937'
            )
            table_num.pack(anchor=tk.W, padx=15, pady=(15, 5))
            
            # Título de tabla
            table_title = tk.Label(
                table_frame,
                text=table["title"],
                font=('Segoe UI', 12, 'bold'),
                bg=colors[i % len(colors)],
                fg='#374151'
            )
            table_title.pack(anchor=tk.W, padx=15, pady=(0, 5))
            
            # Descripción
            table_desc = tk.Label(
                table_frame,
                text=table["description"],
                font=('Segoe UI', 10),
                bg=colors[i % len(colors)],
                fg='#6b7280'
            )
            table_desc.pack(anchor=tk.W, padx=15, pady=(0, 5))
            
            # Uso
            usage_label = tk.Label(
                table_frame,
                text=f"Uso: {table['usage']}",
                font=('Segoe UI', 9, 'italic'),
                bg=colors[i % len(colors)],
                fg='#059669'
            )
            usage_label.pack(anchor=tk.W, padx=15, pady=(0, 15))

    def create_objectives_content(self):
        """Crear contenido de objetivos"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            content_frame,
            text="Objetivos de la NOM-001-SEDE-2012",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=20)
        
        objectives = [
            "Proteger a las personas contra riesgos eléctricos como choques eléctricos y quemaduras",
            "Proteger bienes y propiedades contra daños por instalaciones eléctricas defectuosas",
            "Establecer prácticas seguras de instalación, operación y mantenimiento",
            "Garantizar la continuidad y calidad del servicio eléctrico",
            "Promover el uso eficiente de la energía eléctrica",
            "Facilitar el cumplimiento de regulaciones gubernamentales mexicanas"
        ]
        
        for i, objective in enumerate(objectives):
            obj_frame = tk.Frame(content_frame, bg='#fef3c7', relief="solid", borderwidth=1)
            obj_frame.pack(fill=tk.X, padx=20, pady=5)
            
            # Icono de seguridad
            icon_label = tk.Label(
                obj_frame,
                text="🛡️",
                font=('Segoe UI', 20),
                bg='#fed7aa',
                width=3,
                height=1
            )
            icon_label.pack(side=tk.LEFT, padx=(15, 10), pady=15)
            
            # Texto del objetivo
            obj_label = tk.Label(
                obj_frame,
                text=objective,
                font=('Segoe UI', 10),
                bg='#fef3c7',
                fg='#92400e',
                wraplength=600,
                justify=tk.LEFT
            )
            obj_label.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 15), pady=15)

    def create_scope_content(self):
        """Crear contenido de alcance"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            content_frame,
            text="Alcance de la Normativa",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=20)
        
        info_text = scrolledtext.ScrolledText(
            content_frame,
            height=15,
            font=('Segoe UI', 10),
            wrap=tk.WORD
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scope_content = """
ALCANCE DE LA NOM-001-SEDE-2012

APLICACIONES:
• Instalaciones eléctricas en edificaciones habitacionales
• Instalaciones comerciales e industriales
• Instalaciones del sector público
• Sistemas monofásicos y trifásicos hasta 1000 V

SISTEMAS CUBIERTOS:
• Conductores y cables eléctricos
• Conduits, ductos y charolas portacables
• Sistemas de tierra física y pararrayos
• Protecciones eléctricas (interruptores, fusibles)
• Motores, transformadores y capacitores
• Tableros de distribución y control
• Instalaciones en áreas peligrosas

CÁLCULOS INCLUIDOS:
• Determinación de corrientes de carga
• Selección de calibres de conductores
• Cálculo de caída de tensión
• Dimensionamiento de protecciones
• Factores de corrección por temperatura
• Factores de agrupamiento de conductores

EXCLUSIONES:
• Instalaciones de empresas de servicio público
• Instalaciones en minas subterráneas
• Sistemas de más de 1000 V (alta tensión)
• Instalaciones navales y aeronáuticas
• Vehículos eléctricos (excepto carga)

CONDICIONES AMBIENTALES MEXICANAS:
• Temperaturas de -10°C a +50°C
• Altitudes hasta 2500 metros sobre el nivel del mar
• Humedad relativa hasta 95%
• Condiciones sísmicas y climáticas locales
        """
        
        info_text.insert(tk.END, scope_content)
        info_text.configure(state='disabled')

    def create_implementation_content(self):
        """Crear contenido de implementación"""
        content_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            content_frame,
            text="Implementación en Aplicaciones de Cálculo",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(anchor=tk.W, padx=20, pady=20)
        
        steps = [
            {
                "step": "Entrada de Datos",
                "desc": "Potencia, voltaje, factor de potencia, longitud del conductor",
                "icon": "📊"
            },
            {
                "step": "Cálculo de Corriente",
                "desc": "Aplicación de fórmulas según sistema monofásico o trifásico",
                "icon": "⚡"
            },
            {
                "step": "Aplicación de Factores",
                "desc": "Factor 125% para motores, 135% para capacitores según NOM",
                "icon": "🔢"
            },
            {
                "step": "Selección de Conductor",
                "desc": "Consulta automática de Tabla 310-15(b)(16) o 310-15(b)(20)",
                "icon": "🔌"
            },
            {
                "step": "Verificación Caída Tensión",
                "desc": "Cálculo y validación de límites 3% alimentadores, 2% derivados",
                "icon": "📉"
            },
            {
                "step": "Selección de Protección",
                "desc": "Interruptor según corriente y coordinación con conductor",
                "icon": "🛡️"
            },
            {
                "step": "Conductor Tierra Física",
                "desc": "Selección automática según Tabla 250-122",
                "icon": "🌍"
            }
        ]
        
        for i, step in enumerate(steps):
            step_frame = tk.Frame(content_frame, bg='#f0f9ff', relief="solid", borderwidth=1)
            step_frame.pack(fill=tk.X, padx=20, pady=5)
            
            # Número y icono
            left_frame = ttk.Frame(step_frame)
            left_frame.pack(side=tk.LEFT, padx=(15, 10), pady=10)
            
            num_label = tk.Label(
                left_frame,
                text=str(i + 1),
                font=('Segoe UI', 12, 'bold'),
                bg='#dbeafe',
                fg='#1d4ed8',
                width=3,
                height=1
            )
            num_label.pack()
            
            icon_label = tk.Label(
                left_frame,
                text=step["icon"],
                font=('Segoe UI', 16),
                bg='#f0f9ff'
            )
            icon_label.pack(pady=(5, 0))
            
            # Contenido del paso
            content_step_frame = ttk.Frame(step_frame)
            content_step_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=10)
            
            step_title = tk.Label(
                content_step_frame,
                text=step["step"],
                font=('Segoe UI', 11, 'bold'),
                bg='#f0f9ff',
                fg='#1f2937'
            )
            step_title.pack(anchor=tk.W)
            
            step_desc = tk.Label(
                content_step_frame,
                text=step["desc"],
                font=('Segoe UI', 9),
                bg='#f0f9ff',
                fg='#6b7280',
                wraplength=500,
                justify=tk.LEFT
            )
            step_desc.pack(anchor=tk.W, pady=(2, 0))

    def create_faq_section(self):
        """Crear sección de preguntas frecuentes"""
        faq_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        faq_frame.pack(fill=tk.X, pady=20)
        
        # Título
        faq_title = tk.Label(
            faq_frame,
            text="Preguntas Frecuentes - NOM Eléctrica",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        faq_title.pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        # Preguntas
        for i, faq in enumerate(self.faqs):
            # Frame para cada pregunta
            question_frame = tk.Frame(faq_frame, bg='#fef3c7', relief="solid", borderwidth=1)
            question_frame.pack(fill=tk.X, padx=20, pady=5)
            
            # Botón de pregunta
            question_btn = tk.Button(
                question_frame,
                text=f"⚡ {faq['question']}",
                font=('Segoe UI', 10, 'bold'),
                bg='#fef3c7',
                fg='#92400e',
                border=0,
                anchor="w",
                padx=15,
                pady=10,
                command=lambda idx=i: self.toggle_faq(idx)
            )
            question_btn.pack(fill=tk.X)
            
            # Frame para la respuesta (inicialmente oculto)
            answer_frame = tk.Frame(question_frame, bg='white')
            
            answer_label = tk.Label(
                answer_frame,
                text=faq['answer'],
                font=('Segoe UI', 10),
                bg='white',
                fg='#374151',
                wraplength=700,
                justify=tk.LEFT
            )
            answer_label.pack(anchor=tk.W, padx=15, pady=15)
            
            # Almacenar referencias para toggle
            setattr(self, f'question_btn_{i}', question_btn)
            setattr(self, f'answer_frame_{i}', answer_frame)

    def toggle_faq(self, index):
        """Alternar visibilidad de respuesta FAQ"""
        answer_frame = getattr(self, f'answer_frame_{index}')
        question_btn = getattr(self, f'question_btn_{index}')
        
        if answer_frame.winfo_viewable():
            answer_frame.pack_forget()
            question_btn.configure(text=f"⚡ {self.faqs[index]['question']}")
        else:
            answer_frame.pack(fill=tk.X, after=question_btn)
            question_btn.configure(text=f"🔻 {self.faqs[index]['question']}")

    def open_calculator(self):
        """Abrir calculadora eléctrica simplificada"""
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Calculadora Eléctrica Rápida")
        calc_window.geometry("400x300")
        calc_window.configure(bg='white')
        
        # Título
        title_label = tk.Label(
            calc_window,
            text="🧮 Calculadora de Corriente",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#1f2937'
        )
        title_label.pack(pady=20)
        
        # Entradas
        tk.Label(calc_window, text="Potencia (W):", bg='white').pack(anchor=tk.W, padx=50)
        power_entry = tk.Entry(calc_window, font=('Segoe UI', 10))
        power_entry.pack(pady=5)
        
        tk.Label(calc_window, text="Voltaje (V):", bg='white').pack(anchor=tk.W, padx=50)
        voltage_entry = tk.Entry(calc_window, font=('Segoe UI', 10))
        voltage_entry.pack(pady=5)
        
        tk.Label(calc_window, text="Factor de Potencia:", bg='white').pack(anchor=tk.W, padx=50)
        fp_entry = tk.Entry(calc_window, font=('Segoe UI', 10))
        fp_entry.pack(pady=5)
        fp_entry.insert(0, "0.85")
        
        # Resultado
        result_label = tk.Label(
            calc_window,
            text="Corriente: -- A",
            font=('Segoe UI', 12, 'bold'),
            bg='#f0f9ff',
            fg='#1d4ed8',
            relief="solid",
            borderwidth=1,
            pady=10
        )
        result_label.pack(pady=20, padx=50, fill=tk.X)
        
        def calculate():
            try:
                P = float(power_entry.get())
                V = float(voltage_entry.get())
                fp = float(fp_entry.get())
                
                I = P / (V * fp)
                result_label.configure(text=f"Corriente: {I:.2f} A")
            except:
                result_label.configure(text="Error en los datos")
        
        calc_btn = tk.Button(
            calc_window,
            text="Calcular",
            command=calculate,
            bg='#f59e0b',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=5
        )
        calc_btn.pack(pady=10)

    def download_nom(self):
        """Simular descarga de NOM"""
        messagebox.showinfo(
            "Descarga NOM-001-SEDE-2012",
            "La descarga de la Norma Oficial Mexicana NOM-001-SEDE-2012 comenzará en breve.\n\n"
            "Incluye: Texto completo, tablas normativas y ejemplos de aplicación.\n\n"
            "Nota: Esta es una simulación para efectos de demostración."
        )

# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    app = NOMElectricalInterface(root)
    
    # Centrar ventana en pantalla
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()