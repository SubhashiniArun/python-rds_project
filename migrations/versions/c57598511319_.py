"""empty message

Revision ID: c57598511319
Revises: 15ea2f508191
Create Date: 2025-05-21 15:57:22.385257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c57598511319'
down_revision = '15ea2f508191'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('access_token_encrypted',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=800),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('access_token_encrypted',
               existing_type=sa.String(length=800),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###
