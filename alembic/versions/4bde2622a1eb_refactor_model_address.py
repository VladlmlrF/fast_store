"""refactor model Address

Revision ID: 4bde2622a1eb
Revises: bf488b3519d6
Create Date: 2024-02-15 14:20:20.768115

"""
from typing import Sequence
from typing import Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4bde2622a1eb"
down_revision: Union[str, None] = "bf488b3519d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE address ALTER COLUMN postal_code TYPE INTEGER USING postal_code::integer"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE address ALTER COLUMN postal_code TYPE VARCHAR USING postal_code::text"
    )
    # ### end Alembic commands ###