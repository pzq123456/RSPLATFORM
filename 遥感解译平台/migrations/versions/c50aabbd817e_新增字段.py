"""新增字段

Revision ID: c50aabbd817e
Revises: 006207ba3dce
Create Date: 2022-06-21 18:25:48.387203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50aabbd817e'
down_revision = '006207ba3dce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('img_path', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'img_path')
    # ### end Alembic commands ###
