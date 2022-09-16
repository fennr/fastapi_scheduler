"""add year to song

Revision ID: 5b82d129ee4f
Revises: a6e506109d15
Create Date: 2022-09-16 22:26:12.606444

"""
from alembic import op
import sqlalchemy as sa

import sqlmodel  # added



# revision identifiers, used by Alembic.
revision = '5b82d129ee4f'
down_revision = 'a6e506109d15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('year', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'year')
    # ### end Alembic commands ###