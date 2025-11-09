"""
Generador de PDFs para Development Diary
Convierte entradas markdown a PDFs con formato bonito
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from datetime import datetime
import markdown2
import re


class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Configura estilos personalizados"""
        # Título principal
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#6b21a8'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))

        # Subtítulo
        if 'CustomHeading2' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomHeading2',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#9333ea'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            ))

        # Texto normal mejorado
        if 'CustomBody' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBody',
                parent=self.styles['BodyText'],
                fontSize=11,
                leading=16,
                spaceAfter=8,
                fontName='Helvetica'
            ))

        # Código (renombrado para evitar conflicto)
        if 'CustomCode' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomCode',
                parent=self.styles['BodyText'],
                fontSize=9,
                textColor=colors.HexColor('#1e293b'),
                backColor=colors.HexColor('#f1f5f9'),
                borderPadding=10,
                fontName='Courier',
                leftIndent=10,
                rightIndent=10
            ))

    def generate_single_entry_pdf(self, entry_data, output_path):
        """
        Genera PDF de una sola entrada

        Args:
            entry_data: Dict con datos de la entrada
            output_path: Ruta donde guardar el PDF
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []

        # Header
        story.append(Paragraph("Development Diary", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))

        # Metadata table
        metadata = [
            ['📁 Proyecto:', entry_data.get('proyecto', 'N/A')],
            ['🌿 Rama:', entry_data.get('rama', 'N/A')],
            ['👤 Autor:', entry_data.get('autor', 'N/A')],
            ['📅 Fecha:', entry_data.get('fecha', 'N/A')],
        ]

        t = Table(metadata, colWidths=[1.5 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e8ff')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6b21a8')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e9d5ff')),
        ]))

        story.append(t)
        story.append(Spacer(1, 0.3 * inch))

        # Título de la entrada
        title = entry_data.get('commit_problema', 'Entrada de desarrollo')
        story.append(Paragraph(title, self.styles['CustomHeading2']))
        story.append(Spacer(1, 0.1 * inch))

        # Contenido (parsear markdown simple)
        content = entry_data.get('content', '')
        story.extend(self.parse_markdown_to_flowables(content))

        # Construir PDF
        doc.build(story)
        print(f"✅ PDF generado: {output_path}")

    def generate_branch_pdf(self, entries, branch_name, project_name, output_path):
        """
        Genera PDF con todas las entradas de una rama

        Args:
            entries: Lista de entradas ordenadas por fecha
            branch_name: Nombre de la rama
            project_name: Nombre del proyecto
            output_path: Ruta donde guardar el PDF
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []

        # Portada
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph("Development Diary", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph(
            f"Proyecto: {project_name}",
            self.styles['CustomHeading2']
        ))
        story.append(Paragraph(
            f"Rama: {branch_name}",
            self.styles['CustomHeading2']
        ))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph(
            f"Total de entradas: {len(entries)}",
            self.styles['CustomBody']
        ))
        story.append(Paragraph(
            f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            self.styles['CustomBody']
        ))

        story.append(PageBreak())

        # Índice
        story.append(Paragraph("📋 Índice", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))

        for i, entry in enumerate(entries, 1):
            title = entry.get('commit_problema', 'Sin título')
            fecha = entry.get('fecha', '')
            story.append(Paragraph(
                f"{i}. {title} <i>({fecha})</i>",
                self.styles['CustomBody']
            ))

        story.append(PageBreak())

        # Entradas
        for i, entry in enumerate(entries, 1):
            story.append(Paragraph(
                f"Entrada {i}/{len(entries)}",
                self.styles['CustomHeading2']
            ))
            story.append(Spacer(1, 0.1 * inch))

            # Metadata
            metadata = [
                ['📅 Fecha:', entry.get('fecha', 'N/A')],
                ['💡 Commit:', entry.get('commit_problema', 'N/A')],
                ['👤 Autor:', entry.get('autor', 'N/A')],
            ]

            t = Table(metadata, colWidths=[1.2 * inch, 4.3 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e8ff')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6b21a8')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e9d5ff')),
            ]))

            story.append(t)
            story.append(Spacer(1, 0.2 * inch))

            # Contenido
            content = entry.get('content', '')
            story.extend(self.parse_markdown_to_flowables(content))

            if i < len(entries):
                story.append(PageBreak())

        # Construir PDF
        doc.build(story)
        print(f"✅ PDF de rama generado: {output_path}")

    def parse_markdown_to_flowables(self, markdown_text):
        """
        Convierte markdown a elementos PDF (simple)

        Args:
            markdown_text: Texto en formato markdown

        Returns:
            Lista de flowables para ReportLab
        """
        flowables = []

        # Eliminar frontmatter
        if markdown_text.startswith('---'):
            parts = markdown_text.split('---', 2)
            if len(parts) >= 3:
                markdown_text = parts[2]

        # Dividir en líneas
        lines = markdown_text.split('\n')

        in_code_block = False
        code_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                flowables.append(Spacer(1, 0.1 * inch))
                continue

            # Code blocks
            if line.startswith('```'):
                if in_code_block:
                    # Fin del bloque de código
                    code_text = '\n'.join(code_lines)
                    flowables.append(Paragraph(
                        f"<font face='Courier' size='9'>{code_text}</font>",
                        self.styles['CustomCode']
                    ))
                    flowables.append(Spacer(1, 0.1 * inch))
                    code_lines = []
                in_code_block = not in_code_block
                continue

            if in_code_block:
                code_lines.append(line)
                continue

            # Headers
            if line.startswith('# '):
                text = line.replace('# ', '')
                flowables.append(Paragraph(text, self.styles['CustomTitle']))
                flowables.append(Spacer(1, 0.1 * inch))
            elif line.startswith('## '):
                text = line.replace('## ', '')
                flowables.append(Paragraph(text, self.styles['CustomHeading2']))
            elif line.startswith('### '):
                text = line.replace('### ', '')
                flowables.append(Paragraph(f"<b>{text}</b>", self.styles['CustomBody']))

            # Listas
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:]
                flowables.append(Paragraph(f"• {text}", self.styles['CustomBody']))

            # Código inline
            elif '`' in line:
                text = line.replace('`', '<font face="Courier" color="#6b21a8">')
                text = text.replace('`', '</font>')
                flowables.append(Paragraph(text, self.styles['CustomBody']))

            # Texto normal
            else:
                # Procesar negritas y cursivas
                text = line
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

                if text.strip():
                    flowables.append(Paragraph(text, self.styles['CustomBody']))

        return flowables