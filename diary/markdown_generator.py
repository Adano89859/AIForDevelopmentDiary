"""
Generador de archivos Markdown para entradas del diario
"""

from datetime import datetime


class MarkdownGenerator:
    def generate(self, entry_data, improved_notes):
        """
        Genera el contenido Markdown de una entrada

        Args:
            entry_data: Datos de la entrada (dict)
            improved_notes: Notas mejoradas por la IA (str)

        Returns:
            str: Contenido Markdown completo
        """
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d %H:%M:%S")

        # Frontmatter YAML
        frontmatter = f"""---
autor: {entry_data['author'] or 'Anónimo'}
proyecto: {entry_data['project']}
rama: {entry_data['branch']}
commit_problema: {entry_data['commit_problem']}
fecha: {fecha}
---

"""

        # Cuerpo del documento
        body = f"""# {entry_data['commit_problem'] or 'Entrada de desarrollo'}

{improved_notes}

---

## 📝 Notas Originales
```
{entry_data['notes']}
```

---
*Generado por Development Diary el {fecha}*
"""

        return frontmatter + body