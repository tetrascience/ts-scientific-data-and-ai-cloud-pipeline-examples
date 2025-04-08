from ts_sdk.task.__task_script_runner import Context
from src.use_context_api_actual import use_context_api_actual

def use_context_api(input: dict, context: Context):
    return use_context_api_actual(input, context)