"""empty message

Revision ID: a3827107c867
Revises: 6d146288179d
Create Date: 2023-07-19 23:33:14.787714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3827107c867'
down_revision = '6d146288179d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.drop_constraint('Client_type_fkey', type_='foreignkey')
        batch_op.drop_column('type')

    with op.batch_alter_table('FavouriteProducts', schema=None) as batch_op:
        batch_op.drop_constraint('FavouriteProducts_client_fkey', type_='foreignkey')
        batch_op.drop_constraint('FavouriteProducts_product_fkey', type_='foreignkey')
        batch_op.drop_column('product')
        batch_op.drop_column('client')

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_type_id', sa.Integer(), nullable=False))
        batch_op.alter_column('logo',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('promo_images',
               existing_type=postgresql.ARRAY(sa.TEXT()),
               type_=sa.ARRAY(sa.String()),
               existing_nullable=True)
        batch_op.alter_column('web_site',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.drop_constraint('Product_type_fkey', type_='foreignkey')
        batch_op.drop_constraint('Product_client_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ProductType', ['product_type_id'], ['id'])
        batch_op.drop_column('registered')
        batch_op.drop_column('client')
        batch_op.drop_column('type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('client', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('registered', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Product_client_fkey', 'Client', ['client'], ['id'])
        batch_op.create_foreign_key('Product_type_fkey', 'UserType', ['type'], ['id'])
        batch_op.alter_column('web_site',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('promo_images',
               existing_type=sa.ARRAY(sa.String()),
               type_=postgresql.ARRAY(sa.TEXT()),
               existing_nullable=True)
        batch_op.alter_column('logo',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.drop_column('product_type_id')

    with op.batch_alter_table('FavouriteProducts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('product', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('FavouriteProducts_product_fkey', 'Product', ['product'], ['id'])
        batch_op.create_foreign_key('FavouriteProducts_client_fkey', 'Client', ['client'], ['id'])

    with op.batch_alter_table('Client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('Client_type_fkey', 'UserType', ['type'], ['id'])

    # ### end Alembic commands ###
