from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers
revision: str = 'f6867092327c'
down_revision: str | Sequence[str] | None = 'daa765486560'


def upgrade() -> None:
    # 1. CREATE THE ENUM TYPE MANUALLY
    # We use postgresql.ENUM to define it and then .create()
    status_enum = sa.Enum('ACTIVE', 'INACTIVE', name='employeestatus')
    status_enum.create(op.get_bind(), checkfirst=True)

    # 2. NOW ALTER THE COLUMN
    # We add 'using' clause to help Postgres convert string to enum
    op.execute(
        'ALTER TABLE employee ALTER COLUMN status TYPE employeestatus USING status::employeestatus'
    )

    # 3. ADD YOUR COLUMNS (Updated with server_default for safety)
    op.add_column(
        'employees_personal_info',
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.add_column(
        'employees_personal_info',
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.add_column('employees_personal_info', sa.Column('deleted_at', sa.DateTime(), nullable=True))

    # 4. TRIGGER LOGIC
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    for table_name in ['employee', 'employees_personal_info', 'employee_financial_info']:
        op.execute(f"""
            CREATE TRIGGER set_updated_at_{table_name}
            BEFORE UPDATE ON {table_name}
            FOR EACH ROW
            EXECUTE PROCEDURE update_updated_at_column();
        """)


def downgrade() -> None:
    # Remove triggers and function
    for table_name in ['employee', 'employees_personal_info', 'employee_financial_info']:
        op.execute(f'DROP TRIGGER IF EXISTS set_updated_at_{table_name} ON {table_name}')
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column')

    # Revert column to VARCHAR
    op.alter_column(
        'employee',
        'status',
        existing_type=sa.Enum('ACTIVE', 'INACTIVE', name='employeestatus'),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # DROP THE TYPE
    sa.Enum(name='employeestatus').drop(op.get_bind(), checkfirst=True)

    op.drop_column('employees_personal_info', 'deleted_at')
    op.drop_column('employees_personal_info', 'updated_at')
    op.drop_column('employees_personal_info', 'created_at')
