from cx_Freeze import setup, Executable

# Añade los módulos necesarios en la opción 'packages'
options = {
    'build_exe': {
        'packages': ['algoritmo', 'resultados' ,'os', 'sys', 'random','PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 'networkx', 'matplotlib.pyplot'],
        'include_files': ['algoritmo.py', 'resultados.py']
    }
}

# Ejecutable que se va a crear
executables = [
    Executable('main.py', base=None)
]

setup(
    name='Buscador-Kinder,Silva',
    version='1.0',
    description='Búsqueda heurística de algoritmos: Escalada simple y Máxima pendiente',
    options=options,
    executables=executables
)