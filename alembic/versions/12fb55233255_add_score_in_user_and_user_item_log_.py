"""add score in user and user item log model

Revision ID: 12fb55233255
Revises: f411a00c25fc
Create Date: 2024-04-08 17:04:14.998096

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "12fb55233255"
down_revision: Union[str, None] = "f411a00c25fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("score", sa.Integer(), nullable=False, server_default="0")
    )
    op.add_column(
        "user_item_log",
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_item_log", "score")
    op.drop_column("user", "score")
    # ### end Alembic commands ###
