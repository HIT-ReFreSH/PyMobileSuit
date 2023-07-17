<div  align=center>
    <img src="Plastic-Metal.png" width = 30% height = 30%  />
</div>

# PlasticMetal.pyLabOn

![PyPI](https://img.shields.io/pypi/v/pylabon?style=flat-square)
![GitHub](https://img.shields.io/github/license/Plastic-Metal/pyLabOn?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/Plastic-Metal/pyLabOn?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Plastic-Metal/pyLabOn/deploy?style=flat-square)
![PyPI - Format](https://img.shields.io/pypi/format/pylabon?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pylabon?style=flat-square)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/pylabon?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/Plastic-Metal/pyLabOn?style=flat-square)
![GitHub code size](https://img.shields.io/github/languages/code-size/Plastic-Metal/pyLabOn?style=flat-square)
=

[View at PyPI](https://pypi.org/project/pylabon/)

Light-weight tool to generate markdown-formatted lab reports. For python.

## Setup

```shell script
pip install pylabon
```

**You may need to install some tex engines by your self.**

## Usage

### Create a report

```python
from pyLabOn import Report

# Name can be anything you like; 
# you may specific path if the report files should not be generated in ./
my_report=Report("demo")
```

### Add content to report

```python
# You can also add formula, code, and anything
my_report.add_plain_content("Hello, pyLabOn")
```

### Add a sub paragraph

```python
# The return value of .add_sub_paragraph() is the sub paragraph created
# You can add sub paragraphs to sub paragraph in the same way
sub_para=my_report.add_sub_paragraph("SubParagraph")

# Add contents to the sub paragraph just like to the report
sub_para.add_plain_content("There is a Table")
```

### Add a table

```python
# Add a Table to the sub paragraph
# (List,List[List] [,Align=0])->Table
# Align: 0=Central, -1=Left, 1=Right
# Align can be a list or a single int
# The return value of .add_table() is the table created
sub_para.add_table(["index"],[[i] for i in range(0,10)])
```

### Save to Markdown and Compile to PDF

```python
# This command generates .md to my_report.MarkdownFilePath, and .pdf to my_report.PDFPath
# You can customize your engine, font and template
# If you just want a Markdown file, use my_report.save_to_file() instead
my_report.compile()
```

