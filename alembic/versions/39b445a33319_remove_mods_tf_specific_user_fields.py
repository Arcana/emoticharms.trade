"""Remove mods.tf specific user fields

Revision ID: 39b445a33319
Revises: 4851d66f53f3
Create Date: 2015-07-18 08:55:16.853587

"""

# revision identifiers, used by Alembic.
revision = '39b445a33319'
down_revision = '4851d66f53f3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'upload_credits')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('upload_credits', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    ### end Alembic commands ###
