#Provide by SecretMoko

import fitz  # PyMuPDF
import os
from PIL import Image

def extract_images_from_pdf(pdf_path, output_folder):
    """
    使用PyMuPDF从PDF中提取所有图片
    """
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)
    
    image_count = 0
    
    # 遍历每一页
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # 获取图片列表
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            # 获取图片引用
            xref = img[0]
            
            # 提取图片数据
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # 保存图片
            image_filename = f"图片_第{page_num+1}页_第{img_index+1}张.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)
            
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            image_count += 1
            print(f"✅ 已保存: {image_filename}")
    
    pdf_document.close()
    print(f"🎉 完成！总共提取了 {image_count} 张图片")
    print(f"📁 图片保存在: {os.path.abspath(output_folder)}")

if __name__ == "__main__":
    print("=" * 50)
    print("PDF图片提取工具")
    print("=" * 50)
    
    # 获取PDF文件路径
    pdf_path = input("请将PDF文件拖拽到此处，然后按回车: ").strip()
    
    # 清理路径
    pdf_path = pdf_path.strip('"').strip("'")
    
    # 自动生成输出文件夹
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = f"{pdf_name}_提取的图片"
    
    # 验证文件
    if not pdf_path.lower().endswith('.pdf'):
        print("❌ 错误：请选择PDF文件！")
    elif not os.path.exists(pdf_path):
        print(f"❌ 错误：文件不存在 - {pdf_path}")
    else:
        print(f"📄 PDF文件: {os.path.basename(pdf_path)}")
        print(f"📁 输出到: {output_folder}")
        print("⏳ 正在提取图片，请稍候...")
        print("-" * 50)
        
        try:
            extract_images_from_pdf(pdf_path, output_folder)
        except Exception as e:
            print(f"❌ 提取过程中出错: {e}")
        finally:
            input("按回车键退出...")