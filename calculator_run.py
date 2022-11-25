import js, json
from js import Alpine
from pyodide.ffi import to_js

# Expose some Python globals to JavaScript and Alpine
js.pyGlobals = globals()
Alpine.store('mapCodes', to_js(MAP_LIST))

# Pass print inputs to JavaScript console and debug view, handled by Alpine
def print(text = ""):
    output = to_js(text, dict_converter = js.Object.fromEntries)
    js.console.log(output)
    Alpine.store('calculatorOutput', output)

# Perform calculation and use Alpine.store() for I/O
def run_calculator():
    input_data = Alpine.store('calculatorInput').to_py()
    calculation_data = main(input_data)
    js.console.log(str(calculation_data))
    output_data = to_js(calculation_data, dict_converter = js.Object.fromEntries)
    Alpine.store('calculatorOutput', output_data)
