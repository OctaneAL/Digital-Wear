"""empty message

Revision ID: 153ede58bf4e
Revises: 20ea3bdc9738
Create Date: 2023-07-19 23:57:12.919485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153ede58bf4e'
down_revision = '20ea3bdc9738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_type_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'UserType', ['client_type_id'], ['id'])

    with op.batch_alter_table('FavouriteProducts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'Client', ['client_id'], ['id'])

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'Client', ['client_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('client_id')

    with op.batch_alter_table('FavouriteProducts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('client_id')

    with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('client_type_id')

    # ### end Alembic commands ###
