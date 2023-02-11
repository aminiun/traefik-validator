#! /home/amin/PycharmProjects/traefik-validator/venv/bin/python3

import argparse

from utils import Validator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="validate_traefik", description='Validate traefik config file.')
    parser.add_argument('-s', '--static-config', type=argparse.FileType('r'), help='The static file path')
    parser.add_argument('-d', '--dynamic-config', type=argparse.FileType('r'), help='The dynamic file path')

    args = parser.parse_args()

    Validator(static_conf_file=args.static_config, dynamic_conf_file=args.dynamic_config).validate()
