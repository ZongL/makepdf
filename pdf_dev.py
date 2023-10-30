# -*- coding:utf-8 -*-
import random
from flask import Flask, render_template, request, redirect, url_for, send_file
#from flasgger import Swagger, swag_from

from PyPDF2 import PdfReader, PdfWriter

import os

app = Flask(__name__)
#swagger = Swagger(app)

'''
@app.route('/', methods=['GET', 'POST'])
@swag_from('swagger.yml')  # 指定Swagger文档的YAML文件
def hello0():
    """
    This is an example API endpoint.

    It returns a JSON response with a "text" key.

    ---
    responses:
      200:
        description: A JSON object with the "text" key.
        schema:
          type: object
          properties:
            text:
              type: string
              example: Hello zongliang BotUser test
    """
    return
    {"text":"Hello zongliang BotUser test "}
'''

@app.route('/')
def index():
    project_path = 'D:/python_dev/pdf_web'
    file_tree = generate_file_tree(project_path)
    return render_template('index.html', file_tree=file_tree)


@app.route('/download_merged_pdf')
def download_merged_pdf():
    merged_pdf_path = 'merged.pdf'  # 合并后的PDF文件路径
    return send_file(merged_pdf_path, as_attachment=True)


def generate_file_tree(path):
    file_tree = []
    for root, dirs, files in os.walk(path):
        root_dir = {
            'name': os.path.basename(root),
            'type': 'directory',
            'children': []
        }
        for file in files:
            root_dir['children'].append({
                'name': file,
                'type': 'file'
            })
        file_tree.append(root_dir)
    return file_tree


def PDF_delete(paths,index):
    #参数是一个整数列表，列表里是要删除的页码
    output = PdfWriter()  # 声明一个用于输出PDF的实例
    input1 = PdfReader(paths)  # 读取本地PDF文件
    pages = len(input1.pages) # 读取文档的页数
    for i in range(pages):
        if (i+1) in index:
            continue  # 待删除的页面
        output.add_page(input1.pages[i])  # 读取PDF的第i页，添加到输出Output实例中
    outputStream = open('newfile.pdf', "wb")
    output.write(outputStream)  # 把编辑后的文档保存到本地


@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    pdf_files = request.files.getlist('pdf_files')

    pdf_writer = PdfWriter()
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in range(len(pdf_reader.pages)):
            # Add each page to the writer object
            pdf_writer.add_page(pdf_reader.pages[page])
    # Write out the merged PDF
    merged_pdf_path = 'merged.pdf'
    with open(merged_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    return redirect(url_for('index'))

def page_rotation(old_file, new_file):
    """
    PDF页面旋转
    :param old_file: 需要旋转的PDF文件
    :param new_file: 旋转后的PDF文件
    :return:
    """
    pdf = PdfReader(old_file)
    page_num = len(pdf.pages)
    pdf_writer = PdfWriter()
    for i in range(page_num):
        # orientation = pdf.getPage(i).get('/Rotate')   # 获取页面的旋转角度
        size = pdf.pages[i].mediabox  # 获取页面大小值（长、宽）
        #x, y = size.getUpperRight_x(), size.getUpperRight_y()
        x=100
        y=20
        if x > y:
            # 顺时针旋转90度  90的倍数
            page = pdf.pages[i].rotate(90)
            # 逆时针旋转90度  90的倍数
            # page = pdf.getPage(i).rotateCounterClockwise(90)
            pdf_writer.add_page(page)
        else:
            # 不旋转
            page = pdf.pages[i].rotate(0)
            pdf_writer.add_pge(page)
    with open(new_file, 'wb') as f:
        pdf_writer.write(f)




if __name__ == '__main__':

    #paths = ['2.pdf', '1.pdf']
    #merge_pdfs(paths, output='merged2.pdf')

    app.run(debug=False)
#http://172.22.188.77:5000/apidocs/