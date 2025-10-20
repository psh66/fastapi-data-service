def save_data(data_list, db, model_class):
    try:
        print("待存储数据数量:", len(data_list))
        for i, data in enumerate(data_list):
            print(f"第{i+1}条数据:", data)
            db.add(model_class(**data))
        db.commit()
        print("数据存储成功")
    except Exception as e:
        db.rollback()
        print("存储异常:", e)