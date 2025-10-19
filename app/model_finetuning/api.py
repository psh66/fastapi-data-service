from transformers import AutoTokenizer
import torch
from model_finetuning.trainers.pet_diagnosis_trainer import finetune_pet_diagnosis_model
from data_cleaning.pipelines import medical_text_pipeline

# 启动时加载模型（仅加载一次，避免重复训练）
model = finetune_pet_diagnosis_model()
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
model.eval()

@router.post("/pet_diagnosis")
def predict_pet_disease(symptoms: str):
    """基于微调模型的宠物疾病诊断接口"""
    # 1. 数据清洗
    cleaned_symptoms = medical_text_pipeline(symptoms)
    # 2. 文本编码（适配模型输入）
    inputs = tokenizer(
        cleaned_symptoms,
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors="pt"
    )
    # 3. 模型推理
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
    # 4. 映射标签到疾病名称
    label_mapping = {
        0: "猫泛白细胞减少症",
        1: "犬细小病毒病",
        2: "猫皮肤真菌病",
        # ... 其他疾病标签
    }
    return {
        "predicted_disease": label_mapping[predicted_label],
        "input_symptoms": cleaned_symptoms
    }