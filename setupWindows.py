from cx_Freeze import setup, Executable

# Incluye los archivos adicionales necesarios
includefiles = ['algoritmo.py']

# Define las opciones
build_exe_options = {
    "packages": ["os", "sys", "random", "PyQt5.QtWidgets", "PyQt5.QtGui", "matplotlib", "networkx"],
    "excludes": ["tkinter"],
    "include_files": includefiles
}

# Define el ejecutable
executables = [
    Executable("interfaz.py", base=None, target_name="interfaz.exe")
]

setup(
    name="Buscador Automático",
    version="1.0",
    description="Aplicación para la creación de nodos y algoritmos de búsqueda.",
    options={"build_exe": build_exe_options},
    executables=executables
)
