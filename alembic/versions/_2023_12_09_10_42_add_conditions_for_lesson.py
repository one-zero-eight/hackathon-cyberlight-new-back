"""add conditions for lesson

Revision ID: 1a0274c4cbfe
Revises: 7dc29d1cb4f7
Create Date: 2023-12-09 10:42:37.751106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1a0274c4cbfe"
down_revision: Union[str, None] = "7dc29d1cb4f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    condition_type = postgresql.ENUM("nothing", "min_level", "reward", "battlepass", name="conditiontype")
    condition_type.create(op.get_bind())

    op.add_column(
        "lessons",
        sa.Column(
            "condition_type",
            sa.Enum("nothing", "min_level", "reward", "battlepass", name="conditiontype"),
            nullable=False,
        ),
    )
    op.add_column("lessons", sa.Column("recommended_level", sa.Integer(), nullable=True))
    op.add_column("lessons", sa.Column("min_level", sa.Integer(), nullable=True))
    op.add_column("lessons", sa.Column("reward_id", sa.Integer(), nullable=True))
    op.add_column("lessons", sa.Column("battlepass_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "lessons", "reward", ["reward_id"], ["id"])
    op.create_foreign_key(None, "lessons", "battle_pass", ["battlepass_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "lessons", type_="foreignkey")
    op.drop_constraint(None, "lessons", type_="foreignkey")
    op.drop_column("lessons", "battlepass_id")
    op.drop_column("lessons", "reward_id")
    op.drop_column("lessons", "min_level")
    op.drop_column("lessons", "recommended_level")
    op.drop_column("lessons", "condition_type")
    # ### end Alembic commands ###
