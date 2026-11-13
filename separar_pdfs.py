# -*- coding: utf-8 -*-
"""Divide un PDF ubicado junto a este script. Requiere: py -m pip install pypdf"""
from pathlib import Path
from getpass import getpass
import re
import tempfile
import sys


def leer_rangos(texto, total):
    """Cada elemento separado por coma genera un PDF independiente."""
    rangos = []
    for parte in texto.split(','):
        coincidencia = re.fullmatch(r'\s*(\d+)\s*(?:-\s*(\d+)\s*)?', parte)
        if not coincidencia:
            raise ValueError('Usa páginas o rangos separados por comas: 1-3, 4-7, 8.')
        inicio = int(coincidencia[1])
        fin = int(coincidencia[2] or coincidencia[1])
        if not 1 <= inicio <= fin <= total:
            raise ValueError(f'Cada rango debe estar entre 1 y {total}, en orden ascendente.')
        rangos.append((inicio, fin))
    return rangos


def main():
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print('Falta instalar pypdf. Ejecuta en CMD:')
        print('    py -m pip install pypdf')
        return

    carpeta = Path(__file__).resolve().parent
    archivos = sorted((p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() == '.pdf'),
                      key=lambda p: p.name.lower())
    print(f'Carpeta del script: {carpeta}\n')
    if not archivos:
        print('No hay archivos PDF en esta carpeta. Coloca tus PDF junto al script.')
        return
    for numero, archivo in enumerate(archivos, 1):
        print(f'{numero}. {archivo.name}')
    while True:
        respuesta = input('\nNúmero del PDF a dividir (0 para salir): ').strip()
        if respuesta == '0':
            return
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(archivos):
            archivo = archivos[int(respuesta) - 1]
            break
        print('Selecciona un número de la lista.')

    with archivo.open('rb') as origen:
        lector = PdfReader(origen)
        if lector.is_encrypted:
            if not lector.decrypt(''):
                if not lector.decrypt(getpass('Contraseña del PDF: ')):
                    print('Contraseña incorrecta.')
                    return
        total = len(lector.pages)
        print(f'\nSeleccionado: {archivo.name} ({total} páginas)')
        print('Cada rango creará un archivo. Ejemplo: 1-3, 4-7, 8')
        print('Usa la posición de las páginas en el PDF, empezando por 1.')
        print('Las páginas no indicadas no se exportarán. El original se conserva.')
        while True:
            respuesta = input('\nRangos (o 0 para salir): ').strip()
            if respuesta == '0':
                return
            try:
                rangos = leer_rangos(respuesta, total)
                break
            except ValueError as error:
                print(error)
        # Una carpeta nueva por ejecución evita sobrescribir resultados anteriores.
        salida = Path(tempfile.mkdtemp(prefix=f'{archivo.stem[:80]}_dividido_', dir=carpeta))
        print(f'\nCarpeta de salida: {salida}')
        for indice, (inicio, fin) in enumerate(rangos, 1):
            destino = salida / f'parte_{indice:02d}_paginas_{inicio}-{fin}.pdf'
            escritor = PdfWriter()
            try:
                for pagina in range(inicio - 1, fin):
                    escritor.add_page(lector.pages[pagina])
                with destino.open('xb') as documento:
                    escritor.write(documento)
            finally:
                escritor.close()
            print(f'Creado: {destino.name}')
        print(f'\nListo: se generaron {len(rangos)} archivos PDF.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperación cancelada.')
    except Exception as error:
        print(f'\nNo se pudo completar la división: {error}')
        print('Revisa el archivo, los permisos y el espacio disponible.')
    finally:
        try:
            input('\nPresiona Enter para cerrar...')
        except (EOFError, KeyboardInterrupt):
            pass
