"""
Development Diary - Build Script
Script para crear el instalador ejecutable
"""

import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path


def clean_build():
    """Limpia directorios de builds anteriores"""
    print("🧹 Limpiando builds anteriores...")

    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   ✓ Eliminado {dir_name}/")

    # Limpiar archivos .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   ✓ Eliminado {spec_file}")


def build_executable():
    """Construye el ejecutable con PyInstaller"""
    print("\n📦 Construyendo ejecutable...")

    # Configuración de PyInstaller
    pyinstaller_args = [
        'app.py',  # Archivo principal
        '--name=DevelopmentDiary',  # Nombre del ejecutable
        '--onefile',  # Todo en un solo archivo
        '--windowed',  # Sin ventana de consola (opcional)
        '--icon=static/favicon.ico',  # Icono (si lo tienes)

        # Incluir carpetas necesarias
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=config;config',

        # Incluir módulos ocultos
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=requests',
        '--hidden-import=jinja2',

        # Optimizaciones
        '--clean',
        '--noconfirm',
    ]

    # Ajustar para Windows/Linux
    if sys.platform == 'win32':
        pyinstaller_args[3] = '--add-data=templates;templates'
        pyinstaller_args[4] = '--add-data=static;static'
        pyinstaller_args[5] = '--add-data=config;config'
    else:
        pyinstaller_args[3] = '--add-data=templates:templates'
        pyinstaller_args[4] = '--add-data=static:static'
        pyinstaller_args[5] = '--add-data=config:config'

    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("\n✅ Ejecutable creado exitosamente!")
        print(f"📂 Ubicación: {Path('dist').absolute()}")
        return True
    except Exception as e:
        print(f"\n❌ Error al crear ejecutable: {e}")
        return False


def create_installer_package():
    """Crea el paquete de instalación completo"""
    print("\n📁 Creando paquete de instalación...")

    # Crear carpeta de distribución
    dist_folder = Path('installer_package')
    dist_folder.mkdir(exist_ok=True)

    # Copiar ejecutable
    exe_name = 'DevelopmentDiary.exe' if sys.platform == 'win32' else 'DevelopmentDiary'
    exe_source = Path('dist') / exe_name

    if exe_source.exists():
        shutil.copy2(exe_source, dist_folder / exe_name)
        print(f"   ✓ Copiado {exe_name}")

    # Copiar scripts de instalación
    installer_scripts = Path('installer')
    if installer_scripts.exists():
        for script in installer_scripts.glob('*'):
            shutil.copy2(script, dist_folder / script.name)
            print(f"   ✓ Copiado {script.name}")

    # Copiar README
    if Path('README.md').exists():
        shutil.copy2('README.md', dist_folder / 'README.md')
        print("   ✓ Copiado README.md")

    # Copiar requirements (por si acaso)
    shutil.copy2('requirements.txt', dist_folder / 'requirements.txt')
    print("   ✓ Copiado requirements.txt")

    print(f"\n✅ Paquete de instalación creado en: {dist_folder.absolute()}")
    print("\n📦 Contenido del paquete:")
    for item in dist_folder.iterdir():
        print(f"   • {item.name}")


def main():
    """Proceso principal de construcción"""
    print("=" * 60)
    print("   DEVELOPMENT DIARY - BUILD INSTALLER")
    print("=" * 60)

    # Verificar que estamos en el directorio correcto
    if not Path('app.py').exists():
        print("❌ Error: No se encuentra app.py")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        sys.exit(1)

    # Paso 1: Limpiar
    clean_build()

    # Paso 2: Construir ejecutable
    if not build_executable():
        print("\n❌ Falló la construcción del ejecutable")
        sys.exit(1)

    # Paso 3: Crear paquete
    create_installer_package()

    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\n📌 Próximos pasos:")
    print("   1. Ve a la carpeta 'installer_package'")
    print("   2. Distribuye todo su contenido")
    print("   3. El usuario ejecuta install.bat (Windows) o install.sh (Linux/Mac)")
    print("\n")


if __name__ == '__main__':
    main()