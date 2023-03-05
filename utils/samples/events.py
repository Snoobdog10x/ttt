import utils.file as f
import utils.samples.skeleton as ske
from jinja2 import Template


def write_event_sample_file(config_file_path):
    event_name = f.extract_file_name_from_config_file(config_file_path)

    camel_name = f.to_camel_case(event_name)
    OUTPUT_EVENT_PATH = f"lib/events/{event_name}"
    f.create_path(OUTPUT_EVENT_PATH)
    OUTPUT_EVENT_FILE_PATH = f"lib/events/{event_name}/{event_name}.dart"
    if f.check_file_exist(OUTPUT_EVENT_FILE_PATH):
        return
    NAMING = camel_name
    template = Template(ske.EVENTS)
    output = template.render(NAMING=NAMING)
    f.write_file(OUTPUT_EVENT_FILE_PATH, output)
    print(print(f"compile {event_name} event"))
