#!/usr/bin/env python3
import argparse
import json
import sys


plugin = {
    "name": "Calculator",
    "directives": [
        {
            "name": "calc",
            "doc": "An example directive for running Python expressions.",
            "body": {
                "type": "string",
                "doc": "The expression to compute",
            },
        }
    ],
}


def declare_result(content):
    """Declare result as JSON to stdout

    :param content: content to declare as the result
    """

    # Format result and write to stdout
    json.dump(content, sys.stdout, indent=2)
    # Successfully exit
    raise SystemExit(0)


def run_directive(name, data):
    """Execute a directive with the given name and data

    :param name: name of the directive to run
    :param data: data of the directive to run
    """
    assert name == "calc"

    # Run user program
    result = eval(data["body"], {**globals(), **vars(__import__("math"))})
    result = {"type": "code", "value": str(result)}
    return [result]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--role")
    group.add_argument("--directive")
    group.add_argument("--transform")
    args = parser.parse_args()

    if args.directive:
        data = json.load(sys.stdin)
        declare_result(run_directive(args.directive, data))
    elif args.transform:
        raise NotImplementedError
    elif args.role:
        raise NotImplementedError
    else:
        declare_result(plugin)
