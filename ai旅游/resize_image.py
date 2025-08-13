from PIL import Image
import cv2
import numpy as np
import os
import sys

try:
    # 检查输入文件是否存在
    input_file = '学习背景图.png'
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'输入文件 {input_file} 不存在')

    print(f'正在读取图片: {input_file}')
    original_img = cv2.imread(input_file)
    if original_img is None:
        raise ValueError('无法读取图片，请确保图片格式正确')

    print('正在进行图像预处理 - 降噪')
    denoised = cv2.fastNlMeansDenoisingColored(original_img, None, 10, 10, 7, 21)

    print('正在进行图像锐化')
    kernel = np.array([[-1, -1, -1],
                      [-1, 9, -1],
                      [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    print('正在应用超分辨率算法')
    scale_factor = 2
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    model_path = 'EDSR_x2.pb'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f'EDSR模型文件 {model_path} 不存在，请确保已下载')

    sr.readModel(model_path)
    sr.setModel('edsr', scale_factor)
    upscaled = sr.upsample(sharpened)

    print('正在调整图片尺寸')
    final_img = cv2.resize(upscaled, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)

    print('正在优化对比度和亮度')
    alpha = 1.2  # 稍微降低对比度
    beta = 10    # 稍微降低亮度
    final_img = cv2.convertScaleAbs(final_img, alpha=alpha, beta=beta)

    output_file = '学习背景图-超清.png'
    print(f'正在保存处理后的图片: {output_file}')
    success = cv2.imwrite(output_file, final_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    if not success:
        raise IOError('保存图片失败')

    print('图片处理完成！')

except Exception as e:
    print(f'错误: {str(e)}')
    sys.exit(1)