def save_data(data_list, db, model_class):
    try:
        for data in data_list:
            db.add(model_class(**data))
        db.commit()
        print("数据提交成功！开始验证查询...")
        # 提交后立即查询最新数据
        latest_data = db.query(model_class).order_by(model_class.id.desc()).first()
        print("最新存入的数据：", latest_data.__dict__ if latest_data else "无数据")
    except Exception as e:
        db.rollback()
        print("存储异常：", str(e))