"""add int id PK to secom_users and user_information per ENTITY_RULE

Revision ID: 20260521_entity_id
Revises: 20260520_user_info
Create Date: 2026-05-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "20260521_entity_id"
down_revision: Union[str, Sequence[str], None] = "20260520_user_info"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names(table: str) -> set[str]:
    bind = op.get_bind()
    return {c["name"] for c in inspect(bind).get_columns(table)}


def _pk_columns(table: str) -> list[str]:
    bind = op.get_bind()
    pk = inspect(bind).get_pk_constraint(table)
    return list(pk.get("constrained_columns") or [])


def _upgrade_secom_users() -> None:
    cols = _column_names("secom_users")
    if "id" not in cols:
        op.add_column("secom_users", sa.Column("id", sa.Integer(), nullable=True))

    op.execute(
        """
        UPDATE secom_users
        SET id = sub.rn
        FROM (
            SELECT user_id, ROW_NUMBER() OVER (ORDER BY user_id) AS rn
            FROM secom_users
            WHERE id IS NULL
        ) AS sub
        WHERE secom_users.user_id = sub.user_id
        """
    )

    op.execute(
        """
        UPDATE secom_users
        SET id = sub.rn
        FROM (
            SELECT user_id, ROW_NUMBER() OVER (ORDER BY user_id) AS rn
            FROM secom_users
        ) AS sub
        WHERE secom_users.id IS NULL AND secom_users.user_id = sub.user_id
        """
    )

    op.alter_column("secom_users", "id", nullable=False)

    if _pk_columns("secom_users") != ["id"]:
        op.drop_constraint("secom_users_pkey", "secom_users", type_="primary")
        op.create_primary_key("secom_users_pkey", "secom_users", ["id"])

    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ix_secom_users_user_id
        ON secom_users (user_id)
        """
    )

    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS secom_users_id_seq OWNED BY secom_users.id;
        SELECT setval(
            'secom_users_id_seq',
            COALESCE((SELECT MAX(id) FROM secom_users), 1)
        );
        ALTER TABLE secom_users
        ALTER COLUMN id SET DEFAULT nextval('secom_users_id_seq');
        """
    )


def _upgrade_user_information() -> None:
    cols = _column_names("user_information")
    pk = _pk_columns("user_information")

    if pk == ["id"]:
        op.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS ix_user_information_user_id
            ON user_information (user_id)
            """
        )
        op.execute(
            """
            CREATE SEQUENCE IF NOT EXISTS user_information_id_seq OWNED BY user_information.id;
            SELECT setval(
                'user_information_id_seq',
                COALESCE((SELECT MAX(id) FROM user_information), 1)
            );
            ALTER TABLE user_information
            ALTER COLUMN id SET DEFAULT nextval('user_information_id_seq');
            """
        )
        return

    if "id" not in cols:
        op.add_column("user_information", sa.Column("id", sa.Integer(), nullable=True))

    if "member_id" not in cols:
        op.add_column("user_information", sa.Column("member_id", sa.Integer(), nullable=True))

    # user_id is still varchar (login) until we rename member_id
    user_id_type = next(
        c["type"]
        for c in inspect(op.get_bind()).get_columns("user_information")
        if c["name"] == "user_id"
    )
    login_fk = isinstance(user_id_type, sa.String) or getattr(user_id_type, "length", None)

    if login_fk:
        op.execute(
            """
            WITH numbered AS (
                SELECT user_id, ROW_NUMBER() OVER (ORDER BY user_id) AS rn
                FROM user_information
            )
            UPDATE user_information ui
            SET id = n.rn
            FROM numbered n
            WHERE ui.user_id = n.user_id AND ui.id IS NULL
            """
        )

        op.execute(
            """
            UPDATE user_information ui
            SET member_id = su.id
            FROM secom_users su
            WHERE ui.user_id = su.user_id
            """
        )

        op.alter_column("user_information", "id", nullable=False)
        op.alter_column("user_information", "member_id", nullable=False)

        op.drop_constraint("user_information_pkey", "user_information", type_="primary")
        op.drop_constraint(
            "user_information_user_id_fkey", "user_information", type_="foreignkey"
        )
        op.drop_column("user_information", "user_id")
        op.alter_column("user_information", "member_id", new_column_name="user_id")

        op.create_primary_key("user_information_pkey", "user_information", ["id"])
        op.create_foreign_key(
            "user_information_user_id_fkey",
            "user_information",
            "secom_users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )

    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ix_user_information_user_id
        ON user_information (user_id)
        """
    )

    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS user_information_id_seq OWNED BY user_information.id;
        SELECT setval(
            'user_information_id_seq',
            COALESCE((SELECT MAX(id) FROM user_information), 1)
        );
        ALTER TABLE user_information
        ALTER COLUMN id SET DEFAULT nextval('user_information_id_seq');
        """
    )


def upgrade() -> None:
    _upgrade_secom_users()
    _upgrade_user_information()


def downgrade() -> None:
    op.add_column(
        "user_information",
        sa.Column("login_user_id", sa.String(length=64), nullable=True),
    )

    op.execute(
        """
        UPDATE user_information ui
        SET login_user_id = su.user_id
        FROM secom_users su
        WHERE ui.user_id = su.id
        """
    )

    op.alter_column("user_information", "login_user_id", nullable=False)

    op.drop_constraint("user_information_user_id_fkey", "user_information", type_="foreignkey")
    op.drop_constraint("user_information_pkey", "user_information", type_="primary")
    op.drop_index("ix_user_information_user_id", table_name="user_information")
    op.drop_column("user_information", "user_id")
    op.drop_column("user_information", "id")

    op.alter_column("user_information", "login_user_id", new_column_name="user_id")

    op.create_foreign_key(
        "user_information_user_id_fkey",
        "user_information",
        "secom_users",
        ["user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )
    op.create_primary_key("user_information_pkey", "user_information", ["user_id"])

    op.execute("DROP SEQUENCE IF EXISTS user_information_id_seq")

    op.drop_index("ix_secom_users_user_id", table_name="secom_users")
    op.drop_constraint("secom_users_pkey", "secom_users", type_="primary")
    op.drop_column("secom_users", "id")
    op.create_primary_key("secom_users_pkey", "secom_users", ["user_id"])

    op.execute("DROP SEQUENCE IF EXISTS secom_users_id_seq")
