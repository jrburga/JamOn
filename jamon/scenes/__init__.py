import os
scenes = []
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py' or module == 'scene_util.py':
        continue
    scenes.append(__import__(module[:-3], locals(), globals()).scene)
del module