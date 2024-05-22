import sqlalchemy as sa
from . import db
from .dialects import func

users = sa.Table(
    "users",
    db.metadata,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("username", sa.String, unique=True),
    sa.Column("email", sa.String, unique=True),
    sa.Column("provider", sa.String),
    sa.Column("metadata", sa.JSON),
    sa.Column("created_at", sa.DateTime),
)

chats = sa.Table(
    "chats",
    db.metadata,
    sa.Column(
        "id", sa.UUID, primary_key=True, server_default=func.uuid(), nullable=False
    ),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("title", sa.String),
    func.json_array_column(
        "tags",
    ),
    sa.Column("model", sa.String),
    func.json_array_column(
        "history",
    ),
    sa.Column("created_at", sa.DateTime),
)
