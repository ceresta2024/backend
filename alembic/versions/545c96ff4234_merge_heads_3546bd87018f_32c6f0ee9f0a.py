"""merge heads(3546bd87018f-32c6f0ee9f0a)

Revision ID: 545c96ff4234
Revises: 32c6f0ee9f0a, 3546bd87018f
Create Date: 2024-04-03 10:09:28.667245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545c96ff4234'
down_revision: Union[str, None] = ('32c6f0ee9f0a', '3546bd87018f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
