# # app/data_cleaning/api.py
# from fastapi import APIRouter
# from app.data_cleaning.pipelines import medical_text_pipeline  # 假设已实现清洗流水线
#
# router = APIRouter(prefix="/data-cleaning", tags=["数据清洗"])  # 分组标签便于Swagger区分
#
# @router.post("/clean_medical_text")
# def clean_medical_text_api(text: str):
#     """清洗宠物医疗文本（如症状描述）"""
#     cleaned_text = medical_text_pipeline(text)
#     return {"cleaned_text": cleaned_text}