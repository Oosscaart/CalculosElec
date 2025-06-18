# EXPORTADOR.PY CON FUENTES CENTURY GOTHIC Y ENCABEZADO TIPO CARTA

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import os
import locale

# Configurar locale para fechas en español
try:
    locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        locale.setlocale(locale.LC_TIME, '')

# Importar reportlab para PDF real
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from PIL import Image as PILImage  # Para manejar proporciones del logo
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class VentanaDatosProyecto:
    def __init__(self, parent):
        self.parent = parent
        self.datos = {}
        self.resultado = False
        
        # Crear ventana modal
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Datos del Proyecto")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        self.setup_ui()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (400 // 2)
        self.ventana.geometry(f"500x400+{x}+{y}")
    
    def setup_ui(self):
        main_frame = tk.Frame(self.ventana, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="DATOS DEL PROYECTO", 
                              font=('Century Gothic', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        # Campos de entrada
        fields_frame = tk.Frame(main_frame, bg='#f0f0f0')
        fields_frame.pack(fill='x', pady=(0, 20))
        
        # Cliente
        tk.Label(fields_frame, text="Cliente:", font=('Century Gothic', 10, 'bold'), bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        self.cliente_var = tk.StringVar(value="Cliente Ejemplo")
        tk.Entry(fields_frame, textvariable=self.cliente_var, width=40, font=('Century Gothic', 10)).grid(row=0, column=1, padx=10, pady=5)
        
        # Proyecto
        tk.Label(fields_frame, text="Proyecto:", font=('Century Gothic', 10, 'bold'), bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.proyecto_var = tk.StringVar(value="Instalación Eléctrica")
        tk.Entry(fields_frame, textvariable=self.proyecto_var, width=40, font=('Century Gothic', 10)).grid(row=1, column=1, padx=10, pady=5)
        
        # Ingeniero
        tk.Label(fields_frame, text="Ingeniero:", font=('Century Gothic', 10, 'bold'), bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        self.ingeniero_var = tk.StringVar(value="Ing. Responsable")
        tk.Entry(fields_frame, textvariable=self.ingeniero_var, width=40, font=('Century Gothic', 10)).grid(row=2, column=1, padx=10, pady=5)
        
        # Dirección
        tk.Label(fields_frame, text="Dirección:", font=('Century Gothic', 10, 'bold'), bg='#f0f0f0').grid(row=3, column=0, sticky='w', pady=5)
        self.direccion_var = tk.StringVar(value="Dirección del proyecto")
        tk.Entry(fields_frame, textvariable=self.direccion_var, width=40, font=('Century Gothic', 10)).grid(row=3, column=1, padx=10, pady=5)
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=20)
        
        tk.Button(button_frame, text="Generar PDF", command=self.generar_reporte,
                 font=('Century Gothic', 12, 'bold'), bg='#2c3e50', fg='white', 
                 cursor='hand2', pady=8).pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Button(button_frame, text="Cancelar", command=self.cancelar,
                 font=('Century Gothic', 12, 'bold'), bg='#e74c3c', fg='white', 
                 cursor='hand2', pady=8).pack(side='left', fill='x', expand=True, padx=(10, 0))
    
    def generar_reporte(self):
        """Genera el reporte con los datos ingresados."""
        self.datos = {
            'cliente': self.cliente_var.get().strip(),
            'proyecto': self.proyecto_var.get().strip(),
            'ingeniero': self.ingeniero_var.get().strip(),
            'direccion': self.direccion_var.get().strip(),
            'fecha': datetime.now().strftime('%d/%m/%Y')
        }
        
        if not self.datos['cliente'] or not self.datos['proyecto']:
            messagebox.showerror("Error", "Cliente y Proyecto son campos obligatorios")
            return
        
        self.resultado = True
        self.ventana.destroy()
    
    def cancelar(self):
        self.resultado = False
        self.ventana.destroy()


class ExportadorPDF:
    def __init__(self, historial_calculos):
        self.historial = historial_calculos or []
        self.font_registered = False
    
    def registrar_fuentes_century_gothic(self):
        """Registra las fuentes Century Gothic si están disponibles."""
        if self.font_registered:
            return True
        
        try:
            # Intentar registrar Century Gothic
            # Nota: Estas rutas pueden variar según el sistema
            font_paths = [
                # Windows
                "C:/Windows/Fonts/GOTHIC.TTF",
                "C:/Windows/Fonts/GOTHICB.TTF",
                # Rutas alternativas comunes
                "century-gothic.ttf",
                "CenturyGothic.ttf"
            ]
            
            # Intentar cargar fuente normal
            for path in font_paths:
                try:
                    if os.path.exists(path):
                        pdfmetrics.registerFont(TTFont('CenturyGothic', path))
                        break
                except:
                    continue
            
            # Intentar cargar fuente bold
            bold_paths = [
                "C:/Windows/Fonts/GOTHICB.TTF",
                "century-gothic-bold.ttf",
                "CenturyGothic-Bold.ttf"
            ]
            
            for path in bold_paths:
                try:
                    if os.path.exists(path):
                        pdfmetrics.registerFont(TTFont('CenturyGothic-Bold', path))
                        break
                except:
                    continue
            
            self.font_registered = True
            return True
            
        except Exception as e:
            print(f"No se pudo cargar Century Gothic: {e}")
            return False
    
    def get_font_name(self, bold=False):
        """Retorna el nombre de fuente a usar."""
        if self.registrar_fuentes_century_gothic():
            return 'CenturyGothic-Bold' if bold else 'CenturyGothic'
        else:
            # Fallback a fuentes disponibles
            return 'Helvetica-Bold' if bold else 'Helvetica'
    
    def verificar_logo_dimensiones(self, logo_path):
        """Función auxiliar para verificar las dimensiones del logo."""
        try:
            pil_logo = PILImage.open(logo_path)
            print(f"📐 Dimensiones del logo: {pil_logo.width}x{pil_logo.height} px")
            print(f"📐 Relación de aspecto: {pil_logo.width/pil_logo.height:.2f}")
            
            # Recomendaciones
            if pil_logo.width / pil_logo.height > 2:
                print("⚠️ Logo muy ancho - considere recortar")
            elif pil_logo.width / pil_logo.height < 0.5:
                print("⚠️ Logo muy alto - considere redimensionar")
            else:
                print("✅ Proporciones del logo adecuadas")
                
            return True
        except Exception as e:
            print(f"❌ Error al verificar logo: {e}")
            return False
    
    def exportar_reporte(self, parent_window=None):
        try:
            if not self.historial:
                messagebox.showwarning(
                    "Advertencia", 
                    "No hay cálculos para exportar. Realice al menos un cálculo."
                )
                return False
            
            # Verificar que reportlab esté disponible
            if not REPORTLAB_AVAILABLE:
                messagebox.showerror(
                    "Error", 
                    "Para exportar PDF se requiere la biblioteca 'reportlab'.\n\n"
                    "Instale con: pip install reportlab"
                )
                return False
            
            # Capturar datos del proyecto
            ventana_datos = VentanaDatosProyecto(parent_window)
            if parent_window:
                parent_window.wait_window(ventana_datos.ventana)
            
            if not ventana_datos.resultado:
                return False
            
            datos_proyecto = ventana_datos.datos
            
            # Solicitar ubicación de archivo PDF
            fecha_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"Memoria_Tecnica_{datos_proyecto['cliente'].replace(' ', '_')}_{fecha_hora}.pdf"
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[
                    ("Archivo PDF", "*.pdf"), 
                    ("Todos los archivos", "*.*")
                ],
                title="Guardar Memoria Técnica PDF como...",
                initialfile=nombre_archivo
            )
            
            if not filename:
                return False
            
            # Generar PDF real
            self.generar_pdf_memoria(filename, datos_proyecto)
            
            messagebox.showinfo(
                "Éxito", 
                f"Memoria Técnica PDF exportada exitosamente:\n{os.path.basename(filename)}"
            )
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar memoria técnica: {str(e)}")
            return False
    
    def generar_pdf_memoria(self, filename, datos):
        """Genera un PDF real usando reportlab con fuentes Century Gothic y encabezado corregido."""
        doc = SimpleDocTemplate(filename, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        story = []
        
        # Registrar fuentes Century Gothic
        self.registrar_fuentes_century_gothic()
        
        # Crear estilos personalizados con Century Gothic
        # TÍTULOS - Century Gothic 12
        title_style = ParagraphStyle(
            'CenturyTitle',
            fontName=self.get_font_name(bold=True),
            fontSize=12,
            leading=14,
            spaceAfter=20,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        )
        
        # SUBTÍTULOS - Century Gothic 11
        subtitle_style = ParagraphStyle(
            'CenturySubtitle',
            fontName=self.get_font_name(bold=True),
            fontSize=11,
            leading=13,
            spaceAfter=15,
            alignment=1,
            textColor=colors.darkblue
        )
        
        # TEXTO NORMAL JUSTIFICADO - Century Gothic 10
        normal_style = ParagraphStyle(
            'CenturyNormal',
            fontName=self.get_font_name(bold=False),
            fontSize=10,
            leading=12,
            spaceAfter=6,
            alignment=4  # Justificado
        )
        
        # TEXTO BOLD JUSTIFICADO - Century Gothic 10 Bold
        bold_style = ParagraphStyle(
            'CenturyBold',
            fontName=self.get_font_name(bold=True),
            fontSize=10,
            leading=12,
            spaceAfter=6,
            alignment=4  # Justificado
        )
        
        # ENCABEZADOS DE SECCIÓN - Century Gothic 11 (mantener alineados izquierda)
        section_style = ParagraphStyle(
            'CenturySection',
            fontName=self.get_font_name(bold=True),
            fontSize=11,
            leading=13,
            spaceAfter=10,
            alignment=0,  # Izquierda para encabezados
            textColor=colors.darkred
        )
        
        # ========== ENCABEZADO PROFESIONAL: LOGO IZQUIERDA + FECHA DERECHA ==========
        # === 1. Insertar el logo en la esquina superior izquierda ===
        logo_path = os.path.join("imagenes", "logo.png")
        if os.path.exists(logo_path):
            # Verificar dimensiones del logo (opcional)
            self.verificar_logo_dimensiones(logo_path)
            
            pil_logo = PILImage.open(logo_path)
            aspect_ratio = pil_logo.width / pil_logo.height
            max_height = 1.2 * inch
            logo_width = max_height * aspect_ratio
            
            # Limitar ancho máximo si es necesario
            if logo_width > 2.0 * inch:
                logo_width = 2.0 * inch
                max_height = logo_width / aspect_ratio
            
            logo_img = Image(logo_path, width=logo_width, height=max_height)
            logo_img.hAlign = 'LEFT'
            
            # Configurar fecha en español
            try:
                # Diccionario de meses en español
                meses_es = {
                    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
                    'April': 'abril', 'May': 'mayo', 'June': 'junio',
                    'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
                    'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
                }
                
                fecha_actual = datetime.now()
                mes_ingles = fecha_actual.strftime("%B")
                mes_espanol = meses_es.get(mes_ingles, mes_ingles.lower())
                fecha_formateada = f"Santiago de Querétaro, a {fecha_actual.day} de {mes_espanol} del {fecha_actual.year}"
                
            except Exception:
                fecha_formateada = f"Santiago de Querétaro, a {datetime.now().strftime('%d de %B del %Y')}"
            
            # Crear tabla con 2 columnas: logo izquierda, fecha derecha
            encabezado_data = [
                [logo_img, Paragraph(fecha_formateada, ParagraphStyle(
                    name='FechaDerecha',
                    fontName=self.get_font_name(),
                    fontSize=10,
                    alignment=2,  # Alineación derecha
                    textColor=colors.black
                ))]
            ]
            
            encabezado_tabla = Table(encabezado_data, colWidths=[3.5*inch, 3.5*inch])
            encabezado_tabla.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Logo alineado izquierda
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Fecha alineada derecha
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                # Sin bordes visibles
                ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ]))
            
            story.append(encabezado_tabla)
            story.append(Spacer(1, 20))
            
        else:
            # Si no hay logo, solo mostrar la fecha
            try:
                meses_es = {
                    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
                    'April': 'abril', 'May': 'mayo', 'June': 'junio',
                    'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
                    'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
                }
                
                fecha_actual = datetime.now()
                mes_ingles = fecha_actual.strftime("%B")
                mes_espanol = meses_es.get(mes_ingles, mes_ingles.lower())
                fecha_formateada = f"Santiago de Querétaro, a {fecha_actual.day} de {mes_espanol} del {fecha_actual.year}"
                
            except Exception:
                fecha_formateada = f"Santiago de Querétaro, a {datetime.now().strftime('%d de %B del %Y')}"
            
            story.append(Paragraph(fecha_formateada, ParagraphStyle(
                name='FechaSola',
                fontName=self.get_font_name(),
                fontSize=10,
                alignment=2,  # Alineación derecha
                spaceAfter=20
            )))
            print(f"⚠️ Logo no encontrado en: {logo_path}")
        
        # === 2. Título centrado debajo del logo y fecha ===
        story.append(Paragraph("MEMORIA TÉCNICA Y DESCRIPTIVA DE INSTALACIÓN ELÉCTRICA", ParagraphStyle(
            name='TituloCentro',
            fontName=self.get_font_name(bold=True),
            fontSize=13,
            alignment=1,  # Centrado
            leading=15,
            spaceAfter=5,
            textColor=colors.HexColor("#1a1a1a")
        )))
        
        story.append(Paragraph("NOM-001-SEDE-2012", ParagraphStyle(
            name='NormativaCentro',
            fontName=self.get_font_name(),
            fontSize=11,
            alignment=1,  # Centrado
            spaceAfter=25,
            textColor=colors.HexColor("#34495E")
        )))
        
        # ========== TABLA DE DATOS PROFESIONAL ALINEADA AL MARGEN ==========
        # Crear tabla con formato profesional: etiquetas azules compactas, valores amplios
        datos_tabla_profesional = Table([
            ['CLIENTE', datos['cliente']],
            ['DIRECCIÓN', datos['direccion']],
            ['PROYECTO', datos['proyecto']],
            ['RESPONSABLE', datos['ingeniero']]
        ], colWidths=[1.2*inch, 4.8*inch])  
        
        datos_tabla_profesional.setStyle(TableStyle([
            # Fondo azul marino para etiquetas (columna izquierda)
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#1B365D")),
            # Fondo blanco para valores (columna derecha)  
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            # Texto blanco en etiquetas
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            # Texto negro en valores
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            # Fuente bold para etiquetas
            ('FONTNAME', (0, 0), (0, -1), self.get_font_name(bold=True)),
            # Fuente normal para valores
            ('FONTNAME', (1, 0), (1, -1), self.get_font_name()),
            # Tamaño de fuente
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            # Alineación centrada en etiquetas
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            # Alineación izquierda en valores
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            # Alineación vertical centrada
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Padding horizontal
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            # PADDING VERTICAL REDUCIDO - FILAS MÁS DELGADAS
            ('TOPPADDING', (0, 0), (-1, -1), 4),    # ← Reducido de 8 a 4
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4), # ← Reducido de 8 a 4
            # Bordes negros para toda la tabla
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        # Tabla alineada al margen izquierdo (sin centrar)
        datos_tabla_profesional.hAlign = 'LEFT'
        
        story.append(datos_tabla_profesional)
        story.append(Spacer(1, 25))
        
        # Resumen ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", section_style))
        story.append(Paragraph(f"Total de cálculos realizados: {len(self.historial)}", normal_style))
        
        # Estadísticas del proyecto
        equipos = set()
        tipos_carga = set()
        cumplimiento = {'cumple': 0, 'no_cumple': 0}
        
        for calculo in self.historial:
            equipos.add(calculo.get('tipo_equipo', 'N/A'))
            tipos_carga.add(calculo.get('tipo_carga', 'derivado'))
            
            limite = 2 if calculo.get('tipo_carga') == 'alimentador' else 3
            if calculo.get('caida_p', 0) <= limite:
                cumplimiento['cumple'] += 1
            else:
                cumplimiento['no_cumple'] += 1
        
        story.append(Paragraph(f"Equipos analizados: {', '.join(sorted(equipos))}", normal_style))
        story.append(Paragraph(f"Tipos de circuitos: {', '.join(sorted(tipos_carga)).upper()}", normal_style))
        story.append(Paragraph(f"Cumplimiento normativo: {cumplimiento['cumple']} de {len(self.historial)} cálculos cumplen con los límites establecidos", normal_style))
        story.append(Spacer(1, 20))
        
        # OBJETIVO Y ALCANCE
        story.append(Paragraph("1. OBJETIVO Y ALCANCE DEL PROYECTO", section_style))
        
        story.append(Paragraph("1.1 OBJETIVO", bold_style))
        objetivo_text = """Desarrollar la memoria técnica y descriptiva de cálculo eléctrico para la instalación 
        de baja tensión, considerando los lineamientos establecidos en la Norma Oficial Mexicana 
        NOM-001-SEDE-2012 "Instalaciones Eléctricas (utilización)", con el fin de garantizar la 
        seguridad, funcionalidad y eficiencia del sistema eléctrico propuesto."""
        story.append(Paragraph(objetivo_text, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("1.2 ALCANCE", bold_style))
        alcance_text = """El presente documento comprende el análisis y cálculo de conductores eléctricos, 
        considerando criterios de ampacidad, caída de tensión, coordinación de protecciones y selección 
        de equipos de protección, aplicando factores de seguridad normativos para garantizar una 
        instalación confiable y segura."""
        story.append(Paragraph(alcance_text, normal_style))
        story.append(Spacer(1, 20))
        
        # NORMATIVAS APLICADAS
        story.append(Paragraph("2. NORMATIVAS Y CÓDIGOS APLICADOS", section_style))
        
        normativas_list = [
            "• NOM-001-SEDE-2012 Instalaciones Eléctricas (utilización)",
            "• Artículo 430-22: Capacidad de los conductores del circuito derivado para un solo motor",
            "• Artículo 450-3: Protección contra sobrecorriente de transformadores",
            "• Artículo 460-8: Capacidad de los conductores para capacitores",
            "• Artículo 445-5: Capacidad de los conductores para generadores",
            "• Artículo 210-19: Conductores - Requisitos mínimos de tamaño y capacidad",
            "• Artículo 215-2: Requisitos mínimos de capacidad y tamaño de alimentadores",
            "• Artículo 220-11: Cargas de motores en alimentadores",
            "• Artículo 240-12: Coordinación eléctrica",
            "• Artículo 250-122: Tamaño de los conductores de puesta a tierra del equipo",
            "• Tabla 310-15(b)(16): Ampacidades admisibles para conductores aislados",
            "• Tabla 310-15(b)(20): Ampacidades para conductores de un solo cable al aire libre"
        ]
        
        for normativa in normativas_list:
            story.append(Paragraph(normativa, normal_style))
        story.append(Spacer(1, 20))
        
        # METODOLOGÍA DE CÁLCULO
        story.append(Paragraph("3. METODOLOGÍA DE CÁLCULO", section_style))
        
        story.append(Paragraph("3.1 CRITERIOS GENERALES DE DISEÑO", bold_style))
        criterios_text = """La metodología aplicada se basa en el cumplimiento estricto de la normativa vigente, 
        considerando factores de seguridad, coordinación de protecciones y optimización del sistema eléctrico. 
        Se implementa un flujo de cálculo que garantiza la correcta selección de conductores y protecciones."""
        story.append(Paragraph(criterios_text, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("3.2 SECUENCIA DE CÁLCULO IMPLEMENTADA", bold_style))
        secuencia_list = [
            "1. Determinación de la corriente nominal del equipo o carga",
            "2. Aplicación del factor de seguridad normativo según tipo de equipo",
            "3. Selección del dispositivo de protección comercial",
            "4. Cálculo de corriente por conductor basado en la capacidad del interruptor",
            "5. Selección del calibre de conductor por criterio de ampacidad",
            "6. Verificación de caída de tensión según límites normativos",
            "7. Selección del conductor de tierra física según Tabla 250-122",
            "8. Evaluación de coordinación conductor-protección"
        ]
        
        for paso in secuencia_list:
            story.append(Paragraph(paso, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("3.3 FACTORES DE SEGURIDAD APLICADOS", bold_style))
        factores_table = Table([
            ['TIPO DE EQUIPO', 'FACTOR DE SEGURIDAD', 'ARTÍCULO NOM'],
            ['Motores', '125% (1.25)', 'Art. 430-22'],
            ['Transformadores', '125% (1.25)', 'Art. 450-3'],
            ['Capacitores', '135% (1.35)', 'Art. 460-8'],
            ['Generadores', '115% (1.15)', 'Art. 445-5'],
            ['Cargas generales', '125% (1.25)', 'Criterio general']
        ], colWidths=[2.5*inch, 2*inch, 1.5*inch])
        
        factores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.get_font_name(bold=True)),
            ('FONTNAME', (0, 1), (-1, -1), self.get_font_name(bold=False)),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(factores_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("3.4 LÍMITES DE CAÍDA DE TENSIÓN", bold_style))
        caida_table = Table([
            ['TIPO DE CIRCUITO', 'LÍMITE MÁXIMO', 'REFERENCIA NORMATIVA'],
            ['Circuitos derivados', '3%', 'Art. 210-19 FPN 4'],
            ['Alimentadores', '2%', 'Art. 215-2 FPN 2'],
            ['Total sistema (alimentador + derivado)', '5%', 'Criterio combinado']
        ], colWidths=[2.5*inch, 2*inch, 1.5*inch])
        
        caida_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.get_font_name(bold=True)),
            ('FONTNAME', (0, 1), (-1, -1), self.get_font_name(bold=False)),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(caida_table)
        story.append(Spacer(1, 20))
        
        # CONSIDERACIONES TÉCNICAS
        story.append(Paragraph("4. CONSIDERACIONES TÉCNICAS ESPECÍFICAS", section_style))
        
        story.append(Paragraph("4.1 SELECCIÓN DE CONDUCTORES", bold_style))
        conductores_text = """La selección de conductores se realizó considerando las tablas de ampacidad 
        de la NOM-001-SEDE-2012, específicamente la Tabla 310-15(b)(16) para instalaciones en conduit 
        y la Tabla 310-15(b)(20) para instalaciones en charola portacables. Se consideró temperatura 
        de operación de 75°C para conductores THW."""
        story.append(Paragraph(conductores_text, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("4.2 COORDINACIÓN DE PROTECCIONES", bold_style))
        protecciones_text = """Los dispositivos de protección fueron seleccionados considerando los 
        factores de protección específicos para cada tipo de carga, garantizando la coordinación 
        adecuada entre la capacidad del interruptor y la ampacidad del conductor, evitando la 
        aplicación duplicada de factores de seguridad."""
        story.append(Paragraph(protecciones_text, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("4.3 SISTEMA DE PUESTA A TIERRA", bold_style))
        tierra_text = """El dimensionamiento del conductor de puesta a tierra se realizó conforme 
        a la Tabla 250-122 de la NOM-001-SEDE-2012, seleccionando el calibre apropiado basado en 
        la capacidad del dispositivo de protección contra sobrecorriente que protege los conductores 
        del circuito."""
        story.append(Paragraph(tierra_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Cálculos detallados
        story.append(Paragraph("MEMORIA DE CÁLCULO DETALLADA", section_style))
        
        for i, calculo in enumerate(self.historial, 1):
            # Título del cálculo - Century Gothic 11
            story.append(Paragraph(f"CÁLCULO #{i:02d} - {calculo.get('tipo_equipo', 'N/A').upper()}", 
                                 subtitle_style))
            
            # Datos de entrada
            entrada_data = [
                ['PARÁMETRO', 'VALOR'],
                ['Tipo de equipo', f"{calculo.get('tipo_equipo', 'N/A')} {calculo.get('tipo_circuito', 'N/A')}"],
                ['Tipo de carga', calculo.get('tipo_carga', 'derivado').upper()],
                ['Potencia', f"{calculo.get('valor_potencia', 'N/A')} {calculo.get('unidad_potencia', '')}"],
                ['Tensión nominal', f"{calculo.get('voltaje', 'N/A')} V"],
                ['Longitud', f"{calculo.get('longitud', 'N/A')} m"],
                ['Material conductor', calculo.get('material', 'N/A').capitalize()],
                ['Conductores por fase', str(calculo.get('num_conductores', 'N/A'))],
                ['Tipo de canalización', calculo.get('canalizacion', 'N/A')]
            ]
            
            entrada_table = Table(entrada_data, colWidths=[2.5*inch, 3.5*inch])
            entrada_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), self.get_font_name(bold=True)),  # Encabezados bold
                ('FONTNAME', (0, 1), (0, -1), self.get_font_name(bold=True)),  # Primera columna bold
                ('FONTNAME', (1, 1), (1, -1), self.get_font_name(bold=False)), # Segunda columna normal
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Todo Century Gothic 10
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(entrada_table)
            story.append(Spacer(1, 15))
            
            # Resultados
            try:
                if isinstance(calculo.get('interruptor_info'), dict):
                    cap_int = calculo['interruptor_info']['capacidad']
                    tipo_prot = calculo['interruptor_info']['tipo_proteccion']
                else:
                    cap_int = calculo.get('corriente_interruptor', 'N/A')
                    tipo_prot = 'N/A'
            except:
                cap_int = 'N/A'
                tipo_prot = 'N/A'
            
            resultado_data = [
                ['RESULTADO', 'VALOR'],
                ['Corriente nominal', f"{calculo.get('corriente', 0):.2f} A"],
                ['Corriente corregida', f"{calculo.get('corriente_para_proteccion', 0):.2f} A"],
                ['Interruptor', f"{cap_int} A - {tipo_prot}"],
                ['Calibre conductor', f"{calculo.get('calibre', 'N/A')} AWG {calculo.get('material', '').capitalize()}"],
                ['Tierra física', f"{calculo.get('calibre_tierra', 'N/A')} AWG"],
                ['Caída de tensión', f"{calculo.get('caida_v', 0):.3f} V ({calculo.get('caida_p', 0):.2f}%)"]
            ]
            
            # Evaluación normativa
            tipo_carga = calculo.get('tipo_carga', 'derivado')
            limite = 2 if tipo_carga == 'alimentador' else 3
            normativa = "Art. 215-2" if tipo_carga == 'alimentador' else "Art. 210-19"
            cumple = "✓ CUMPLE" if calculo.get('caida_p', 0) <= limite else "✗ EXCEDE"
            
            resultado_data.append(['Evaluación normativa', f"{cumple} (Límite: {limite}% - {normativa})"])
            
            resultado_table = Table(resultado_data, colWidths=[2.5*inch, 3.5*inch])
            resultado_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgreen),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), self.get_font_name(bold=True)),  # Encabezados bold
                ('FONTNAME', (0, 1), (0, -1), self.get_font_name(bold=True)),  # Primera columna bold
                ('FONTNAME', (1, 1), (1, -1), self.get_font_name(bold=False)), # Segunda columna normal
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Todo Century Gothic 10
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(resultado_table)
            story.append(Spacer(1, 25))
        
        # Referencias normativas MEJORADAS
        story.append(Paragraph("REFERENCIAS NORMATIVAS Y BIBLIOGRAFÍA", section_style))
        
        story.append(Paragraph("NORMAS OFICIALES MEXICANAS:", bold_style))
        story.append(Paragraph("• NOM-001-SEDE-2012, Instalaciones Eléctricas (utilización). Secretaría de Energía. Diario Oficial de la Federación, 29 de noviembre de 2012.", normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("ARTÍCULOS ESPECÍFICOS APLICADOS:", bold_style))
        
        articulos_data = [
            ['ARTÍCULO', 'DESCRIPCIÓN', 'APLICACIÓN'],
            ['Art. 430-22', 'Capacidad de conductores para un solo motor', 'Cálculo de motores'],
            ['Art. 450-3', 'Protección de transformadores', 'Cálculo de transformadores'],
            ['Art. 460-8', 'Capacidad de conductores para capacitores', 'Banco de capacitores'],
            ['Art. 445-5', 'Capacidad de conductores para generadores', 'Plantas de emergencia'],
            ['Art. 210-19', 'Conductores de circuitos derivados', 'Límites de caída - derivados'],
            ['Art. 215-2', 'Capacidad mínima de alimentadores', 'Límites de caída - alimentadores'],
            ['Art. 220-11', 'Cargas de motores en alimentadores', 'Factores de demanda'],
            ['Art. 240-12', 'Coordinación eléctrica', 'Protecciones en cascada'],
            ['Art. 250-122', 'Conductores de puesta a tierra', 'Dimensionamiento de tierras']
        ]
        
        articulos_table = Table(articulos_data, colWidths=[1.2*inch, 2.8*inch, 2*inch])
        articulos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.get_font_name(bold=True)),
            ('FONTNAME', (0, 1), (-1, -1), self.get_font_name(bold=False)),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(articulos_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("TABLAS NORMATIVAS UTILIZADAS:", bold_style))
        story.append(Paragraph("• Tabla 310-15(b)(16): Ampacidades admisibles de conductores aislados para tensiones de 0 a 2000 V y 60°C a 90°C. No más de tres conductores portadores de corriente en una canalización, cable o directamente enterrados.", normal_style))
        story.append(Paragraph("• Tabla 310-15(b)(20): Ampacidades admisibles de conductores aislados de un solo cable al aire libre para tensiones de 0 a 2000 V y 60°C a 90°C.", normal_style))
        story.append(Paragraph("• Tabla 250-122: Tamaño mínimo de los conductores de puesta a tierra del equipo para canalizaciones y equipos.", normal_style))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("CRITERIOS DE INTERPRETACIÓN NORMATIVA:", bold_style))
        story.append(Paragraph("• Se aplicó la metodología de cálculo establecida en la NOM-001-SEDE-2012, considerando factores de corrección por temperatura y agrupamiento cuando aplique.", normal_style))
        story.append(Paragraph("• Los factores de demanda se aplicaron únicamente en alimentadores según lo establecido en el Artículo 220-11.", normal_style))
        story.append(Paragraph("• La coordinación de protecciones se verificó conforme al Artículo 240-12 para garantizar selectividad del sistema.", normal_style))
        story.append(Spacer(1, 20))
        
        # CONCLUSIONES Y RECOMENDACIONES
        story.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES TÉCNICAS", section_style))
        
        story.append(Paragraph("CONCLUSIONES:", bold_style))
        conclusiones_text = f"""Con base en los cálculos realizados y presentados en este documento, se concluye que:

1. Se analizaron un total de {len(self.historial)} circuitos eléctricos, de los cuales {cumplimiento['cumple']} cumplen con los límites normativos de caída de tensión establecidos.

2. La metodología aplicada garantiza el cumplimiento de la NOM-001-SEDE-2012 en todos sus aspectos técnicos relevantes.

3. Los conductores seleccionados presentan ampacidades adecuadas considerando los factores de seguridad normativos.

4. El sistema de protecciones propuesto garantiza la coordinación adecuada y la seguridad de la instalación."""
        
        story.append(Paragraph(conclusiones_text, normal_style))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("RECOMENDACIONES:", bold_style))
        recomendaciones_text = """Se recomienda:

• Implementar un programa de mantenimiento preventivo para garantizar el funcionamiento óptimo del sistema eléctrico.

• Realizar verificaciones periódicas de las conexiones y dispositivos de protección.

• Considerar estudios de coordinación de protecciones para sistemas complejos con múltiples niveles de alimentación.

• Evaluar la implementación de sistemas de monitoreo para instalaciones críticas.

• Verificar las condiciones ambientales de operación para confirmar los factores de corrección aplicados."""
        
        story.append(Paragraph(recomendaciones_text, normal_style))
        story.append(Spacer(1, 30))
        
        # Pie de página profesional con Century Gothic
        story.append(Spacer(1, 30))
        story.append(PageBreak())
        
        # PÁGINA FINAL - VALIDACIÓN Y FIRMAS
        story.append(Paragraph("VALIDACIÓN TÉCNICA Y RESPONSABILIDADES", section_style))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("DECLARACIÓN DE RESPONSABILIDAD TÉCNICA", bold_style))
        declaracion_text = """El presente documento ha sido elaborado bajo los más estrictos criterios técnicos 
        y normativos, aplicando la metodología establecida en la NOM-001-SEDE-2012. Los cálculos y 
        especificaciones contenidos en esta memoria técnica garantizan el cumplimiento de los requisitos 
        de seguridad, funcionalidad y eficiencia para la instalación eléctrica proyectada."""
        story.append(Paragraph(declaracion_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Tabla de firmas
        firmas_table = Table([
            ['', ''],
            ['_________________________', '_________________________'],
            [f'{datos["ingeniero"]}', 'Vo.Bo. Cliente'],
            ['Ingeniero Responsable', f'{datos["cliente"]}'],
            ['Hertz Ingeniería & Servicios Eléctricos', ''],
            [f'Fecha: {datos["fecha"]}', f'Fecha: _______________']
        ], colWidths=[3*inch, 3*inch])
        
        firmas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.get_font_name(bold=False)),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(firmas_table)
        story.append(Spacer(1, 30))
        
        # Información corporativa final
        story.append(Paragraph("INFORMACIÓN CORPORATIVA", bold_style))
        story.append(Paragraph("HERTZ INGENIERÍA & SERVICIOS ELÉCTRICOS S.A DE C.V", bold_style))
        story.append(Paragraph("Especialistas en Instalaciones Eléctricas de Baja y Media Tensión", normal_style))
        story.append(Paragraph("Cálculos y Proyectos conforme a NOM-001-SEDE-2012", normal_style))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(f"Proyecto: {datos['proyecto']}", normal_style))
        story.append(Paragraph(f"Cliente: {datos['cliente']}", normal_style))
        story.append(Paragraph(f"Ubicación: {datos['direccion']}", normal_style))
        story.append(Paragraph(f"Ingeniero Responsable: {datos['ingeniero']}", normal_style))
        story.append(Paragraph(f"Fecha de Elaboración: {datos['fecha']}", normal_style))
        
        # Construir PDF
        doc.build(story)


# Función de prueba mejorada
def test_exportador():
    """Función de prueba - eliminar después de verificar."""
    if REPORTLAB_AVAILABLE:
        print("✅ ExportadorPDF con Century Gothic y encabezado tipo carta importado correctamente")
        exportador = ExportadorPDF([])
        
        # Verificar si existe el logo
        logo_path = os.path.join("imagenes", "logo.png")
        if os.path.exists(logo_path):
            print("✅ Logo encontrado en: imagenes/logo.png")
            exportador.verificar_logo_dimensiones(logo_path)
        else:
            print("⚠️ Logo no encontrado. Crear carpeta 'imagenes' con 'logo.png'")
        
        print("✅ Instancia creada exitosamente")
        print("📋 Requiere: pip install reportlab pillow")
        print("📄 Encabezado tipo carta: Fecha alineada derecha + Logo izquierda + Título centrado")
        print("🗓️ Formato de fecha: 'Santiago de Querétaro, a DD de MM del AAAA'")
        print("📏 Filas de tabla más delgadas con padding reducido (4pt)")
        return True
    else:
        print("❌ Reportlab no disponible. Instale con: pip install reportlab pillow")
        return False

if __name__ == "__main__":
    test_exportador()