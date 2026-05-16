from .kullanici_input import TOOL_SCHEMA, kullanici_input_handler, submit_input

TOOL_DEFINITIONS = [TOOL_SCHEMA]

TOOL_FUNCTIONS = {
    "kullanici_input": kullanici_input_handler,
}

__all__ = ["TOOL_DEFINITIONS", "TOOL_FUNCTIONS", "submit_input"]
