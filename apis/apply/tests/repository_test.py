import pytest
from rest_framework.exceptions import ValidationError
from django.conf import settings

from apply.repositories import WantedRepo
from exceptions import NotFoundError

wanted_repo = WantedRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


valid_wanted_create_params = {
    "company": 1,
    "title": "test",
    "country": "korea",
    "location": "서울",
    "role": "백엔드",
    "reward": 100,
    "tech_stack_name": "asd",
    "contents": "adsasdasdasdasd",
}

invalid_wanted_params = (
    [
        {},
        {**valid_wanted_create_params, "company": -125},
        {**valid_wanted_create_params, "reward": "a"},
        {
            x: valid_wanted_create_params[x]
            for x in valid_wanted_create_params
            if x not in "company"
        },
    ],
)


@pytest.mark.django_db()
def test_create_wanted():
    sut = wanted_repo.create(valid_wanted_create_params)
    isinstance(sut, dict)


@pytest.mark.django_db()
@pytest.mark.parametrize("param", invalid_wanted_params)
def test_create_wanted_with_invalid_params(param):
    with pytest.raises(ValidationError):
        wanted_repo.create(param)


@pytest.mark.django_db()
def test_update_wanted():
    sut = wanted_repo.update(8, {**valid_wanted_create_params, "reward": 1000})
    isinstance(sut, dict)


@pytest.mark.django_db()
@pytest.mark.parametrize("param", invalid_wanted_params)
def test_update_wanted_with_invalid_params(param):
    with pytest.raises(ValidationError):
        wanted_repo.create(param)


@pytest.mark.django_db()
def test_delete_wanted():
    assert wanted_repo.delete(8)


@pytest.mark.django_db()
def test_delete_non_exist_wanted():
    with pytest.raises(NotFoundError):
        wanted_repo.delete(-1)


@pytest.mark.django_db()
def test_find_with_limit():
    sut = wanted_repo.find_with_limit()
    assert isinstance(sut, list)
    if len(sut):
        assert isinstance(sut[0], dict)


@pytest.mark.django_db()
def test_count_with_options():
    sut = wanted_repo.count_with_options()
    assert isinstance(sut, int)
    assert sut >= 0