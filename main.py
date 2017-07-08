#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from argparse import ArgumentParser
from mistune import mistune


def parser():
    usage = 'Usage: python {} FILE [--templete <file>] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('fname', type=str,
                           help='create html from markdown')
    argparser.add_argument('-t', '--templete', type=str,
                           dest='templete_file',
                           help='use your templete file')
    args = argparser.parse_args()
    ret = {'md': args.fname, 'templete': 'templete.html'}
    if args.templete_file:
        ret['templete'] = args.templete_file
    return ret


class IDRenderer(mistune.Renderer):
    _id = re.compile(r'{#(.*)}$')

    def list_item(self, text):
        """rendering list item snippet. Like ``<li id='if exist'>``"""
        idatr = self._id.search(text)
        text = self._id.sub('', text)
        if idatr is not None:
            return '<li id=\'{}\'>{}</li>\n'\
                    .format(idatr.group(1), text)


def main():
    args = parser()
    f = open(args['md'])
    md = f.read()
    f.close()
    rep = {}
    renderer = IDRenderer(escape=False)
    rep['content'] = mistune.Markdown(renderer=renderer)(md)
    h = re.compile('<h1>(.*)</h1>')
    h1 = h.search(rep['content'])
    if h1 is not None:
        rep['title'] = h1.group(0)
    f = open(args['templete'])
    temp = f.read()
    f.close()
    for key in rep:
        temp = re.sub('{{'+key+'}}', rep[key], temp)
    fname, ext = os.path.splitext(args['md'])
    f = open(fname+'.html', 'w')
    f.write(temp)
    f.close()


if __name__ == '__main__':
    main()
