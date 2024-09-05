import sys
import yaml

def add_resource(file_name:str) -> None:

    with open(file_name, "r+") as file:
        configuration = yaml.safe_load(file)
        containers = configuration['spec']['template']['spec']['containers']

        for (index, container) in enumerate(containers):
            if container["image"] == "__DOCKER_IMG__":
                container["resources"] = {
                    "requests": {
                        "memory": "512Mi",
                        "cpu": "250m"
                    },
                    # "limits": {
                    #     "memory": "1Gi"
                    # }
                }
                configuration['spec']['template']['spec']['containers'][index] = container
        file.seek(0)
        file.truncate()
        yaml.dump(configuration, file)
        print(f"Updated {file_name}")

if __name__ == '__main__':
    n = len(sys.argv)
    if n < 3:
        print('Usage: python3 add_resource.py branchname file_to_read_.yml')
        sys.exit(0)
    if sys.argv[1] == 'main':
        add_resource(file_name=sys.argv[2])
    else:
        print('Ignoring: will add resource only to main branch')