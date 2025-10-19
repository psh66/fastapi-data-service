# data_cleaning/cleaners/text_cleaner.py
import re

def clean_medical_text(text: str) -> str:
    """清洗宠物医疗文本：去除无关符号、标准化术语"""
    # 去除特殊符号
    text = re.sub(r"[^\w\s\u4e00-\u9fa5]", "", text)
    # 标准化疾病术语（如“猫瘟”→“猫泛白细胞减少症”）
    term_mapping = {
        "猫瘟": "猫泛白细胞减少症",
        "犬细小": "犬细小病毒病",
        "猫癣": "猫皮肤真菌病"
    }
    for old, new in term_mapping.items():
        text = text.replace(old, new)
    return text