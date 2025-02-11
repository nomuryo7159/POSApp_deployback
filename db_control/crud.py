# uname() error回避
import platform
print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd

from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import Master, Purchases, PurchaseDetails
from datetime import datetime


def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"


def mytrade(mymodel, data):
    """
    Purchasesテーブルに新規レコードを挿入し、
    挿入されたレコードの trd_id (主キー) だけを返す関数。
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    new_record = mymodel(**data)
    result = None  # ここに最終的な trd_id を格納

    try:
        # トランザクション開始
        with session.begin():
            session.add(new_record)

        # トランザクション確定後に new_record を refresh して
        # DB から採番された trd_id を取得
        session.refresh(new_record)

        new_trd_id = new_record.trd_id

    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        print("一意制約違反などにより挿入に失敗しました")
        # 必要に応じて raise しても構いません

    finally:
        # セッションを閉じる
        session.close()

    return new_trd_id


def myselect(mymodel, code):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.code == code)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for item_info in result:
            result_dict_list.append({
                "prd_id": item_info.prd_id,
                "code": item_info.code,
                "name": item_info.name,
                "price": item_info.price
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def get_trd_record(table, trd_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    trd_record = session.query(table).filter(table.trd_id == trd_id).first()
    session.close()
    return trd_record


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json


def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    trd_id = values.pop("trd_id")

    query = update(mymodel).where(mymodel.trd_id == trd_id).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"


def mydelete(mymodel, prd_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.prd_id == prd_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return prd_id + " is deleted"