# model_finetuning/trainers/pet_diagnosis_trainer.py
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
from app.core.config import MODEL_DIR  # 假设在 core/config.py 中定义模型存储路径

def finetune_pet_diagnosis_model():
    """微调模型用于宠物疾病诊断"""
    # 加载已清洗的数据集（可来自爬虫或本地文件）
    dataset = load_dataset("json", data_files="path/to/cleaned_pet_data.json")
    # 加载基础模型（如 BERT 中文模型）
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-chinese",
        num_labels=10  # 假设区分 10 种常见宠物疾病
    )
    # 配置训练参数
    training_args = TrainingArguments(
        output_dir=MODEL_DIR / "pet_diagnosis",  # 模型保存路径
        num_train_epochs=3,
        per_device_train_batch_size=16,
        logging_steps=100,
    )
    # 初始化 Trainer 并开始训练
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
    )
    trainer.train()
    return model