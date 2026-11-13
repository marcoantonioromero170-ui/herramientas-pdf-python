# -*- coding: utf-8 -*-
"""Une un PDF base con cada otro PDF de la carpeta del script.
Instalar dependencia una sola vez: py -m pip install pypdf
"""
from pathlib import Path
import tempfile


def main():
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print('Falta instalar pypdf. Ejecuta en CMD: py -m pip install pypdf')
        return

    carpeta = Path(__file__).resolve().parent
    archivos = sorted(
        (p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() == '.pdf'),
        key=lambda p: p.name.casefold(),
    )
    print(f'Carpeta: {carpeta}\n')
    if len(archivos) < 2:
        print('Coloca al menos dos PDF junto al script: el base y otro para unir.')
        return
    for numero, archivo in enumerate(archivos, 1):
        print(f'{numero}. {archivo.name}')

    while True:
        opcion = input('\nNúmero del PDF BASE (0 para salir): ').strip()
        if opcion == '0':
            return
        if opcion.isdigit() and 1 <= int(opcion) <= len(archivos):
            base = archivos[int(opcion) - 1]
            break
        print('Ingresa un número válido de la lista.')

    def abrir_pdf(ruta):
        lector = PdfReader(str(ruta))
        if lector.is_encrypted and not lector.decrypt(''):
            raise ValueError('El PDF tiene contraseña. Guarda una copia sin contraseña para utilizarlo.')
        if not len(lector.pages):
            raise ValueError('El PDF no contiene páginas.')
        return lector

    lector_base = abrir_pdf(base)
    # Los resultados quedan fuera de la lista de entrada de futuras ejecuciones.
    # Cada ejecución usa una carpeta nueva para conservar resultados anteriores.
    salida = Path(tempfile.mkdtemp(prefix='PDFs_unidos_', dir=carpeta))
    print(f'\nPDF base: {base.name}')
    print(f'Resultados: {salida}\n')
    correctos = 0
    errores = []
    for archivo in archivos:
        if archivo == base:
            continue
        destino = salida / f'{archivo.stem}_{base.stem}.pdf'
        escritor = PdfWriter()
        try:
            lector_otro = abrir_pdf(archivo)
            escritor.append(lector_otro)
            escritor.append(lector_base)
            # Exclusivo: nunca sobrescribir un archivo existente.
            with destino.open('xb') as documento:
                try:
                    escritor.write(documento)
                except BaseException:
                    documento.close()
                    destino.unlink(missing_ok=True)
                    raise
            correctos += 1
            print(f'Creado: {destino.name}')
        except Exception as error:
            errores.append(archivo.name)
            print(f'ERROR con {archivo.name}: {error}')
        finally:
            escritor.close()
    print(f'\nFinalizado: {correctos} PDF creados; {len(errores)} con error.')
    print('Los archivos originales se conservan.')
    print(f'Carpeta de salida: {salida}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperación cancelada.')
    except Exception as error:
        print(f'\nNo se pudo completar la operación: {error}')
    finally:
        try:
            input('\nPresiona Enter para cerrar...')
        except (EOFError, KeyboardInterrupt):
            pass
