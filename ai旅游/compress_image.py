from PIL import Image
import os

try:
    # 检查输入文件是否存在
    input_file = '学习背景图-超清.png'
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'输入文件 {input_file} 不存在')

    print(f'正在读取图片: {input_file}')
    # 打开图片
    img = Image.open(input_file)

    # 保持原始分辨率
    width, height = img.size

    # 转换为RGB模式（如果需要）
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # 设置输出文件名
    output_file = '学习背景图-超清-小.png'

    # 使用优化的设置保存图片
    print('正在压缩并保存图片...')
    img.save(
        output_file,
        'PNG',
        optimize=True,  # 启用优化
        quality=85,     # 设置质量（对PNG可能无效）
        compress_level=6  # PNG压缩级别（0-9），6是较好的平衡点
    )

    # 获取文件大小信息
    original_size = os.path.getsize(input_file) / (1024 * 1024)  # 转换为MB
    compressed_size = os.path.getsize(output_file) / (1024 * 1024)  # 转换为MB

    print(f'\n压缩完成！')
    print(f'原始文件大小: {original_size:.2f}MB')
    print(f'压缩后文件大小: {compressed_size:.2f}MB')
    print(f'压缩率: {((original_size - compressed_size) / original_size * 100):.2f}%')

except Exception as e:
    print(f'错误: {str(e)}')