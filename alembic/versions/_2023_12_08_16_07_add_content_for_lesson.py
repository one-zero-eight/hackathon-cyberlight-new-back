"""add content for lesson

Revision ID: 8c2668411a39
Revises: ed6fdb3d02c5
Create Date: 2023-12-08 16:07:31.184293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c2668411a39"
down_revision: Union[str, None] = "ed6fdb3d02c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("lessons", sa.Column("content", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("lessons", "content")
    # ### end Alembic commands ###
