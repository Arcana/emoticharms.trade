"""Added user account

Revision ID: 4851d66f53f3
Revises: 
Create Date: 2015-07-18 00:12:33.600046

"""

# revision identifiers, used by Alembic.
revision = '4851d66f53f3'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('account_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=256, collation='utf8_swedish_ci'), nullable=True),
    sa.Column('profile_url', sa.String(length=128), nullable=True),
    sa.Column('avatar_small', sa.String(length=128), nullable=True),
    sa.Column('avatar_medium', sa.String(length=128), nullable=True),
    sa.Column('avatar_large', sa.String(length=128), nullable=True),
    sa.Column('joined', sa.DateTime(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=False),
    sa.Column('next_steam_check', sa.DateTime(), nullable=True),
    sa.Column('user_class', sa.Integer(), nullable=True),
    sa.Column('upload_credits', sa.Integer(), nullable=True),
    sa.Column('signed_in', sa.Boolean(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('account_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###