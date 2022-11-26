from js import Alpine, Object, console
from pyodide.ffi import create_proxy, to_js

try:
    from calculator_web import MAP_LIST, map_translator, main
except ModuleNotFoundError as err:
    module_error = [{"type": "error", "message": str(err)}]
    console.log(str(module_error))
    output_data = to_js(module_error, dict_converter = Object.fromEntries)
    Alpine.store('calculatorOutput', output_data)


# Expose calculator_web imports to Alpine
Alpine.store('mapCodes', to_js(MAP_LIST))
Alpine.store('mapTranslator', create_proxy(map_translator))

# Perform calculation and use Alpine.store() for I/O
def run_calculator():
    input_data = Alpine.store('calculatorInput').to_py()
    calculation_data = main(input_data)
    console.log(str(calculation_data))
    output_data = to_js(calculation_data, dict_converter = Object.fromEntries)
    Alpine.store('calculatorOutput', output_data)
