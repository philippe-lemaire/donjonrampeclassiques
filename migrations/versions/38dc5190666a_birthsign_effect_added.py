"""birthsign_effect added

Revision ID: 38dc5190666a
Revises: d048f2d147a7
Create Date: 2021-10-18 11:11:03.154692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38dc5190666a'
down_revision = 'd048f2d147a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('birthsign_effect', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('characters', 'birthsign_effect')
    # ### end Alembic commands ###
