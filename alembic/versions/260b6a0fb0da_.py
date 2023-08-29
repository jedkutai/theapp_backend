"""empty message

Revision ID: 260b6a0fb0da
Revises: 5228c1b37538
Create Date: 2023-08-27 19:12:33.416665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '260b6a0fb0da'
down_revision: Union[str, None] = '5228c1b37538'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
