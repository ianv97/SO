from cx_Freeze import setup, Executable

base = None
executables = [Executable("SimuladorSO.py", base=base, compress=True, icon="Recursos/logo.ico")]

packages = ['idna', 'numpy.core._methods', 'numpy.lib.format']
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "SimuladorSO",
    options = options,
    version = "1.0",
    description = "Simulador de SO: Planificación de procesos y administración de memoria",
    author= "Ian Vaernet",
    executables = executables
)