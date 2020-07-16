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
        self.picname = ''

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
            filename = join(dirname, name)
            logger.debug(f'filename {name}, dirname {dirname}, fulname {filename}')
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
        return 'Done'

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
                fnst = lines[idx].find('>') + 1
                fnend = lines[idx].find('}')
                self.picname = lines[idx][fnst:fnend]
                logger.debug(f'parse cotan block of {self.picname}')
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
                            y, x, w, h = str_to_deg(coords)
                            deg = 0
                        elif len(coords) == 5:
                            y, x, w, h, deg = str_to_deg(coords)
                        else:
                            y, x, w, h, deg = [0, 0, 0, 0, 0]
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

    def parce_aimg(self, lines):
        # функция парсера aimg из основного модуля. Просто сохранил. Потом переписать.
        def str2int(string):
            result = []
            for i in string.split(","):
                # print string
                result.append(int(i))
            return result

        coordinates = []
        niks = []
        texts = []
        data = '\n'.join(lines)
        self.body = re.compile(u'<aimg}}(.*)', re.S).findall(data)[0]
        # print self.body
        s = re.compile(u'@(.*?)~', re.S).findall(data)
        titleImg = re.compile(u'{cnav}[^*]\*\*([^*]*?)\*').findall(data)[0].decode('utf8')
        # self.titleImg.setText(titleImg)
        pathImg = re.compile(u'{aimg>([^]]*?)}').findall(data)
        # self.lineEdit.setText(":".join(pathImg[0].split(":")[:-1]))
        # print ":".join(pathImg[0].split(":")[:-1])
        # print pathImg[0].split(":")
        for i in s:
            ss = i.split("\n")

            coordinates.append(str2int(ss[0]))
            rr = re.compile(u'\(.*?\)|\[.*?\]', re.S).findall(ss[1])
            # print rr
            niks.append(rr)
            ss[1] = re.compile(u'\(.*?\)|\[.*?\]').sub('', ss[1])
            # ss[1]=re.compile(u'\[.*?\]').sub('',ss[1])
            texts.append(ss[1])
        return coordinates, texts, niks

    def savefile(self):
        lines = []
        lines.append(self.title)
        lines.append(self.descr)
        lines.append('')
        lines.append('{cnav}')
        lines.append(''.join(['{{cotan>', self.picname, '}}']))
        for line in self.masks:
            coord = dict_to_write(line)
            lines.append(coord)
            if line['mask'] is None:
                text = '#'
            else:
                text = ''.join(['#', line['mask']])
            lines.append(text)
            lines.append('~')
        for line in self.texts:
            coord = dict_to_write(line)
            lines.append(coord)
            text = line['text']
            lines.append(text)
            lines.append('~')
        lines.append('{{<cotan}}')
        if self.uptext != '':
            lines.append(self.uptext)
        lines.append('{cnav}')
        ret = '\n'.join(lines)
        return ret


def str_to_deg(listing):
    return [int(i) for i in listing]


def dict_to_write(data):
    ret1 = []
    ret1.append(str(data['x']))
    ret1.append(str(data['y']))
    ret1.append(str(data['w']))
    ret1.append(str(data['h']))
    if data['deg'] != 0:
        ret1.append(str(data['deg']))
    ret2 = []
    if data['lup'] != '10%':
        if data['rup'] != data['lup']:
            ret2.append(data['lup'])
            ret2.append(data['rup'])
            ret2.append(data['rdn'])
            ret2.append(data['ldn'])
        elif data['rup'] != data['rdn']:
            ret2.append(data['lup'])
            ret2.append(data['rdn'])
        else:
            ret2.append(data['lup'])
    ret = ','.join(ret1)
    ret = ''.join(['@', ret])
    if len(ret2) > 0:
        ret2 = ','.join(ret2)
        ret = ';'.join([ret, ret2])
    return ret


if __name__ == '__main__':
    f = 'D:\\tmp\granite\Бесшовная текстура гранита #3535.jpg'
    f = 'D:\\tmp\comicslate\\0021.txt'
    # e = MyFile(f)
    e = ParcerTxt()
    e.open(f)
    print(e.savefile())

