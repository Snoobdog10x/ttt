import utils.file as f
import utils.samples.skeleton as ske
from jinja2 import Template


def write_screen_provider_sample_file(config_file_path):
    screen_provider_name = f.extract_file_name_from_config_file(config_file_path)
    camel_name = f.to_camel_case(screen_provider_name)
    OUTPUT_EVENT_PATH = f"lib/screens/{screen_provider_name}"
    f.create_path(OUTPUT_EVENT_PATH)
    OUTPUT_EVENT_FILE_PATH = f"lib/screens/{screen_provider_name}/{screen_provider_name}_provider.dart"
    if f.check_file_exist(OUTPUT_EVENT_FILE_PATH):
        return
    NAMING = camel_name
    template = Template(ske.SCREENS_PROVIDER)
    output = template.render(NAMING=NAMING)
    f.write_file(OUTPUT_EVENT_FILE_PATH, output)
    print(print(f"compiled {screen_provider_name} screen"))


def write_screen_sample_file(config_file_path):
    screen_name = f.extract_file_name_from_config_file(config_file_path)
    camel_name = f.to_camel_case(screen_name)
    OUTPUT_EVENT_PATH = f"lib/screens/{screen_name}"
    f.create_path(OUTPUT_EVENT_PATH)
    OUTPUT_EVENT_FILE_PATH = f"lib/screens/{screen_name}/{screen_name}_screen.dart"
    if f.check_file_exist(OUTPUT_EVENT_FILE_PATH):
        return
    NAMING = camel_name
    PATH_NAMING = screen_name
    template = Template(ske.SCREENS)
    output = template.render(NAMING=NAMING, PATH_NAMING=PATH_NAMING)
    f.write_file(OUTPUT_EVENT_FILE_PATH, output)
    print(print(f"compiled {screen_name} screen"))


def write_abstract_screen_file(path: str):
    output_abstract = f'{path}/abstract_state.dart'
    output_provider = f'{path}/abstract_provider.dart'
    f.write_file(output_abstract, ske.ABSTRACT_SCREEN)
    f.write_file(output_provider, ske.ABSTRACT_PROVIDER)
