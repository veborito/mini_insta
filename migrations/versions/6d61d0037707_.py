"""empty message

Revision ID: 6d61d0037707
Revises: 1d9182631a45
Create Date: 2023-05-29 13:35:15.728223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d61d0037707'
down_revision = '1d9182631a45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'photo', ['photo_id'], ['id'])

    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('photo_id')

    # ### end Alembic commands ###
