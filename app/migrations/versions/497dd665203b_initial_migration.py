"""Initial migration

Revision ID: 497dd665203b
Revises:
Create Date: 2024-11-16 04:22:12.988704

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "497dd665203b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the "assets" table
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("file_url", sa.String, nullable=False),
        sa.Column("category", sa.String, nullable=False, index=True),
    )


def downgrade() -> None:
    # Drop the "assets" table
    op.drop_table("assets")
