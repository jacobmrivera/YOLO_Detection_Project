#!/usr/bin/env python
import json
import argparse
import obj_predictor.data_processing.make_config

'''
Created by Jacob Rivera
Fall 2023

Last edit: 01/03/2024

Description:
    Generates .yaml config file for YOLO training form json config file
'''





def main():
    parser = argparse.ArgumentParser(description="Generate .yaml config file for YOLO training")
    parser.add_argument("--json_config_path", required=True, help="Path to json config file")
    args = parser.parse_args()

    json_config_path = args.json_config_path

    try:
        with open(json_config_path, 'r') as config_file:
            json_config = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error reading config file.")

    obj_predictor.data_processing.make_config.make_config(json_config)

    return

if __name__ == "__main__":
    main()