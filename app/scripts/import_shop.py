from sqlalchemy.dialects.postgresql import insert

from app.models.base import engine
from app.models.shop import Shop

INITIAL_ITEM_QUANTITY = 10


def insert_do_nothing_on_conflicts(table, conn, cols, data_iter):
    stmt = insert(table.table).values(list(data_iter))
    stmt = stmt.on_conflict_do_nothing(index_elements=["item_id"])
    conn.execute(stmt)


def populate_shop_data(df):
    data_top = df.columns
    print(data_top)
    # remove unmatched columns to shop db
    for column in list(df.columns.values):
        if column not in ("created", "updated", "id", "price"):
            df.drop(column, inplace=True, axis="columns")

    # item_ids = [r.item_id for r in next(get_session()).query(Shop).all()]

    # Rename columns to db columns
    df = df.rename(columns={"id": "item_id"})

    df.insert(3, "quantity", INITIAL_ITEM_QUANTITY)

    # populate db
    df.to_sql(
        Shop.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        method=insert_do_nothing_on_conflicts,
    )
