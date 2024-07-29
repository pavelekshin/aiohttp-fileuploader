"""add geo table

Revision ID: d57ba2227962
Revises: 4e6a7c537423
Create Date: 2024-07-29 15:36:49.647580

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d57ba2227962"
down_revision: Union[str, None] = "4e6a7c537423"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "geo",
        sa.Column("anzsic06", sa.String(), nullable=False),
        sa.Column("area", sa.String(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("geo_count", sa.Integer(), nullable=False),
        sa.Column("ec_count", sa.Integer(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("geo")
    # ### end Alembic commands ###
