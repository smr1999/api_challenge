"""empty message

Revision ID: 27d2ab221dcd
Revises: d22373201201
Create Date: 2023-05-16 23:29:14.917147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d2ab221dcd'
down_revision = 'd22373201201'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.String(), nullable=False))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('comment')

    # ### end Alembic commands ###