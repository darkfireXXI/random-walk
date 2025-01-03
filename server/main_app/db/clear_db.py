import argparse
import time

from db.models import main, relationship  # noqa: F401
from db.models.base import Base
from db.utils import rw_sync_session


def clear_db():
    with rw_sync_session() as session, session.begin():
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())


if __name__ in "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Clear DB")
    parser.add_argument(
        "-y",
        "--yes",
        default=False,
        action="store_true",
        help="ensure you actually want to clear the db",
    )
    parser.add_argument(
        "-f",
        "--fast",
        default=False,
        action="store_true",
        help="skip the sleep when clearing db [you're psychotic]",
    )

    args = parser.parse_args()

    yes_clear_db = args.yes
    yes_im_fast_and_psychotic = args.fast

    if yes_clear_db:
        if not yes_im_fast_and_psychotic:
            print("DB will be cleared in 5 seconds...")
            time.sleep(5)
        clear_db()
        print("DB has been cleared")
    else:
        print("DB not cleared")
