import utils.samples.skeleton as ske
from jinja2 import Template
import utils.file as f


def _get_default_data_by_type(dart_type: str, has_equal: bool = True):
    prefix = ""
    if has_equal:
        prefix = " = "
    if dart_type.upper() == "BOOL":
        return f"{prefix}false"
    nums = ["DOUBLE", "INT"]
    if dart_type.upper() in nums:
        return f"{prefix}0"
    if "LIST" in dart_type.upper():
        return f"{prefix}{'{}'}"
    if dart_type.upper() == "STRING":
        return f'{prefix}""'
    return ""


def _arguments_to_class_field(data: dict):
    if data is None or "arguments" not in data or data["arguments"] is None:
        return ""
    arguments = []
    for argument in data["arguments"]:
        dart_type = list(dict(argument).values())[0]
        field = list(dict(argument).keys())[0]
        arguments.append(f"{dart_type}? {field};")
    return "\n\t".join(arguments)


def _arguments_to_main_constructor(data: dict):
    if data is None or "arguments" not in data or data["arguments"] is None:
        return ""
    arguments = []
    for argument in data["arguments"]:
        field = list(dict(argument).keys())[0]
        dart_type = list(dict(argument).values())[0]
        default_value = _get_default_data_by_type(dart_type)
        arguments.append(f'this.{field}{default_value},')
    return "\n\t\t".join(arguments)


def _arguments_to_from_json_constructor(data: dict):
    if data is None or "arguments" not in data or data["arguments"] is None:
        return ""
    arguments = []
    for argument in data["arguments"]:
        field = list(dict(argument).keys())[0]
        dart_type = list(dict(argument).values())[0]
        default_value = _get_default_data_by_type(dart_type, False)
        arguments.append(f'{field} = json["' + field + f'"] ?? {default_value};')
    return "\n\t\t".join(arguments)


def _arguments_to_to_json(data: dict):
    if data is None or "arguments" not in data or data["arguments"] is None:
        return ""
    arguments = []
    for argument in data["arguments"]:
        field = list(dict(argument).keys())[0]
        arguments.append(f'data["' + field + f'"] = this.{field};')
    return "\n\t\t".join(arguments)


def write_model_sample_file(config_file_path):
    model_name = f.extract_file_name_from_config_file(config_file_path)
    print(f"compile {model_name} model")
    camel_name = f.to_camel_case(model_name)
    OUTPUT_MODEL_PATH = f"lib/models/{model_name}"
    f.create_path(OUTPUT_MODEL_PATH)
    OUTPUT_MODEL_FILE_PATH = f"lib/models/{model_name}/{model_name}.dart"
    ARGUMENTS = f.read_config_file(config_file_path)
    NAMING = camel_name
    CLASS_FIELD = _arguments_to_class_field(ARGUMENTS)
    MAIN_CONSTRUCTOR = _arguments_to_main_constructor(ARGUMENTS)
    FORM_JSON_CONSTRUCTOR = _arguments_to_from_json_constructor(ARGUMENTS)
    TO_JSON = _arguments_to_to_json(ARGUMENTS)
    template = Template(ske.MODELS)

    output = template.render(NAMING=NAMING, CLASS_FIELD=CLASS_FIELD, MAIN_CONSTRUCTOR=MAIN_CONSTRUCTOR,
                             FORM_JSON_CONSTRUCTOR=FORM_JSON_CONSTRUCTOR, TO_JSON=TO_JSON)
    f.write_file(OUTPUT_MODEL_FILE_PATH, output)
