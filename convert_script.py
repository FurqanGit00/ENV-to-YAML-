import pathlib
import yaml

def convert_env_to_flat_yaml():
    # Define the root directory
    root_dir = pathlib.Path(r"C:\Users\FURQAN\Documents\Custom Office Templates\ENV-to-YAML-")
    
    # Define input and output directories
    env_files_dir = root_dir / "ENV_FILES"  # Input .env files
    output_dir = root_dir / "CONVERTED_ENV_TO_YAML"  # Output YAML files
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each .env file
    for env_file in env_files_dir.glob("*.env"):
        try:
            if not env_file.is_file():
                continue

            # Create a ConfigMap structure
            configmap = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {
                    "name": env_file.stem.lower().replace('_', '-'),
                    "namespace": "application"
                },
                "data": {}
            }

            # Read the .env file
            with env_file.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(('#', 'export ')):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Handle quoted values
                            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                                value = value[1:-1]
                            configmap["data"][key] = value or ""

            # Write the YAML file
            yaml_file = output_dir / f"{env_file.stem}.yaml"
            with yaml_file.open('w', encoding='utf-8') as yf:
                yaml.dump(
                    configmap,
                    yf,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    indent=2,
                    width=1000  # Prevent line wrapping
                )
            
            print(f"Converted: {env_file.name} => {yaml_file.name}")

        except Exception as e:
            print(f"Error processing {env_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    convert_env_to_flat_yaml()