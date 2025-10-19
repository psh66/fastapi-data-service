# data_cleaning/pipelines.py
from .cleaners.text_cleaner import clean_medical_text

def medical_text_pipeline(text: str) -> str:
    """文本清洗流水线：组合多步清洗逻辑"""
    text = clean_medical_text(text)
    # 可扩展：添加去停用词、分词等步骤
    return text