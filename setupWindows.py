from cx_Freeze import setup, Executable

# Incluye los archivos adicionales necesarios
includefiles = ['algoritmo.py', 'resultados.py']

# Define las opciones
build_exe_options = {
    "packages": ["algoritmo", "resultados", "os", "sys", "random", "PyQt5.QtWidgets", "PyQt5.QtGui", "matplotlib", "networkx"],
    "include_files": includefiles
}

# Define el ejecutable
executables = [
    Executable("interfaz.py", base=None, target_name="Buscador-Kinder,Silva.exe")
]

setup(
    name="Buscador-Kinder,Silva",
    version="1.0",
    description="Búsqueda heurística de algoritmos: Escalada simple y Máxima pendiente",
    options={"build_exe": build_exe_options},
    executables=executables
)
