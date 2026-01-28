import os

dir_path = os.path.dirname(os.path.realpath(__file__))
TEST_SQLITE_DB_PATH = os.path.join(dir_path, "..", "..", "..", "db", "test.sqlite3")
