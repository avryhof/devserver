import pprint
import re

from utilities.aware_datetime import aware_datetime

datetime = aware_datetime()


def path_explode(path_string):
    return re.split(r"/|\\", path_string)


def join_url(*args):
    args = list(args)

    path_parts = []
    for arg in args:
        if isinstance(arg, list):
            arg = join_url(*arg)

        elif "http" in arg:
            split_args = arg.split("/")
            split_args[0] = "%s/" % split_args[0]
            for split_arg in split_args:
                path_parts.append(split_arg)

        else:
            path_parts.append(arg)

    for path_part in path_parts:
        if not path_part:
            path_parts.remove(path_part)

    path_retn = "/".join(path_parts)

    return path_retn


def format_log_message(message, **kwargs):
    pretty = kwargs.get("pretty", False)

    if pretty:
        message = pprint.pformat(message)

    log_message = "%s: %s\n" % (datetime.now().isoformat()[0:19], message)

    return log_message


def slugify(value):
    if isinstance(value, str):
        value = re.sub(r"[^a-z0-9_\- ]", "", value.lower()).replace(" ", "-")

    return value
