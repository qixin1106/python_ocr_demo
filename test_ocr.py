from ocr_tool import OCRTool
import os
import sys

def test_ocr_tool():
    """测试OCR工具类的功能"""
    print("=== OCR工具类测试 ===")
    
    # 创建OCR工具实例
    try:
        ocr_tool = OCRTool(lang='ch')
        print("✓ OCR工具初始化成功")
    except Exception as e:
        print(f"✗ OCR工具初始化失败: {str(e)}")
        return False
    
    # 检查测试图片是否存在
    test_image = 'example_image.png'
    if not os.path.exists(test_image):
        print(f"✗ 测试图片不存在: {test_image}")
        print("请确保example_image.png文件在当前目录")
        return False
    
    # 测试字典格式输出
    try:
        print(f"\n正在识别图片: {test_image}")
        result_dict = ocr_tool.recognize_text(test_image, output_format='dict')
        print("✓ 图片识别成功")
        print(f"  - 识别到 {len(result_dict['texts'])} 段文字")
        
        # 打印所有识别结果
        if result_dict['texts']:
            for i, text_info in enumerate(result_dict['texts']):
                print(f"  - 第{i+1}段: {text_info['text']} (置信度: {text_info['confidence']:.2f})")
        else:
            print("  - 未识别到任何文字")
            
    except Exception as e:
        print(f"✗ 图片识别失败: {str(e)}")
        return False
    
    # 测试纯文本格式输出
    try:
        result_text = ocr_tool.recognize_text(test_image, output_format='text')
        print("\n✓ 纯文本格式转换成功")
        print("  识别结果:")
        if result_text:
            print("  " + result_text.replace('\n', '\n  '))
        else:
            print("  未识别到任何文字")
    except Exception as e:
        print(f"✗ 纯文本格式转换失败: {str(e)}")
        return False
    
    print("\n=== 所有测试通过 ===")
    return True

if __name__ == "__main__":
    success = test_ocr_tool()
    sys.exit(0 if success else 1)