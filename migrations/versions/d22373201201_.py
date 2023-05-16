"""empty message

Revision ID: d22373201201
Revises: 
Create Date: 2023-05-16 23:19:42.026237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd22373201201'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['ads.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'ad_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('ads')
    op.drop_table('users')
    # ### end Alembic commands ###
