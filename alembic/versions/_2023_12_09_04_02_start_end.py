"""start-end

Revision ID: 7dc29d1cb4f7
Revises: d90480a7bb31
Create Date: 2023-12-09 04:02:48.469470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7dc29d1cb4f7"
down_revision: Union[str, None] = "d90480a7bb31"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("timeslots", sa.Column("end", sa.String(), nullable=False))
    op.alter_column("timeslots", "start", existing_type=sa.INTEGER(), type_=sa.String(), existing_nullable=False)
    op.drop_column("timeslots", "duration")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("timeslots", sa.Column("duration", sa.INTEGER(), autoincrement=False, nullable=False))
    op.alter_column("timeslots", "start", existing_type=sa.String(), type_=sa.INTEGER(), existing_nullable=False)
    op.drop_column("timeslots", "end")
    # ### end Alembic commands ###
