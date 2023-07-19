import i18n
import os

import yaml

res_dir = os.path.join(os.path.dirname(__file__))

i18n.load_path.append(res_dir)
i18n.set('skip_locale_root_data', True)


class Translated(object):
    def __init__(self, package_name, resource_dir=res_dir):
        with open(os.path.join(resource_dir, f'{package_name}.en.yaml')) as f:
            resx_dict = yaml.load(f)
        for key in resx_dict.keys():
            setattr(self, key, i18n.t(f'{package_name}.{key}'))


class LangClass(Translated):
    def __init__(self):
        super().__init__('Lang')


Lang = LangClass()


class BuildInCommandInformationsClass(Translated):
    def __init__(self):
        super().__init__('BuildInCommandInformations')


BuildInCommandInformations = BuildInCommandInformationsClass()

__all__ = ['BuildInCommandInformations', 'Lang']
