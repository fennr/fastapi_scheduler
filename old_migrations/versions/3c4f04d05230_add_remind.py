"""add Remind

Revision ID: 3c4f04d05230
Revises: 96265422d15e
Create Date: 2023-04-13 15:54:10.522803
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3c4f04d05230'
down_revision = '96265422d15e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'remind',
        sa.Column(
            'dtime',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'event_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            'connector', sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ['event_id'], ['task.id'], name='remind_event_id_fkey'
        ),
        sa.PrimaryKeyConstraint('id', name='remind_pkey'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('remind')
    # ### end Alembic commands ###
