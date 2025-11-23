from paddleocr import PaddleOCR
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRTool:
    """
    OCR工具类，用于识别图片中的文字内容
    第一次使用时会自动检查并下载所需模型
    """
    
    def __init__(self, lang='ch'):
        """
        初始化OCR工具
        
        Args:
            lang (str): 识别语言，默认为中文('ch')，支持多种语言组合如'ch+en'
        """
        self.lang = lang
        self.ocr = None
        self._initialize_ocr()
    
    def _initialize_ocr(self):
        """初始化OCR实例，检查并下载模型"""
        try:
            logger.info(f"初始化OCR工具，语言: {self.lang}")
            # PaddleOCR会自动检查模型是否存在，不存在则下载
            self.ocr = PaddleOCR(
                # lang=self.lang,
                # use_angle_cls=True  # 启用角度检测
                enable_mkldnn=False,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False
            )
            logger.info("OCR工具初始化成功")
        except Exception as e:
            logger.error(f"OCR工具初始化失败: {str(e)}")
            raise
    
    def recognize_text(self, image_path, output_format='dict'):
        """
        识别图片中的文字内容
        
        Args:
            image_path (str): 本地图片文件路径
            output_format (str): 输出格式，可选'dict'或'text'，默认为'dict'
            
        Returns:
            根据output_format返回不同格式的识别结果
            - 'dict': 返回包含详细信息的字典
            - 'text': 返回纯文本字符串
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
        if not self.ocr:
            self._initialize_ocr()
        
        try:
            logger.info(f"开始识别图片: {image_path}")
            # 执行OCR识别
            result = self.ocr.predict(image_path)
            logger.debug(f"OCR原始结果: {result}")
            
            if output_format == 'dict':
                return self._format_result_dict(result)
            elif output_format == 'text':
                return self._format_result_text(result)
            else:
                raise ValueError(f"不支持的输出格式: {output_format}")
                
        except Exception as e:
            logger.error(f"图片识别失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def _format_result_dict(self, result):
        """
        将OCR结果格式化为字典形式
        
        Args:
            result: OCR原始识别结果
            
        Returns:
            dict: 格式化后的OCR结果
        """
        formatted_result = {
            'texts': [],
            'bboxes': [],
            'confidences': []
        }
        
        if result:
            # 检查结果是否为字典格式
            if isinstance(result, dict):
                # 提取字典中的文本信息
                if 'text' in result:
                    formatted_result['texts'].append(result['text'])
                if 'bbox' in result:
                    formatted_result['bboxes'].append(result['bbox'])
                if 'confidence' in result:
                    formatted_result['confidences'].append(result['confidence'])
                elif 'prob' in result:
                    formatted_result['confidences'].append(result['prob'])
            # 检查结果是否为列表格式
            elif isinstance(result, list):
                for line in result:
                    if isinstance(line, dict):
                        # 提取字典中的文本信息
                        if 'text' in line:
                            formatted_result['texts'].append(line['text'])
                        if 'bbox' in line:
                            formatted_result['bboxes'].append(line['bbox'])
                        if 'confidence' in line:
                            formatted_result['confidences'].append(line['confidence'])
                        elif 'prob' in line:
                            formatted_result['confidences'].append(line['prob'])
                    elif isinstance(line, (list, tuple)) and len(line) >= 2:
                        # 提取列表中的文本信息
                        bbox = line[0]
                        text = line[1][0] if isinstance(line[1], tuple) and len(line[1]) >= 2 else line[1]
                        confidence = line[1][1] if isinstance(line[1], tuple) and len(line[1]) >= 2 else 1.0
                        
                        formatted_result['texts'].append(text)
                        formatted_result['bboxes'].append(bbox)
                        formatted_result['confidences'].append(confidence)
        
        return formatted_result
    
    def _format_result_text(self, result):
        """
        将OCR结果格式化为纯文本形式
        
        Args:
            result: OCR原始识别结果
            
        Returns:
            str: 格式化后的纯文本
        """
        text_result = ""
        
        if result:
            # 检查结果是否为字典格式
            if isinstance(result, dict):
                if 'text' in result:
                    text_result += result['text'] + '\n'
            # 检查结果是否为列表格式
            elif isinstance(result, list):
                for line in result:
                    if isinstance(line, dict):
                        if 'text' in line:
                            text_result += line['text'] + '\n'
                    elif isinstance(line, (list, tuple)) and len(line) >= 2:
                        text = line[1][0] if isinstance(line[1], tuple) and len(line[1]) >= 2 else line[1]
                        text_result += text + '\n'
        
        return text_result.strip()

# 示例用法
if __name__ == "__main__":
    # 创建OCR工具实例
    ocr_tool = OCRTool(lang='ch+en')
    
    # 测试图片路径（请替换为实际图片路径）
    test_image_path = 'example_image.png'
    
    if os.path.exists(test_image_path):
        # 以字典格式输出结果
        result_dict = ocr_tool.recognize_text(test_image_path, output_format='dict')
        print("识别结果（字典格式）:")
        print(result_dict)
        
        # 以纯文本格式输出结果
        result_text = ocr_tool.recognize_text(test_image_path, output_format='text')
        print("\n识别结果（纯文本格式）:")
        print(result_text)
    else:
        print(f"测试图片不存在: {test_image_path}")
        print("请将测试图片放在当前目录或修改test_image_path变量")