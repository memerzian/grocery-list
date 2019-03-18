"""create initial tables

Revision ID: ce8b86620d05
Revises: 
Create Date: 2019-03-18 09:35:25.817637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce8b86620d05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='grc'
    )
    op.create_table('unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='grc'
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('unit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['unit_id'], ['grc.unit.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='grc'
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['grc.ingredient.id'], ),
    sa.ForeignKeyConstraint(['meal_id'], ['grc.meal.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='grc'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe', schema='grc')
    op.drop_table('ingredient', schema='grc')
    op.drop_table('unit', schema='grc')
    op.drop_table('meal', schema='grc')
    # ### end Alembic commands ###
