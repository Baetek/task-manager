"""init

Revision ID: 5bcca2256ac5
Revises: 
Create Date: 2024-08-06 13:55:09.063917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bcca2256ac5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'DOING', 'BLOCKED', 'DONE', name='taskstatus'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_history_description'), 'task_history', ['description'], unique=False)
    op.create_index(op.f('ix_task_history_id'), 'task_history', ['id'], unique=False)
    op.create_index(op.f('ix_task_history_title'), 'task_history', ['title'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'DOING', 'BLOCKED', 'DONE', name='taskstatus'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_description'), 'tasks', ['description'], unique=False)
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_description'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_task_history_title'), table_name='task_history')
    op.drop_index(op.f('ix_task_history_id'), table_name='task_history')
    op.drop_index(op.f('ix_task_history_description'), table_name='task_history')
    op.drop_table('task_history')
    # ### end Alembic commands ###
