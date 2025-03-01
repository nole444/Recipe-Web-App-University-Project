"""Add role to User model

Revision ID: 0a27ee5acd64
Revises: 402a79d29c2e
Create Date: 2024-06-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0a27ee5acd64'
down_revision = '402a79d29c2e'
branch_labels = None
depends_on = None

def upgrade():
    # Check if the role_id column already exists
    connection = op.get_bind()
    if not column_exists(connection, 'user', 'role_id'):
        # Add the role_id column
        op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))

    # Get the connection and metadata
    metadata = sa.MetaData()
    metadata.reflect(bind=connection)

    # Reference to the user and role tables
    user_table = metadata.tables['user']
    role_table = metadata.tables['role']

    # Insert default role if not exists
    existing_roles = connection.execute(sa.select(role_table.c.id).where(role_table.c.id == 1)).fetchall()
    if not existing_roles:
        connection.execute(role_table.insert().values(id=1, name='user', permissions=''))

    # Update existing users to have the default role
    connection.execute(
        user_table.update().values(role_id=1)
    )

    # Set the role_id column to not nullable
    op.alter_column('user', 'role_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])

def downgrade():
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')

def column_exists(connection, table_name, column_name):
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns
