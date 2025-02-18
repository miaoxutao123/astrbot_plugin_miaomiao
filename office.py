from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

# Function to create a new Word document with title and subtitle
# 创建一个带有标题和副标题的新Word文档的函数
def create_word_document(file_path, title, subtitle, content, 
                         title_font='Arial', title_size=24, title_color=(0, 0, 0),
                         subtitle_font='Arial', subtitle_size=18, subtitle_color=(0, 0, 0),
                         content_font='Arial', content_size=12, content_color=(0, 0, 0)):
    doc = Document()
    
    title_paragraph = doc.add_heading(title, level=1)
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_paragraph.runs[0]
    title_run.font.name = title_font
    title_run.font.size = Pt(title_size)
    title_run.font.color.rgb = RGBColor(*title_color)

    subtitle_paragraph = doc.add_heading(subtitle, level=2)
    subtitle_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle_paragraph.runs[0]
    subtitle_run.font.name = subtitle_font
    subtitle_run.font.size = Pt(subtitle_size)
    subtitle_run.font.color.rgb = RGBColor(*subtitle_color)

    content_paragraph = doc.add_paragraph(content)
    content_run = content_paragraph.runs[0]
    content_run.font.name = content_font
    content_run.font.size = Pt(content_size)
    content_run.font.color.rgb = RGBColor(*content_color)

    doc.save(file_path)

# Function to modify an existing Word document with additional content
# 修改现有Word文档并添加内容的函数
def modify_word_document(file_path, content, 
                         content_font='Arial', content_size=12, content_color=(0, 0, 0)):
    doc = Document(file_path)
    content_paragraph = doc.add_paragraph(content)
    content_run = content_paragraph.runs[0]
    content_run.font.name = content_font
    content_run.font.size = Pt(content_size)
    content_run.font.color.rgb = RGBColor(*content_color)
    doc.save(file_path)

# Function to create a new Excel workbook with title and data
# 创建一个带有标题和数据的新Excel工作簿的函数
def create_excel_workbook(file_path, sheet_name, title, data, 
                          title_font='Arial', title_size=14, title_color='000000'):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    title_cell = ws.cell(row=1, column=1, value=title)
    title_cell.font = Font(name=title_font, size=title_size, bold=True, color=title_color)

    for row in data:
        ws.append(row)

    wb.save(file_path)

# Function to modify an existing Excel workbook with additional data
# 修改现有Excel工作簿并添加数据的函数
def modify_excel_workbook(file_path, sheet_name, data):
    wb = load_workbook(file_path)
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    for row in data:
        ws.append(row)

    wb.save(file_path)

# General function to handle both Word and Excel documents
# 通用函数来处理Word和Excel文档
def handle_document(doc_type, action, file_path, **kwargs):
    if doc_type == 'word':
        if action == 'create':
            create_word_document(file_path, **kwargs)
        elif action == 'modify':
            modify_word_document(file_path, **kwargs)
    elif doc_type == 'excel':
        if action == 'create':
            create_excel_workbook(file_path, **kwargs)
        elif action == 'modify':
            modify_excel_workbook(file_path, **kwargs)

# Example usage of the functions
# 函数的示例用法

# # 示例：创建一个新的Word文档
# create_word_document(
#     file_path='example.docx',
#     title='主标题',
#     subtitle='副标题',
#     content='这是文档的内容。'
# )

# # 示例：修改现有的Word文档
# modify_word_document(
#     file_path='example.docx',
#     content='这是添加到文档的新内容。'
# )

# # 示例：创建一个新的Excel工作簿
# create_excel_workbook(
#     file_path='example.xlsx',
#     sheet_name='Sheet1',
#     title='工作簿标题',
#     data=[
#         ['列1', '列2', '列3'],
#         [1, 2, 3],
#         [4, 5, 6]
#     ]
# )

# # 示例：修改现有的Excel工作簿
# modify_excel_workbook(
#     file_path='example.xlsx',
#     sheet_name='Sheet1',
#     data=[
#         [7, 8, 9],
#         [10, 11, 12]
#     ]
# )