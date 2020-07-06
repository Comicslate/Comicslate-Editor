# -*- coding: utf-8 -*-
from os.path import (basename, realpath, join, dirname)
import os
import re
import logging
import magic


logging.basicConfig(format='%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('comicslate.files')
logger.setLevel(logging.DEBUG)


class MyFile(object):
    def __init__(self, filename):
        logger.debug(f'MyFile| Подгружаем файл картинки {filename}')
        self.filename = self._checkfilename(filename)
        self.listfiles = []
        self.index = 0
        self.name = ''
        self._getparams(self.filename)

    def __str__(self):
        return self.filename

    def _getparams(self, filename):
        self.name = basename(filename)
        self.dir = dirname(filename)
        listfiles = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                listfiles.append(join(root, file))
        if len(listfiles) != len(self.listfiles):
            self.listfiles.clear()
            self.listfiles = listfiles.copy()
        self.index = self.listfiles.index(filename)

    def _checkfilename(self, filename):
        if os.name == 'nt':
            filename = filename.replace('/', '\\')
        else:
            filename = filename.replace('\\', '/')
        return filename

    def next(self):
        if self.index + 1 <= len(self.listfiles) - 1:
            self.index = self.index + 1
        self.filename = self.listfiles[self.index]
        self._getparams(self.filename)
        return self.filename

    def prev(self):
        if self.index - 1 < 0:
            self.index = self.index - 1
        self.filename = self.listfiles[self.index]
        self._getparams(self.filename)
        return self.filename


class ParcerTxt(object):
    def __init__(self):
        logger.debug('Инициализируем класс парсера')
        self.cotan = re.compile('{{cotan>(\d+)}}(.+){{cotan}}')
        self.cotan2 = re.compile('{{cotan>\d+}}')
        self.cnav = re.compile('{\d{4}?>?cnav}')
        # Заголовок стрипа
        self.title = ''
        # описание под заголовком стрипа
        self.descr = ''
        # описание над самим стрипом
        self.uptext = ''
        # маски, закрывающие текст
        # https://comicslate.org/ru/wiki/12balloons
        # @x,y,w,h
        # все что ниже реализовано для aimg или в планах
        # @x,y,w,h,deg
        # @x,y,w,h,deg;lup, rup, rdn, ldn
        # @x,y,w,h,deg;lup, rup, rdn, ldn
        # @x,y,w,h,deg;lup,,,
        # @x,y,w,h,deg;lup,,rdn,
        # кол-во скруглений от 1 до 4. При нуле скругление 10%
        # lup задает радиус всем или только верхним при наличии rdn
        # rdn задает радиус нижнему правому или всем нижним

        self.masks = []
        # сами баннеры с текстом
        self.texts = []
        # текст под стрипом
        self.buttontext = ''

    def _checkfilename(self, filename):
        if os.name == 'nt':
            filename = filename.replace('/', '\\')
        else:
            filename = filename.replace('\\', '/')
        return filename

    def get(self):
        return [self.title, self.descr, self.uptext, self.masks, self.texts, self.buttontext]

    def open(self, filename):
        logger.debug(f'Try to open {filename}')
        filename = str(filename)
        if not os.path.isabs(filename):
            logger.debug(f'Path is nor absolute')
    #    return None
        if filename.find('txt') < 0:
            logger.debug(f'file is not text, searching for text file')
            dirname = os.path.dirname(filename)
            name = os.path.basename(filename)
            name = '.'.join([name.split('.')[0], 'txt'])
            logger.debug(f'filename {name}, dirname {dirname}')
            filename = join(dirname, name)
        if not os.path.isfile(filename):
            logger.debug(f'File {filename} not exists')
            return None
        mime = magic.Magic(mime_encoding=True)
        encofing = mime.from_file(filename)
        with open(filename, 'r', encoding=encofing) as f:
            logger.debug(f'Reading file')
            data = f.read()
        lines = data.split('\n')
        self.title = lines[0]
        self.descr = lines[1]
        if data.find('cotan') > 0:
            logger.debug(f'Cotan findet')
            self.parce_cotan(lines)

    def parce_cotan(self, lines):
        idx = 1
        fcnav = False
        fcotan = False
        while idx < len(lines):
            if lines[idx].find('cnav') > 0 and not fcnav:
                duptext = []
                fcnav = True
                logger.debug(f'searching uptext')
                while lines[idx + 1].find('cotan') < 0:
                    idx = idx + 1
                    duptext.append(lines[idx])
                self.uptext = '\n'.join(duptext)
            if lines[idx].find('cotan') > 0 and not fcotan:
                logger.debug(f'parse cotan block')
                fcotan = True
                while lines[idx + 1].find('cotan') < 0:
                    idx = idx + 1
                    coords = []
                    rounds = []
                    #logger.debug(f'Parse line: "{lines[idx]}"')
                    if lines[idx][0] == '@':
                        res = lines[idx][1:].split(';')
                        if len(res) == 2:
                            coords, rounds = res
                        elif len(res) == 1:
                            coords = res[0]
                        else:
                            print("error in coords")
                            exit(1)
                        coords = coords.split(',')
                        if len(coords) == 4:
                            x, y, w, h = str_to_deg(coords)
                            deg = 0
                        elif len(coords) == 5:
                            x, y, w, h, deg = str_to_deg(coords)
                        else:
                            x, y, w, h, deg = [0, 0, 0, 0, 0]
                        if len(rounds) > 0:
                            rounds = rounds.split(',')
                            if len(rounds) == 1:
                                rounds = [rounds[0], rounds[0], rounds[0], rounds[0]]
                            elif len(rounds) == 2:
                                rounds = [rounds[0], rounds[0], rounds[1], rounds[1]]
                        else:
                            rounds = ['10%', '10%', '10%', '10%']
                        lup, rup, rdn, ldn = rounds
                        text = []
                        fmask = False
                        while lines[idx + 1][0] != '~':
                            idx = idx + 1
                            if lines[idx][0] == '#':
                                fmask = True
                                if len(lines[idx][1:]) > 1:
                                    text.append(lines[idx][1:])
                                continue
                            text.append(lines[idx])
                        if fmask:
                            if len(text) > 0:
                                text = '\n'.join(text)
                            else:
                                text = None
                            self.masks.append({'x': x, 'y': y, 'w': w, 'h': h, 'deg': deg,
                                               'lup': lup, 'rup': rup, 'rdn': rdn, 'ldn': ldn,
                                               'text': None,
                                               'mask': text})
                        else:
                            self.texts.append({'x': x, 'y': y, 'w': w, 'h': h, 'deg': deg,
                                               'lup': lup, 'rup': rup, 'rdn': rdn, 'ldn': ldn,
                                               'text': '\n'.join(text),
                                               'mask': None})
            if lines[idx].find('cotan') > 0 and fcotan:
                text = []
                logger.debug(f'searching buttontext')
                while lines[idx + 1].find('cnav') < 0:
                    idx = idx + 1
                    text.append(lines[idx])
                self.buttontext = '\n'.join(text)
            idx = idx + 1


def str_to_deg(listing):
    return [int(i) for i in listing]


if __name__ == '__main__':
    f = 'D:\\tmp\granite\Бесшовная текстура гранита #3535.jpg'
    f = 'D:\\tmp\comicslate\\0021.txt'
    # e = MyFile(f)
    e = ParcerTxt()
    e.open(f)
    print(e.get())
