from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "full_name" VARCHAR(50),
    "hashed_password" VARCHAR(128),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "note" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(225) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ship" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(225) NOT NULL,
    "description" VARCHAR(225) NOT NULL,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "frame" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "frame_pos" DECIMAL(9,3) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "ship_id" INT NOT NULL REFERENCES "ship" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_frame_frame_p_c5f422" UNIQUE ("frame_pos", "ship_id")
);
CREATE INDEX IF NOT EXISTS "idx_frame_frame_p_2c4b84" ON "frame" ("frame_pos");
CREATE TABLE IF NOT EXISTS "framecsvalues" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "center" point NOT NULL,
    "area" DECIMAL(40,15) NOT NULL,
    "aqy" DECIMAL(40,15) NOT NULL,
    "aqz" DECIMAL(40,15) NOT NULL,
    "ay" DECIMAL(40,15) NOT NULL,
    "az" DECIMAL(40,15) NOT NULL,
    "ayy" DECIMAL(40,15) NOT NULL,
    "azz" DECIMAL(40,15) NOT NULL,
    "ayz" DECIMAL(40,15) NOT NULL,
    "ayys" DECIMAL(40,15) NOT NULL,
    "azzs" DECIMAL(40,15) NOT NULL,
    "ayzs" DECIMAL(40,15) NOT NULL,
    "phi" DECIMAL(40,15) NOT NULL,
    "i1" DECIMAL(40,15) NOT NULL,
    "i2" DECIMAL(40,15) NOT NULL,
    "ir1" DECIMAL(40,15) NOT NULL,
    "ir2" DECIMAL(40,15) NOT NULL,
    "shear_center" point NOT NULL,
    "it" DECIMAL(40,15) NOT NULL,
    "awwm" DECIMAL(40,15) NOT NULL,
    "frame_id" INT NOT NULL  PRIMARY KEY REFERENCES "frame" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "framepoint" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "y" DECIMAL(9,3) NOT NULL,
    "z" DECIMAL(9,3) NOT NULL,
    "frame_id" INT NOT NULL REFERENCES "frame" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "framesegment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "thick" DECIMAL(9,3) NOT NULL,
    "end_point_id" INT NOT NULL REFERENCES "framepoint" ("id") ON DELETE CASCADE,
    "frame_id" INT NOT NULL REFERENCES "frame" ("id") ON DELETE CASCADE,
    "start_point_id" INT NOT NULL REFERENCES "framepoint" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
