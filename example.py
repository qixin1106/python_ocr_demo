#!/usr/bin/env python3
"""
OCR工具类示例脚本
"""

from ocr_tool import OCRTool
import os

def main():
    print("=== OCR工具类示例 ===")
    
    # 创建OCR工具实例
    try:
        ocr_tool = OCRTool(lang='ch')
        print("✓ OCR工具初始化成功")
    except Exception as e:
        print(f"✗ OCR工具初始化失败: {str(e)}")
        # 检查示例图片
    example_image = 'example_image.png'
    if not os.path.exists(example_image):
        print(f"✗ 示例图片不存在: {example_image}")
        print("请确保example_image.png文件在当前目录")
        return False
    
    print(f"\n示例图片: {example_image}")
    print("图片内容:")
    print("  Python OCR Demo")
    print("  这是一个测试图片")
    print("  包含中文和英文文字")
    print("  OCR Tool Class")
    print("  2024年1月")
    
    # 注意：PaddleOCR可能无法直接处理SVG格式图片
    # 我们需要先将SVG转换为PNG或JPG格式
    print("\n注意：PaddleOCR可能无法直接处理SVG格式图片")
    print("建议将SVG转换为PNG或JPG格式后再进行识别")
    print("\n可以使用以下命令将SVG转换为PNG：")
    print("  convert example_image.svg example_image.png")
    print("\n或者使用Python的PIL库：")
    print("  from PIL import Image")
    print("  import cairosvg")
    print("  cairosvg.svg2png(url='example_image.svg', write_to='example_image.png')")
    
    # 如果存在转换后的PNG图片，尝试识别
    if os.path.exists('example_image.png'):
        print("\n✓ 发现转换后的PNG图片，开始识别...")
        try:
            result = ocr_tool.recognize_text('example_image.png', output_format='text')
            print("\n识别结果:")
            if result:
                print(result)
            else:
                print("未识别到任何文字")
        except Exception as e:
            print(f"✗ 识别失败: {str(e)}")
    
    print("\n=== 示例结束 ===")

if __name__ == "__main__":
    main()