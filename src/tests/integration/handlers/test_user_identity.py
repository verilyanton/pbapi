import logging
import os
import uuid
from datetime import datetime

from src.handlers.user_identity import UserIdentityHandler
from src.schemas.common import TableName
from src.schemas.user_identity import UserIdentity, IdentityProvider

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")


def test_handler():
    try:
        # Mocking environment for local dev if not set
        os.environ.setdefault("ENV_NAME", "test")
        os.environ.setdefault("POSTGRES_HOST", "localhost")
        os.environ.setdefault("POSTGRES_PORT", "5433")
        os.environ.setdefault("POSTGRES_DB", "pbapi_test")
        os.environ.setdefault("POSTGRES_USER", "postgres")
        os.environ.setdefault("POSTGRES_PASSWORD", "postgres")

        handler = UserIdentityHandler(logger)

        # Create a user first because of foreign key constraint
        user_uuid = uuid.uuid4()
        user_data = {
            "id": str(user_uuid),
            "email": f"test-{user_uuid}@example.com",
            "name": "Test User",
            "creation_time": int(datetime.now().timestamp()),
            "login_generation": 1,
            "banned": False,
        }
        handler.db.use_table(TableName.USER)
        handler.db.create_one(user_data)

        handler.db.use_table(TableName.USER_IDENTITY)
        identity_id = f"test-id-{uuid.uuid4()}"
        user_id = user_uuid

        print(f"Testing with identity_id: {identity_id}")

        # 1. Create
        identity = UserIdentity(
            id=identity_id, provider=IdentityProvider.GOOGLE, user_id=user_id
        )

        print("Creating identity...")
        created_id = handler.create(identity)
        print(f"Created ID: {created_id}")

        # 2. Find
        print("Finding identity...")
        found = handler.find(identity_id, IdentityProvider.GOOGLE)

        if found:
            print(f"Found identity: {found}")
            assert found.id == identity_id
            assert found.user_id == user_id
            print("SUCCESS: Identity found and matches!")
        else:
            print("FAILED: Identity not found!")
            return

        # 3. Update
        print("Updating identity...")
        # Note: We need another valid user if we want to change user_id,
        # but here we just test if update works at all.
        found.provider = IdentityProvider.GOOGLE  # same value
        updated = handler.update(found)
        print(f"Update result: {updated}")

        # 4. Verify Update
        print("Verifying update...")
        verified = handler.find(identity_id, IdentityProvider.GOOGLE)
        if verified and verified.user_id == user_id:
            print("SUCCESS: Identity update verified!")
        else:
            print(f"FAILED: Identity update verification failed!")

        # 5. Get or Create User (Existing)
        print("Testing get_or_create_user_by_identity (existing)...")
        user = handler.get_or_create_user_by_identity(
            identity_id, IdentityProvider.GOOGLE, "test@example.com", "Test User"
        )
        assert user.id == user_id
        assert user.email == f"test-{user_uuid}@example.com"
        print("SUCCESS: get_or_create_user_by_identity (existing) verified!")

        # 6. Get or Create User (New)
        print("Testing get_or_create_user_by_identity (new)...")
        new_identity_id = f"new-id-{uuid.uuid4()}"
        new_email = f"new-{uuid.uuid4()}@example.com"
        new_user = handler.get_or_create_user_by_identity(
            new_identity_id, IdentityProvider.GOOGLE, new_email, "New User"
        )
        assert new_user.email == new_email
        assert new_user.name == "New User"

        # Verify it was actually created in DB
        found_identity = handler.find(new_identity_id, IdentityProvider.GOOGLE)
        assert found_identity is not None
        print(f"New user ID: {new_user.id}, Identity user ID: {found_identity.user_id}")
        assert str(found_identity.user_id) == str(new_user.id)
        print("SUCCESS: get_or_create_user_by_identity (new) verified!")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_handler()
