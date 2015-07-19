"""user-pack relation

Revision ID: 308366cb44aa
Revises: 3f4d38db0caf
Create Date: 2015-07-19 20:06:39.133834

"""

# revision identifiers, used by Alembic.
revision = '308366cb44aa'
down_revision = '3f4d38db0caf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user_packs',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pack_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False, server_default="0"),
    sa.ForeignKeyConstraint(['pack_id'], ['pack.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.account_id'], )
    )


def downgrade():
    op.drop_table('user_packs')
