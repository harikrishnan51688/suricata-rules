import os
from validator import validate_rules_files, combine_and_validate_rules
from get_rules import process_yaml_sources
from process_rules import create_tarball_archives



if __name__ == "__main__":

    yaml_file = "index.yaml"
    
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file '{yaml_file}' not found!")
        print("Please update the yaml_file variable with the correct path.")
    else:
        process_yaml_sources(yaml_file, output_dir='rules_downloads')
    
    validator_1 = validate_rules_files()
    validator_2 = combine_and_validate_rules()
    make_tarball = create_tarball_archives()
