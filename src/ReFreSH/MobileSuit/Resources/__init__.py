import os
import yaml
from .. import SuitConfig

res_dir = os.path.join(os.path.dirname(__file__))


class Translated(object):

    def __init__(self, package_name, resource_dir=res_dir):
        self.package_name = package_name
        self.resource_dir = res_dir
        self.Load()
    def Load(self):
        path = os.path.join(self.resource_dir, f'{self.package_name}.{SuitConfig.LOCALE}.yaml')
        with open(path,'r', encoding='utf8') as f:
            resx_dict = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in resx_dict.items():
            setattr(self, key, value)

class LangClass(Translated):
    def __init__(self):
        super().__init__('Lang')


Lang = LangClass()


class BuildInCommandInformationsClass(Translated):
    def __init__(self):
        super().__init__('BuildInCommandInformations')


BuildInCommandInformations = BuildInCommandInformationsClass()

__all__ = ['BuildInCommandInformations', 'Lang']
