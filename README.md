# Python OCR 工具类

一个基于 PaddleOCR 的 Python OCR 工具类，支持图片文字识别，第一次使用时会自动检查并下载所需模型。

## 功能特性

- 🚀 基于 PaddleOCR，识别准确率高
- 📱 支持多种语言（中文、英文、多语言混合等）
- 📁 自动检查并下载所需模型
- 🎨 支持多种输出格式（字典、纯文本）
- 💻 支持 CPU 和 GPU 两种模式
- 📊 提供详细的识别结果（文字内容、置信度、 bounding box）

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd python-ocr
```

### 2. 安装依赖

本项目使用 `uv` 管理依赖和虚拟环境。

```bash
# 初始化项目（如果尚未初始化）
uv init

# 安装依赖
uv add paddlepaddle paddleocr
```

## 使用示例

### 基本用法

```python
from ocr_tool import OCRTool

# 创建 OCR 工具实例
ocr_tool = OCRTool(lang='ch+en', use_gpu=False)

# 识别图片
image_path = 'path/to/your/image.jpg'

# 获取字典格式的识别结果
result_dict = ocr_tool.recognize_text(image_path, output_format='dict')
print("识别结果（字典格式）:")
print(result_dict)

# 获取纯文本格式的识别结果
result_text = ocr_tool.recognize_text(image_path, output_format='text')
print("\n识别结果（纯文本格式）:")
print(result_text)
```

### 输出格式说明

#### 字典格式 (`output_format='dict'`)

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

#### 纯文本格式 (`output_format='text'`)

```
示例文字1
示例文字2
```

## 参数说明

### OCRTool 初始化参数

- `lang` (str): 识别语言，默认为 'ch'（中文）
  - 支持的语言组合：'ch'（中文）、'en'（英文）、'ch+en'（中英文混合）等
- `use_gpu` (bool): 是否使用 GPU 加速，默认为 False

### recognize_text 方法参数

- `image_path` (str): 本地图片文件路径
- `output_format` (str): 输出格式，可选 'dict' 或 'text'，默认为 'dict'

## 模型下载

第一次使用时，PaddleOCR 会自动检查所需模型是否存在于本地。如果不存在，会自动下载到以下目录：

- Linux: `~/.paddleocr/`
- Windows: `C:\Users\<用户名>\.paddleocr\`
- macOS: `~/Library/Application Support/paddleocr/`

## 系统要求

- Python 3.8+
- 支持的操作系统：Linux、Windows、macOS
- GPU 支持（可选）：需要安装 CUDA 和 cuDNN

## 性能优化建议

1. **使用 GPU 加速**：如果你的机器有 NVIDIA GPU，并且安装了 CUDA 和 cuDNN，可以将 `use_gpu` 参数设置为 True，以提高识别速度
2. **调整图片大小**：对于过大的图片，可以先进行缩放处理，以减少识别时间
3. **选择合适的语言**：根据图片中的文字语言选择合适的 `lang` 参数，避免不必要的多语言识别

## 常见问题

### Q: 第一次使用时下载模型很慢怎么办？

A: 可以尝试使用国内镜像源加速下载：

```bash
uv config set registry https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 识别准确率不高怎么办？

A: 可以尝试以下方法：
1. 确保图片清晰度足够
2. 调整图片对比度和亮度
3. 使用角度检测（已默认启用）
4. 尝试不同的语言参数

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！