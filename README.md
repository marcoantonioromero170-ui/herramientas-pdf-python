# Herramientas PDF en Python

Dos scripts interactivos para combinar y dividir archivos PDF desde la terminal.

## Instalación

Instala Python 3 y la biblioteca pypdf. En Windows, ejecuta:

```powershell
py -m pip install pypdf
```

En macOS o Linux, usa `python3` en lugar de `py`.

## Uso

Coloca tus PDFs en la misma carpeta que el script.

### Combinar archivos con un PDF base

Ejecuta `py unir_pdf_base.py` y selecciona el documento base. Si tienes `Base.pdf`, `A.pdf` y `B.pdf`, el script genera `A_Base.pdf` y `B_Base.pdf`, con el PDF base al final de cada archivo.

### Dividir por rangos de páginas

Ejecuta `py separar_pdfs.py`, selecciona el PDF y escribe los rangos separados por comas. Por ejemplo, `1-3, 4-7, 8` genera tres PDFs independientes. La numeración empieza en 1.

Ambos scripts conservan los originales y guardan cada ejecución en una carpeta nueva junto al script.
