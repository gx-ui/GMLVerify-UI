from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(16) NOT NULL,
    "password" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "datasource" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(16) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_datasource_name_deedc6" UNIQUE ("name", "user_id")
);
CREATE TABLE IF NOT EXISTS "dataasset" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64),
    "datasource_id" INT NOT NULL REFERENCES "datasource" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_dataasset_name_01ceff" UNIQUE ("name", "datasource_id")
);
CREATE TABLE IF NOT EXISTS "expectationsuite" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type_id" INT NOT NULL,
    "suite_json" JSONB NOT NULL,
    "data_asset_id" INT NOT NULL REFERENCES "dataasset" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "validationresult" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "validation_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "success" BOOL NOT NULL,
    "result_json" JSONB NOT NULL,
    "data_asset_id" INT NOT NULL REFERENCES "dataasset" ("id") ON DELETE CASCADE,
    "expectation_suite_id" INT NOT NULL REFERENCES "expectationsuite" ("id") ON DELETE CASCADE
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
