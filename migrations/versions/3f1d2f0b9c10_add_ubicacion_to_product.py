"""add ubicacion to product

Revision ID: 3f1d2f0b9c10
Revises: 6a5c7b6292e2
Create Date: 2026-02-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f1d2f0b9c10'
down_revision = '6a5c7b6292e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ubicacion', sa.String(length=100), nullable=True))


def downgrade():
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('ubicacion')
