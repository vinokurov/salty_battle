import yaml

with open("secrets.yaml", 'r') as stream:
    secrets = yaml.load(stream)

ALBY_KEY = secrets['alby_key']
