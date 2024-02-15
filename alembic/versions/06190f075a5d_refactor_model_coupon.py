"""refactor model Coupon

Revision ID: 06190f075a5d
Revises: 4bde2622a1eb
Create Date: 2024-02-15 16:48:39.435607

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "06190f075a5d"
down_revision: Union[str, None] = "4bde2622a1eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("coupon", sa.Column("active", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("coupon", "active")
    # ### end Alembic commands ###
