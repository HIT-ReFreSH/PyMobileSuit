import xml.etree.ElementTree as ET
import yaml
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('source', type=str)
parser.add_argument('target', type=str)

args = parser.parse_args()

with open(args.source, 'r', encoding='utf8') as src:
    root = ET.parse(src).getroot()
resx_dict = {data.get('name'): data.find('value').text for data in root.findall('data')}


with open(args.target, 'w', encoding='utf-8') as f:
    yaml.dump(resx_dict, f, allow_unicode=True)

