import yaml
from collections import OrderedDict
import ordered
from ordered import *

class orderedYld(object):
    """description of class"""
    def __init__ (self):
                data = {}

    def orderedYaml_loader(filepath):
                """Loads a yaml file"""
                oorr = ordered
                with open(filepath, "r") as file_descriptor:
                        data = oorr.ordered_load (file_descriptor, yaml.SafeLoader)
                        #data = ordered_load(file_descriptor, yaml.SafeLoader)
                return data

    def orderedYaml_dump(filepath, data):
                """Dump data to a yaml file"""
                oorw = ordered
                with open(filepath, "w") as file_desxriptor:
                        #yaml.dump(data, file_desxriptor , default_flow_style=False)
                        oorw.ordered_dump(data, file_desxriptor ,  Dumper=yaml.SafeDumper , default_flow_style=False)

    def orderedYaml_append(filepath, data):
                """Dump data to a yaml file"""
                oorw = ordered
                with open(filepath, 'a') as file_desxriptor:
                        #yaml.dump(data, file_desxriptor , default_flow_style=False)
                        oorw.ordered_dump(data, file_desxriptor ,  Dumper=yaml.SafeDumper , default_flow_style=False)
    
