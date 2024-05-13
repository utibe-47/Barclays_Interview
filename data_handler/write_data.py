from os.path import join, exists, dirname, abspath
from datetime import datetime
from openpyxl import load_workbook
from os import access, W_OK, mkdir, makedirs
import pandas as pd
import sys


class WriteData:

    def __init__(self, save_path=None, extension='xlsx'):
        if save_path is None:
            save_path = dirname(abspath(__file__))
        self.save_path = save_path
        self.ext = extension
        try:
            self._make_path(self.save_path)
        except OSError as e:
            raise OSError('folder path {} is not a valid path. See error {}'.format(self.save_path, str(e)))

    def write(self, file_name: str, **kwargs):
        folder_path = join(self.save_path, file_name + '_' + datetime.now().strftime("%m-%d-%Y"))
        self._make_path(folder_path)
        if self.ext == 'xlsx':
            self._write_to_excel(folder_path, file_name, kwargs)
        else:
            self._write_to_csv(folder_path, file_name, **kwargs)

    def _write_to_excel(self, folder_path, file_name, kwargs):
        file_path = join(folder_path, file_name + '.' + self.ext)
        if exists(file_path):
            with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:
                for key, data_frame in kwargs.items():
                    data_frame.to_excel(writer, sheet_name=key)
        else:
            with pd.ExcelWriter(file_path, mode='w') as writer:
                for key, data_frame in kwargs.items():
                    data_frame.to_excel(writer, sheet_name=key)
        writer.save()

    def _write_to_csv(self, folder_path: str, file_name: str, **kwargs):
        file_path = join(folder_path, file_name + '.' + self.ext)
        for _, data_frame in kwargs.items():
            data_frame.to_csv(file_path, encoding='utf-8')

    @staticmethod
    def _valid_path(folder_path):
        if exists(folder_path):
            return True
        elif access(dirname(folder_path), W_OK):
            return True
        else:
            try:
                mkdir(folder_path)
            except OSError as e:
                return False
            else:
                return True

    @staticmethod
    def _make_path(folder_path):
        if exists(folder_path):
            pass
        else:
            try:
                mkdir(folder_path)
            except OSError as e:
                makedirs(folder_path)
