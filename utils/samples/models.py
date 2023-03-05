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
    if dart_type.upper() == "STRING":
        return f'{prefix}""'
    return ""


def _arguments_to_class_field(data: list):
    arguments = []
    for argument in data:
        dart_type = list(dict(argument).values())[0]
        field = list(dict(argument).keys())[0]
        arguments.append(f"{dart_type} {field};")
    return "\n\t".join(arguments)


def _arguments_to_main_constructor(data: list):
    arguments = []
    for argument in data:
        field = list(dict(argument).keys())[0]
        dart_type = list(dict(argument).values())[0]
        default_type_value = _get_default_data_by_type(dart_type)
        arguments.append(f'this.{field}{default_type_value},')
    return "\n\t\t".join(arguments)


def _enums_to_class_enum(enums: []):
    enums_gen = []
    enum_ske = Template("enum {{ENUM_NAME}} { {{ENUM_TYPES}} }")
    for enum in enums:
        name = list(dict(enum).keys())[0]
        ENUM_NAME = f.to_camel_case(name)
        ENUM_TYPES = ",".join([enum_type.upper() for enum_type in enum[name]])
        enum_sample = enum_ske.render(ENUM_NAME=ENUM_NAME, ENUM_TYPES=ENUM_TYPES)
        enums_gen.append(enum_sample)
    return "\t\n".join(enums_gen)


def _arguments_to_from_json_constructor(data: list):
    arguments = []
    for argument in data:
        field = list(dict(argument).keys())[0]
        dart_type = list(dict(argument).values())[0]
        default_value = _get_default_data_by_type(dart_type, False)
        arguments.append(f'{field} = json["' + field + f'"] ?? {default_value};')
    return "\n\t\t".join(arguments)


def _arguments_to_to_json(data: list):
    arguments = []
    for argument in data:
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
    ARGUMENTS = f.get_arguments_from_config(config_file_path)
    ENUMS_CONFIG = f.get_enums_from_config(config_file_path)
    NAMING = camel_name
    CLASS_FIELD = _arguments_to_class_field(ARGUMENTS)
    ENUMS = _enums_to_class_enum(ENUMS_CONFIG)
    MAIN_CONSTRUCTOR = _arguments_to_main_constructor(ARGUMENTS)
    FORM_JSON_CONSTRUCTOR = _arguments_to_from_json_constructor(ARGUMENTS)
    TO_JSON = _arguments_to_to_json(ARGUMENTS)
    template = Template(ske.MODELS)

    output = template.render(ENUMS=ENUMS, NAMING=NAMING, CLASS_FIELD=CLASS_FIELD, MAIN_CONSTRUCTOR=MAIN_CONSTRUCTOR,
                             FORM_JSON_CONSTRUCTOR=FORM_JSON_CONSTRUCTOR, TO_JSON=TO_JSON)
    f.write_file(OUTPUT_MODEL_FILE_PATH, output)
