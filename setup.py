from cx_Freeze import setup, Executable

# Añade los módulos necesarios en la opción 'packages'
options = {
    'build_exe': {
        'packages': ['algoritmo', 'PyQt5', 'random', 'networkx', 'matplotlib'],
        'include_files': ['algoritmo.py']
    }
}

# Ejecutable que se va a crear
executables = [
    Executable('interfaz.py', base=None)
]

setup(
    name='Interfaz',
    version='1.0',
    description='Descripción de tu aplicación',
    options=options,
    executables=executables
)
