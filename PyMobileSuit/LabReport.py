#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   Report.py
@Contact :   ferdinandsukhoi@outlook.com
@License :   (C)Copyright 2020 Plastic-Metal

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-5-15   Ferdinand Sukhoi      0.1.4   Light-weight tool to generate markdown-formatted lab reports.
"""

import pypandoc
from os.path import join

__all__ = ['Report', 'ReportParagraph', 'ReportPlainContent', 'ReportTable']
__version__ = '0.1.4'
__author__ = 'Ferdinand Sukhoi'


class ReportContent(object):
    """A part of content in a report

    Base class
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return str(self)


class ReportPlainContent(ReportContent):
    """A part of plain content in a report

    Codes, normal text, formula, and so on

    Decorators:
        content: content represented by the class

    """

    def __init__(self, content):
        """
        initial a plain content with content represented by the class
        :param content: content represented by the class
        """
        super().__init__()
        self.content = content

    def __str__(self):
        """
        get the markdown-expression of this content
        :return: content represented by the class
        """
        return str(self.content) + '\n'


class ReportTable(ReportContent):
    """A markdown table

    Decorators:
        Headers: headers of the Table
        Data: data of the table
        Align align setting of the table:Left=-1,Right=1,Central(default)=0;
    """

    def __init__(self, headers, data, align=0):
        """
        :param headers: headers of the Table
        :param data: data of the table
        :param align align setting of the table:Left=-1,Right=1,Central(default)=0;
        :type headers list
        :type data list[list]
        :type align: list[int] or int
        """
        super().__init__()
        self.Align = align if isinstance(align, list) else [align] * len(headers)
        self.Data = data
        self.Headers = headers
        self.__TableAlign = [' :----: |', ' ----:', ':-----|']

    def __str__(self):
        """
        get the markdown-expression of this content
        :return: content represented by the class
        """
        r = '|'
        width = len(self.Headers)
        for header in self.Headers:
            r += str(header) + "|"

        r += '\n|'
        for align in self.Align:
            r += self.__TableAlign[align]
        r += '\n'
        for line in self.Data:
            r += '|'
            for cell in line:
                r += str(cell) + '|'
            r += '\n'

        return r


class ReportParagraph(ReportContent):
    """A markdown paragraph
    Decorators:
        Level: Title-level
        Title: Title
        SubContents: Contents contained by this paragraph
    """

    def __init__(self, level, title):
        """
        Initialize a report paragraph with Title-level and Title
        :param level: Title-level
        :param title: Title
        :type level: int
        """
        super().__init__()
        self.SubContents = []
        self.Level = level
        self.Title = title

    def __str__(self):
        """
        get the markdown-expression of this content
        :return: content represented by the class
        """
        r = '#' * self.Level + ' ' + str(self.Title) + '\n\n'
        for subContent in self.SubContents:
            r += str(subContent) + '\n'

        return r

    def add_sub_paragraph(self, title):
        """
        Create and add a sub paragraph to this paragraph
        :param title: Title of the sub paragraph
        :type title: str
        :return: The sub paragraph added
        :type ReportParagraph
        """
        sub_paragraph = ReportParagraph(self.Level + 1, title)
        self.SubContents.append(sub_paragraph)
        return sub_paragraph

    def add_table(self, headers, data, align=0):
        """
        Create and add a table to this paragraph
        :param headers: Headers of the table
        :type headers: list[str]
        :param data: Data of the table
        :type data list[list[str]]
        :param align: Optional. Align of the table, default 0-Central
        :type align: list or int
        :return: The table added
        :type ReportTable
        """
        table = ReportTable(headers, data, align)
        self.SubContents.append(table)
        return table

    def add_plain_content(self, content):
        """
        Add a plain content to the paragraph
        :param content: The content represented by the class
        :type content: str
        :return: Plain content added
        :type ReportPlainContent
        """
        plain_content = ReportPlainContent(content)
        self.SubContents.append(plain_content)
        return plain_content


class Report(ReportParagraph):
    """A markdown report file
    Decorators:
        MarkdownFilePath: full-path of the markdown file
        PDFPath: full-path of the PDF file
    """
    def __init__(self, title, path=''):
        """
        Initialize a report Title and optional Path
        :param path: default directory path to storage files
        :param title: Title
        :type path: str
        :type title str
        """
        super().__init__(1, title)
        self.MarkdownFilePath = join(path,title+".md")
        self.PDFPath = join(path,title+".pdf")

    def save_to_file(self):
        """
        Save the report to markdown file
        """
        file = open(self.MarkdownFilePath, "w+")
        file.write(str(self))
        file.close()

    def compile(self, engine='', font='', template=''):
        """
        Save Markdown and Compile the file to PDF
        :param engine: engine used to compile pdf
        :param font: main font of the pdf
        :param template: tex template for the PDF
        """
        self.save_to_file()
        extra_args=[]
        if template!='':
            extra_args.append('--template=pm-template.latex'+template)    
        if engine!='':
            extra_args.append('--pdf-engine='+engine)
        if font!='':
            extra_args.append('-V mainfont="'+font+'"')

        pypandoc.convert_file(self.MarkdownFilePath, 'pdf', outputfile=self.PDFPath,
                              extra_args=extra_args)
