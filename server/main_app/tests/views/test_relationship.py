from dataclasses import asdict
from uuid import uuid4

from utils.utils import custom_dict_factory, naive_utcnow
from views.relationship import CategorySiteRelationshipView, UserCategoryRelationshipView, UserSiteRelationshipView


def test_category_site_relationship_view():
    category_site_relationship_view = CategorySiteRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="tag",
        status=None,
        submitted_by=None,
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    category_site_relationship_json = asdict(category_site_relationship_view, dict_factory=custom_dict_factory)

    assert str(category_site_relationship_view.uuid) == category_site_relationship_json["uuid"]
    assert str(category_site_relationship_view.from_uuid) == category_site_relationship_json["from_uuid"]
    assert str(category_site_relationship_view.to_uuid) == category_site_relationship_json["to_uuid"]
    assert category_site_relationship_view.relationship == category_site_relationship_json["relationship"]
    assert category_site_relationship_view.status == category_site_relationship_json["status"]
    assert category_site_relationship_view.submitted_by == category_site_relationship_json["submitted_by"]
    assert str(category_site_relationship_view.created_at) == category_site_relationship_json["created_at"]
    assert str(category_site_relationship_view.updated_at) == category_site_relationship_json["updated_at"]


def test_user_category_relationship():
    user_category_relationship_view = UserCategoryRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    user_category_relationship_json = asdict(user_category_relationship_view, dict_factory=custom_dict_factory)

    assert str(user_category_relationship_view.uuid) == user_category_relationship_json["uuid"]
    assert str(user_category_relationship_view.from_uuid) == user_category_relationship_json["from_uuid"]
    assert str(user_category_relationship_view.to_uuid) == user_category_relationship_json["to_uuid"]
    assert user_category_relationship_view.relationship == user_category_relationship_json["relationship"]
    assert str(user_category_relationship_view.created_at) == user_category_relationship_json["created_at"]
    assert str(user_category_relationship_view.updated_at) == user_category_relationship_json["updated_at"]


def test_user_site_relationship():
    user_site_relationship_view = UserSiteRelationshipView(
        uuid=uuid4(),
        from_uuid=uuid4(),
        to_uuid=uuid4(),
        relationship="like",
        created_at=naive_utcnow(),
        updated_at=naive_utcnow(),
    )

    user_site_relationship_json = asdict(user_site_relationship_view, dict_factory=custom_dict_factory)

    assert str(user_site_relationship_view.uuid) == user_site_relationship_json["uuid"]
    assert str(user_site_relationship_view.from_uuid) == user_site_relationship_json["from_uuid"]
    assert str(user_site_relationship_view.to_uuid) == user_site_relationship_json["to_uuid"]
    assert user_site_relationship_view.relationship == user_site_relationship_json["relationship"]
    assert str(user_site_relationship_view.created_at) == user_site_relationship_json["created_at"]
    assert str(user_site_relationship_view.updated_at) == user_site_relationship_json["updated_at"]
