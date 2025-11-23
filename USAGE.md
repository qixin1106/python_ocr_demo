# OCR 工具类使用说明

本文档详细介绍了如何使用 `OCRTool` 类进行图片文字识别。

## 1. 安装

### 1.1 安装依赖

```bash
uv add paddlepaddle paddleocr
```

### 1.2 导入类

```python
from ocr_tool import OCRTool
```

## 2. 初始化

### 2.1 基本初始化

```python
ocr_tool = OCRTool()
```

### 2.2 指定语言

```python
# 中文
ocr_tool = OCRTool(lang='ch')

# 英文
ocr_tool = OCRTool(lang='en')

# 中英文混合
ocr_tool = OCRTool(lang='ch+en')
```

### 2.3 使用 GPU 加速

```python
ocr_tool = OCRTool(use_gpu=True)
```

## 3. 识别图片

### 3.1 基本用法

```python
image_path = 'path/to/your/image.jpg'
result = ocr_tool.recognize_text(image_path)
```

### 3.2 输出格式

#### 3.2.1 字典格式（默认）

```python
result = ocr_tool.recognize_text(image_path, output_format='dict')
```

返回结果示例：

```python
{
    'success': True,
    'total_texts': 2,
    'texts': [
        {
            'text': '示例文字1',
            'confidence': 0.99,
            'bbox': [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        },
        {
            'text': '示例文字2',
            'confidence': 0.98,
            'bbox': [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
    ]
}
```

#### 3.2.2 纯文本格式

```python
result = ocr_tool.recognize_text(image_path, output_format='text')
```

返回结果示例：

```
示例文字1
示例文字2
```

## 4. 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- GIF
- TIFF
- SVG（需要额外处理）

## 5. 模型管理

### 5.1 自动下载

第一次使用时，PaddleOCR 会自动检查所需模型是否存在于本地。如果不存在，会自动下载到以下目录：

- Linux: `~/.paddleocr/`
- Windows: `C:\Users\<用户名>\.paddleocr\`
- macOS: `~/Library/Application Support/paddleocr/`

### 5.2 手动下载

如果自动下载失败，可以手动下载模型文件并放置到上述目录中。

模型下载地址：
- [PaddleOCR 模型库](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/models_list.md)

## 6. 异常处理

### 6.1 文件不存在

```python
try:
    result = ocr_tool.recognize_text('non_existent_image.jpg')
except FileNotFoundError as e:
    print(f"错误: {str(e)}")
```

### 6.2 识别失败

```python
try:
    result = ocr_tool.recognize_text('corrupted_image.jpg')
except Exception as e:
    print(f"识别失败: {str(e)}")
```

## 7. 性能优化

### 7.1 调整图片大小

对于过大的图片，可以先进行缩放处理：

```python
from PIL import Image
import os

def resize_image(image_path, max_size=1024):
    """调整图片大小，最大边长不超过max_size"""
    image = Image.open(image_path)
    width, height = image.size
    
    if width > height and width > max_size:
        height = int(height * (max_size / width))
        width = max_size
    elif height > max_size:
        width = int(width * (max_size / height))
        height = max_size
    
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
    
    # 保存为临时文件
    temp_path = f"{os.path.splitext(image_path)[0]}_resized.jpg"
    resized_image.save(temp_path, quality=95)
    
    return temp_path

# 使用示例
resized_image_path = resize_image('large_image.jpg')
result = ocr_tool.recognize_text(resized_image_path)
```

### 7.2 预处理图片

可以对图片进行预处理，提高识别准确率：

```python
from PIL import Image, ImageEnhance
import os

def preprocess_image(image_path):
    """预处理图片，提高识别准确率"""
    image = Image.open(image_path)
    
    # 转换为灰度图
    image = image.convert('L')
    
    # 增强对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # 增强亮度
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.5)
    
    # 保存为临时文件
    temp_path = f"{os.path.splitext(image_path)[0]}_preprocessed.jpg"
    image.save(temp_path)
    
    return temp_path

# 使用示例
preprocessed_image_path = preprocess_image('low_quality_image.jpg')
result = ocr_tool.recognize_text(preprocessed_image_path)
```

## 8. 批量处理

### 8.1 批量识别图片

```python
import os

def batch_recognize_images(image_dir):
    """批量识别目录中的所有图片"""
    ocr_tool = OCRTool(lang='ch+en')
    results = []
    
    # 获取目录中的所有图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    for filename in os.listdir(image_dir):
        if os.path.splitext(filename)[1].lower() in image_extensions:
            image_path = os.path.join(image_dir, filename)
            try:
                result = ocr_tool.recognize_text(image_path, output_format='dict')
                results.append({
                    'filename': filename,
                    'result': result
                })
                print(f"成功识别: {filename}")
            except Exception as e:
                print(f"识别失败: {filename} - {str(e)}")
    
    return results

# 使用示例
image_directory = 'path/to/images'
batch_results = batch_recognize_images(image_directory)
```

### 8.2 保存结果到文件

```python
import json

def save_results_to_file(results, output_file):
    """将识别结果保存到JSON文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# 使用示例
save_results_to_file(batch_results, 'ocr_results.json')
```

## 9. 常见问题

### 9.1 第一次使用时下载模型很慢

可以尝试使用国内镜像源加速下载：

```bash
uv config set registry https://pypi.tuna.tsinghua.edu.cn/simple
```

### 9.2 识别准确率不高

1. 确保图片清晰度足够
2. 调整图片对比度和亮度
3. 使用角度检测（已默认启用）
4. 尝试不同的语言参数
5. 对图片进行预处理

### 9.3 GPU 加速不生效

1. 确保安装了 CUDA 和 cuDNN
2. 确保安装了 GPU 版本的 PaddlePaddle
3. 检查 `use_gpu` 参数是否设置为 True

## 10. 示例代码

### 10.1 完整示例

```python
from ocr_tool import OCRTool
import os
import json

def main():
    # 创建OCR工具实例
    ocr_tool = OCRTool(lang='ch+en', use_gpu=False)
    
    # 图片目录
    image_dir = 'images'
    
    # 结果保存文件
    output_file = 'ocr_results.json'
    
    # 批量识别图片
    results = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    for filename in os.listdir(image_dir):
        if os.path.splitext(filename)[1].lower() in image_extensions:
            image_path = os.path.join(image_dir, filename)
            print(f"正在识别: {filename}")
            
            try:
                # 识别图片
                result_dict = ocr_tool.recognize_text(image_path, output_format='dict')
                
                # 保存结果
                results.append({
                    'filename': filename,
                    'image_path': image_path,
                    'result': result_dict
                })
                
                print(f"成功识别: {filename} - 发现 {result_dict['total_texts']} 段文字")
                
            except Exception as e:
                print(f"识别失败: {filename} - {str(e)}")
    
    # 保存所有结果到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n所有识别完成，结果保存到: {output_file}")
    print(f"成功识别: {len([r for r in results if r['result']['success']])} 张图片")
    print(f"识别失败: {len([r for r in results if not r['result']['success']])} 张图片")

if __name__ == "__main__":
    main()
```