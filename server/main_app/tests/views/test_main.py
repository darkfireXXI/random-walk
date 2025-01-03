from dataclasses import asdict
from uuid import uuid4

from utils.utils import custom_dict_factory, naive_utcnow
from views.main import CategoryGroupView, CategoryView, SiteView, UserView


def test_user_view():
    user_view = UserView(
        uuid=uuid4(),
        user_name="drip___drop",
        email="nah@hellyeah.com",
        password="passw0rd",
        photo=None,
        role="default",
        joined_at=naive_utcnow(),
        last_login=naive_utcnow(),
    )

    user_json = asdict(user_view, dict_factory=custom_dict_factory)

    assert str(user_view.uuid) == user_json["uuid"]
    assert user_view.user_name == user_json["user_name"]
    assert user_view.email == user_json["email"]
    assert user_view.password == user_json["password"]
    assert user_view.photo == user_json["photo"]
    assert user_view.role == user_json["role"]
    assert str(user_view.joined_at) == user_json["joined_at"]
    assert str(user_view.last_login) == user_json["last_login"]


def test_site_view():
    site_view = SiteView(
        uuid=uuid4(),
        url="www.coolest-site-ever.com",
        name=None,
        status=None,
        likes=0,
        dislikes=0,
        collections=0,
        score=0,
        thumbnail=None,
        submitted_by=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    site_json = asdict(site_view, dict_factory=custom_dict_factory)

    assert str(site_view.uuid) == site_json["uuid"]
    assert site_view.url == site_json["url"]
    assert site_view.name == site_json["name"]
    assert site_view.status == site_json["status"]
    assert site_view.likes == site_json["likes"]
    assert site_view.dislikes == site_json["dislikes"]
    assert site_view.collections == site_json["collections"]
    assert site_view.score == site_json["score"]
    assert site_view.thumbnail == site_json["thumbnail"]
    assert site_view.submitted_by == site_json["submitted_by"]
    assert str(site_view.created_at) == site_json["created_at"]
    assert str(site_view.updated_at) == site_json["updated_at"]


def test_category_group_view():
    category_group_view = CategoryGroupView(
        uuid=uuid4(),
        name="cool",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    category_group_json = asdict(category_group_view, dict_factory=custom_dict_factory)

    assert str(category_group_view.uuid) == category_group_json["uuid"]
    assert category_group_view.name == category_group_json["name"]
    assert str(category_group_view.created_at) == category_group_json["created_at"]
    assert str(category_group_view.updated_at) == category_group_json["updated_at"]


def test_category_view():
    category_view = CategoryView(
        uuid=uuid4(),
        name="cool stuff",
        parent_uuid=uuid4(),
        parent_name="cool",
        status=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    category_json = asdict(category_view, dict_factory=custom_dict_factory)

    assert str(category_view.uuid) == category_json["uuid"]
    assert category_view.name == category_json["name"]
    assert str(category_view.parent_uuid) == category_json["parent_uuid"]
    assert category_view.parent_name == category_json["parent_name"]
    assert category_view.status == category_json["status"]
    assert str(category_view.created_at) == category_json["created_at"]
    assert str(category_view.updated_at) == category_json["updated_at"]
