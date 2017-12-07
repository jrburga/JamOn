import os
scenes = {}
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    name = module.split('.')[0]
    imports = __import__(module[:-3], locals(), globals())
    if hasattr(imports, 'build_scene'):
        scenes[name] = imports.build_scene
del module