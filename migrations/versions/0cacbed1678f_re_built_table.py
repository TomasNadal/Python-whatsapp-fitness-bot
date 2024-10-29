"""Re-built table

Revision ID: 0cacbed1678f
Revises: 
Create Date: 2024-10-26 20:44:48.212801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cacbed1678f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('date_of_birth', sa.DateTime(timezone=True), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('initial_weight', sa.Float(), nullable=True),
    sa.Column('phone_number', sa.String(length=30), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('surname', sa.String(length=50), nullable=True),
    sa.Column('alias', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_updated_at'), ['updated_at'], unique=False)

    op.create_table('training_sessions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('training_sessions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_training_sessions_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_training_sessions_updated_at'), ['updated_at'], unique=False)

    op.create_table('user_stats',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('ecuacion', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name='fk_user_stats_exercise'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_stats_user'),
    sa.PrimaryKeyConstraint('user_id', 'exercise_id')
    )
    op.create_table('training_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('serie', sa.Integer(), nullable=False),
    sa.Column('rep', sa.Integer(), nullable=False),
    sa.Column('kg', sa.Float(), nullable=False),
    sa.Column('d', sa.Float(), nullable=True),
    sa.Column('vm', sa.Float(), nullable=True),
    sa.Column('vmp', sa.Float(), nullable=True),
    sa.Column('rm', sa.Integer(), nullable=True),
    sa.Column('p_w', sa.Float(), nullable=True),
    sa.Column('ejercicio_id', sa.Integer(), nullable=False),
    sa.Column('atleta_id', sa.Integer(), nullable=False),
    sa.Column('hash_id', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['atleta_id'], ['users.id'], name='fk_training_details_user'),
    sa.ForeignKeyConstraint(['ejercicio_id'], ['exercises.id'], name='fk_training_details_exercise'),
    sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('training_details', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_training_details_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_training_details_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_training_details_updated_at'), ['updated_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('training_details', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_training_details_updated_at'))
        batch_op.drop_index(batch_op.f('ix_training_details_timestamp'))
        batch_op.drop_index(batch_op.f('ix_training_details_created_at'))

    op.drop_table('training_details')
    op.drop_table('user_stats')
    with op.batch_alter_table('training_sessions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_training_sessions_updated_at'))
        batch_op.drop_index(batch_op.f('ix_training_sessions_created_at'))

    op.drop_table('training_sessions')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_updated_at'))
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_index(batch_op.f('ix_users_created_at'))

    op.drop_table('users')
    op.drop_table('exercises')
    # ### end Alembic commands ###
