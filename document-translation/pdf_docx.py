import os
from pdf2docx import Converter
from docx import Document
from docx.oxml.ns import qn

def unify_docx_font(docx_path, ascii_font='Times New Roman', eastasia_font='宋体'):
    """
    统一 Word 文档中的字体，解决 pdf2docx 转换后字体混乱的问题
    """
    try:
        doc = Document(docx_path)
        
        # 遍历文档中所有的 rPr (Run Properties) 节点，强制修改字体
        for rPr in doc.element.xpath('.//w:rPr'):
            rFonts = rPr.find(qn('w:rFonts'))
            if rFonts is None:
                from docx.oxml import OxmlElement
                rFonts = OxmlElement('w:rFonts')
                rPr.append(rFonts)
            
            # 设置中文字体和英文字体
            rFonts.set(qn('w:ascii'), ascii_font)
            rFonts.set(qn('w:hAnsi'), ascii_font)
            rFonts.set(qn('w:eastAsia'), eastasia_font)
            rFonts.set(qn('w:cs'), ascii_font)
            
        doc.save(docx_path)
    except Exception as e:
        print(f"统一字体失败: {docx_path}. 错误信息: {e}")

def batch_convert_pdf_to_docx(pdf_folder, docx_folder):
    """
    批量将指定文件夹下的 PDF 转换为 DOCX
    :param pdf_folder: 存放 PDF 的文件夹路径
    :param docx_folder: 存放转换后 DOCX 的文件夹路径
    """
    
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(docx_folder):
        os.makedirs(docx_folder)
        print(f"已创建输出目录: {docx_folder}")

    # 获取文件夹内所有文件
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        print(f"输入文件夹 '{pdf_folder}' 不存在，已自动创建。请将PDF放入后重试。")
        return

    files = os.listdir(pdf_folder)
    
    # 筛选出 pdf 文件
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"未在指定文件夹 {pdf_folder} 中找到 PDF 文件。")
        return

    print(f"共找到 {len(pdf_files)} 个 PDF 文件，准备开始转换...\n")

    for filename in pdf_files:
        pdf_path = os.path.join(pdf_folder, filename)
        
        # 构建输出文件名 (去掉.pdf后缀，加上.docx)
        docx_filename = os.path.splitext(filename)[0] + '.docx'
        docx_path = os.path.join(docx_folder, docx_filename)

        try:
            print(f"正在转换: {filename} ...")
            
            # --- 核心转换代码 ---
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            # -------------------
            
            # 统一字体
            unify_docx_font(docx_path)
            
            print(f"成功: {docx_filename}\n")
            
        except Exception as e:
            print(f"转换失败: {filename}. 错误信息: {e}\n")

    print("所有 PDF 转换任务处理完成！")

if __name__ == '__main__':
    # 默认存放源PDF的文件夹
    input_dir = 'originfiles' 
    # 默认输出的DOCX文件夹 (也是下一步翻译的输入文件夹)
    output_dir = 'docxfiles'

    batch_convert_pdf_to_docx(input_dir, output_dir)
