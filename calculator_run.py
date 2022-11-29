from js import Alpine, Object, console, performance
from sys import exit
from pyodide.ffi import create_proxy, to_js


# Exports Python to JavaScript console and Alpine.store()
def export_data(data):
    # console.log(str(data))
    output = to_js(data, dict_converter = Object.fromEntries)
    Alpine.store('calculatorOutput', output)
    Alpine.store('time').end = performance.now()


def import_calculator() -> tuple:
    try:
        from calculator_web import main_api, map_translator, MAP_LIST, get_arguments
        return (main_api, map_translator, MAP_LIST, get_arguments)
    except ModuleNotFoundError as err:
        module_error = [{"type": "error", "message": str(err)}]
        export_data(module_error)
        return False


calculator = import_calculator()
if not calculator:
    exit()

main, map_translator, MAP_LIST, get_arguments = calculator[0], calculator[1], calculator[2], calculator[3]

# Expose calculator_web imports to Alpine
Alpine.store('mapCodes', to_js(MAP_LIST))
Alpine.store('mapTranslator', create_proxy(map_translator))
Alpine.store('arguments', to_js(get_arguments(), dict_converter = Object.fromEntries))

# Perform calculation and use Alpine.store() for I/O
def run_calculator():
    input_data = Alpine.store('calculatorInput').to_py()
    calculation_data = main(input_data)
    export_data(calculation_data)
