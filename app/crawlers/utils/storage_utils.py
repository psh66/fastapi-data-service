def save_data(cleaned_data_list, db, model_class):
    """将清洗后的数据存入对应的数据表"""
    for data in cleaned_data_list:
        db_obj = model_class(**data)  # 动态实例化模型
        db.add(db_obj)
    db.commit()