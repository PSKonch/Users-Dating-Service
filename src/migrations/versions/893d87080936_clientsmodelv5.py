"""ClientsModelV5

Revision ID: 893d87080936
Revises: f0a7d28e1b43
Create Date: 2024-10-30 20:45:11.597992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "893d87080936"
down_revision: Union[str, None] = "f0a7d28e1b43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("clients", sa.Column("latitude", sa.Float(), nullable=True))
    op.add_column("clients", sa.Column("longitude", sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("clients", "longitude")
    op.drop_column("clients", "latitude")
    # ### end Alembic commands ###
