"""Export characters data into XLSL
Traverses folder structure and parses character meshes
"""
import os
from pathlib import Path

import xlsxwriter
import utils_general as utils


class ProjectTraverser:
    @classmethod
    def path_to_dict(cls, path, parent=None):
        curr_dir = os.path.basename(path)
        data = {curr_dir: ''}

        if os.path.isdir(path):
            data[curr_dir] = [cls.path_to_dict(os.path.join(path,x), curr_dir) for x in os.listdir(path)]
        else:
            data[curr_dir] = os.stat(path).st_size / (1024*1024)
        
        return data

    @staticmethod
    def traverse(path) -> dict:
        paths = {}

        def inner(curr_path, type_='general', level=-1) -> None:
            if level == 1:
                type_ = os.path.basename(os.path.dirname(curr_path))

            if not os.path.isdir(curr_path):
                paths.setdefault(type_, [])
                paths[type_].append(curr_path)

                return

            children = [os.path.join(curr_path, x) for x in os.listdir(curr_path)]

            if children:
                [inner(curr_path=child, type_=type_, level=level+1) for child in children]
            else:
                return
        
        inner(path)
        return paths


class XLWriter:
    @staticmethod
    def write_xls(path, name, data: dict):
        workbook = xlsxwriter.Workbook(os.path.join(path,name))
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        counter = 1
        for k, v in data.items():
            worksheet.write(f'A{counter}', k, bold)
            counter += 1

            for item in v:
                worksheet.write(f'A{counter}', item)
                counter += 1
        
        workbook.close()


class FilterUtils:
    @staticmethod
    def filter_names(data):
        def filter_cb(path: str):
            #TODO replace with regexes
            
            exclude_conditions = [
                lambda path: not 'Mesh' in path, # filter out non-Mesh assets
                lambda path: 'Physics' in path,  # filter out Physics assets
                lambda path: 'Skeleton' in path,  # filter out Skeleton assets
                lambda path: 'place_holder' in path.lower(),  # filter out placeholders
                lambda path: 'placeholder' in path.lower(),  # filter out placeholders
                lambda path: 'MT_' in path,  # filter out Material assets
                lambda path: 'SM_' in path,  # filter out Static Mesh assets
                lambda path: 'FX' in path,  # filter out FX assets
                ]

            if any(func(path) for func in exclude_conditions):
                return False

            return True
        
        filtered = list(filter(filter_cb, data))
        return filtered

    @staticmethod
    def trim_names(data):
        return [os.path.splitext(os.path.basename(path))[0] for path in data]

    @staticmethod
    def filter_empty(data):
        return {key:value for (key, value) in data.items() if value}


def main():
    # chars = ['Reiko', 'RainMage','Tanya','ShaoKahn','ShangTsung','Sindel','Kitana','Reptile']   
    chars = ['Smoke']   
    kameo_top_dir = 'C:\p4vSDevMinNSA\MK12\Content\Disk'
    kameo_chars = os.listdir(kameo_top_dir)
    kameo_dirs = [os.path.join(kameo_top_dir, char) for char in kameo_chars]

    for ch in chars:
        path = fr'C:\p4vSDevMinNSA\MK12\Content\Disk\Char\{ch}'    
    
    # for ch in kameo_chars:
        # path = fr'{kameo_top_dir}\{ch}' 
        data = ProjectTraverser.traverse(path)

        for k, v in data.items():
            print(v)
            data[k] = FilterUtils.filter_names(v)
        
        for k, v in data.items():
            data[k] = FilterUtils.trim_names(v)
        
        data = FilterUtils.filter_empty(data)

        save_path = r'C:\Projects\ContentTracker\kameo_excels' 
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        XLWriter.write_xls(save_path, f'{ch}_data.xlsx', data)

    # open in explorer
    utils.explore(save_path)

main()