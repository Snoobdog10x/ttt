from utils.samples import models, events, screens
import utils.file as f
import argparse


def ttt_sync():
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
    print("test")


def main(args):
    if args.sync:
        ttt_sync()
        return
    count_code_line()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sync', action='store_true', help='sync file from config')
    group.add_argument('--count', action='store_true', help='count line code')
    args = parser.parse_args()
    main(args)
