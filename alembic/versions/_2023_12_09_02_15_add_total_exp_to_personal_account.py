"""add total exp to personal account

Revision ID: 83efe801a8b7
Revises: 962e9ce075dd
Create Date: 2023-12-09 02:15:39.162048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83efe801a8b7"
down_revision: Union[str, None] = "962e9ce075dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("personal_account", sa.Column("total_exp", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("personal_account", "total_exp")
    # ### end Alembic commands ###
