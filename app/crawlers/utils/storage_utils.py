def save_data(data_list, db, model_class):  # data_list：清洗后的有效数据；db：数据库会话；model_class：模型（如ZhihuHot）
    try:
        for data in data_list:  # 遍历每条数据
            # 创建模型实例：将字典数据转为数据库记录（**data解包字典，如{"rank":1}→rank=1）
            db.add(model_class(** data))  # 添加到会话（暂存，未写入磁盘）
        db.commit()  # 提交事务（批量写入数据库，真正生效）
        print("数据提交成功！开始验证查询...")
        # 提交后立即查询最新数据（验证是否真的存入）
        latest_data = db.query(model_class).order_by(model_class.id.desc()).first()
        print("最新存入的数据：", latest_data.__dict__ if latest_data else "无数据")  # 打印最新数据详情
    except Exception as e:  # 捕获存储异常（如字段不匹配、类型错误）
        db.rollback()  # 回滚事务（避免部分数据写入导致数据库不一致）
        print("存储异常：", str(e))  # 打印异常信息（方便定位问题）