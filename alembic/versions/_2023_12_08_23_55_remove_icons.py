"""remove icons

Revision ID: 8bd28c795ab0
Revises: 35ebf7f9e06d
Create Date: 2023-12-08 23:55:57.882992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8bd28c795ab0"
down_revision: Union[str, None] = "35ebf7f9e06d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("achievement", "icon")
    op.drop_column("reward", "icon")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("reward", sa.Column("icon", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column("achievement", sa.Column("icon", sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
