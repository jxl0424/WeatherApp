"""create weather_searches table

Revision ID: 0001
Revises:
Create Date: 2026-06-24
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import TIMESTAMP

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "weather_searches",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("location_query", sa.String(255), nullable=False),
        sa.Column("resolved_location_name", sa.String(255), nullable=False),
        sa.Column("latitude", sa.Numeric(8, 5), nullable=False),
        sa.Column("longitude", sa.Numeric(8, 5), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("weather_condition", sa.String(64), nullable=False),
        sa.Column("temperature", sa.Numeric(5, 2), nullable=False),
        sa.Column("humidity", sa.SmallInteger(), nullable=True),
        sa.Column("wind_speed", sa.Numeric(5, 2), nullable=True),
        sa.Column(
            "created_at",
            TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("end_date >= start_date", name="ck_weather_searches_date_range"),
        sa.CheckConstraint("humidity >= 0 AND humidity <= 100", name="ck_weather_searches_humidity"),
    )
    op.create_index("ix_weather_searches_created_at", "weather_searches", ["created_at"])
    op.create_index(
        "ix_weather_searches_resolved_location_name",
        "weather_searches",
        ["resolved_location_name"],
    )


def downgrade() -> None:
    op.drop_index("ix_weather_searches_resolved_location_name")
    op.drop_index("ix_weather_searches_created_at")
    op.drop_table("weather_searches")
