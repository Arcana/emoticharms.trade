"""Add image column to charms

Revision ID: 437c09969b1e
Revises: 475a20af2e75
Create Date: 2015-07-28 08:03:42.186910

"""

# revision identifiers, used by Alembic.
revision = '437c09969b1e'
down_revision = '475a20af2e75'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('charm', sa.Column('image', sa.String(length=16384, collation='utf8_swedish_ci'), nullable=True))


def downgrade():
    op.drop_column('charm', 'image')
