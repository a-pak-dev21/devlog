from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Numeric, UniqueConstraint, Index


metadata = MetaData()

pairs_table = Table("pairs",
                    metadata,
                    Column("id", Integer, primary_key=True),
                    Column("base", String(10), nullable=False),
                    Column("quote", String(10), nullable=False),
                    UniqueConstraint("base", "quote", name="uq_pairs"),
                    )

exchanges_table = Table("exchanges",
                       metadata,
                       Column("id", Integer, primary_key=True),
                       Column("name", String(30), nullable=False, unique=True)
                       )


snapshots_table = Table("snapshots",
                       metadata,
                       Column("id", Integer, primary_key=True),
                       Column("snapshot_time", DateTime(timezone=True), nullable=False),
                       Index("idx_snapshot_time", "snapshot_time"),
                       UniqueConstraint("snapshot_time", name="uq_snapshot")
                       )

prices_table = Table("prices",
                    metadata,
                    Column("id", Integer, primary_key=True),
                    Column("snapshot_id", ForeignKey("snapshots.id", ondelete="CASCADE"), nullable=False),
                    Column("pair_id", ForeignKey("pairs.id"), nullable=False),
                    Column("exchange_id", ForeignKey("exchanges.id"), nullable=False),
                    Column("price", Numeric(18,8), nullable=False),
                    UniqueConstraint("snapshot_id", "pair_id", "exchange_id", name="uq_price_combination")
                    )

Index("idx_snapshot_pair", prices_table.c.snapshot_id, prices_table.c.pair_id)

errors_table = Table("errors",
                    metadata,
                    Column("id", Integer, primary_key=True),
                    Column("snapshot_id", ForeignKey("snapshots.id"), nullable=True),
                    Column("pair_id", ForeignKey("pairs.id"), nullable=True),
                    Column("exchange_id", ForeignKey("exchanges.id"), nullable=True),
                    Column("error_type", String(20), nullable=False),
                    Column("message", String, nullable=False),
                    Column("source", String(30), nullable=False),
                    Column("error_time", DateTime(timezone=True), nullable=False)
                    )