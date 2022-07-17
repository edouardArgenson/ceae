"""Added wind_energy_generation_prediction table

Revision ID: 62f8a65a16a2
Revises: 7bdb334ac6f7
Create Date: 2022-07-16 21:32:58.497547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62f8a65a16a2'
down_revision = '7bdb334ac6f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wind_energy_generation_prediction',
    sa.Column('country', sa.VARCHAR(length=32), nullable=False),
    sa.Column('datetime', sa.TIMESTAMP(), nullable=False),
    sa.Column('timezone', sa.INTEGER(), nullable=False),
    sa.Column('prediction', sa.FLOAT(), nullable=False),
    sa.Column('unit', sa.VARCHAR(length=32), nullable=False),
    sa.PrimaryKeyConstraint('country', 'datetime', name=op.f('pk_predicted_wind_energy_generation'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wind_energy_generation_prediction')
    # ### end Alembic commands ###