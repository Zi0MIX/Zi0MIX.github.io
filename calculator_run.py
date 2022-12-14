from js import Alpine, Object, console, performance
from pyodide.ffi import create_proxy, to_js


# Exports Python to JavaScript console and Alpine.store()
def export_data(data):
    console.log(str(data))
    output = to_js(data, dict_converter = Object.fromEntries)
    Alpine.store('calculatorOutput', output)
    Alpine.store('time').end = performance.now()


def import_calculator() -> tuple:
    try:
        from zm_calculator import main_api, map_translator, MAP_LIST, get_arguments
        return (main_api, map_translator, MAP_LIST, get_arguments)
    except ModuleNotFoundError as err:
        module_error = [{"type": "error", "message": str(err)}]
        export_data(module_error)
        return False


calculator = import_calculator()

# Assign imported components to globals available for this module
if calculator:
    main, map_translator, map_list, argument_list = calculator

    # Expose calculator_web imports to Alpine
    Alpine.store('mapCodes', to_js(map_list))
    Alpine.store('mapTranslator', create_proxy(map_translator))
    Alpine.store('arguments', to_js(argument_list(), dict_converter = Object.fromEntries))


# Perform calculation and use Alpine.store() for I/O
def run_calculator():
    input_data = Alpine.store('calculatorInput').to_py()
    calculation_data = main(input_data)
    export_data(calculation_data)
