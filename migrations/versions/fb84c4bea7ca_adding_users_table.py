"""Adding users table

Revision ID: fb84c4bea7ca
Revises: 
Create Date: 2024-10-31 11:46:25.209499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb84c4bea7ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('categories')
    op.drop_table('items')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('items',
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.Column('item_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('item_about', sa.VARCHAR(length=500), nullable=False),
    sa.Column('item_class', sa.VARCHAR(length=30), nullable=False),
    sa.Column('item_price', sa.INTEGER(), nullable=False),
    sa.Column('category_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('categories',
    sa.Column('category_id', sa.INTEGER(), nullable=False),
    sa.Column('category_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('category_route', sa.VARCHAR(length=30), nullable=False),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
