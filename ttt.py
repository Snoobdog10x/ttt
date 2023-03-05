from utils.samples import models, events, screens
import utils.file as f
import argparse
import os


def ttt_sync():
    screens.write_abstract_screen_file("lib/screens/abstracts")
    configs = f.get_all_config_file()
    for path in configs:
        if "models" in path:
            models.write_model_sample_file(path)
            continue

        if "events" in path:
            events.write_event_sample_file(path)
            continue

        if "screens" in path:
            screens.write_screen_sample_file(path)
            screens.write_screen_provider_sample_file(path)
            continue


def count_code_line():
    exts = ["dart"]
    PWD = os.path.dirname(os.path.realpath(__file__))
    for ext in exts:
        print(ext)
        f.count_lines(PWD, ext=ext)


def init_folder():
    f.create_path("config/models")
    f.create_path("config/screens")
    f.create_path("config/events")
    f.create_path("lib/models")
    f.create_path("lib/screens")
    f.create_path("lib/events")
    f.create_path("lib/screens/abstracts")
    screens.write_abstract_screen_file("lib/screens/abstracts")
    pass


def main(args):
    if args.init_source:
        init_folder()
        return
    if args.sync:
        ttt_sync()
        return
    if args.count:
        count_code_line()
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init_source', action='store_true',
                       help='init flutter project by provider structure file from config')
    group.add_argument('--sync', action='store_true', help='sync file from config')
    group.add_argument('--count', action='store_true', help='count line code')
    args = parser.parse_args()
    main(args)
