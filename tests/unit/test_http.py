import requests
from mock import patch, Mock, call
from pyapp.conf import settings
from pytest import fixture, raises

from transfer_market_scraper.exceptions import LoginError
from transfer_market_scraper.http import BaseHttpSession, GameHttpSession


##############
#  Fixtures  #
##############
@fixture
def base_session():
    base_session = Mock()
    return base_session


@fixture
def game_session():
    game_session = Mock()
    return game_session


@fixture
def base_http(base_session):
    with patch("requests.Session", Mock(return_value=base_session)):
        base_http = BaseHttpSession()
        return base_http


@fixture
def game_http(game_session):
    with patch("requests.Session", Mock(return_value=game_session)):
        with settings.modify() as settings_patch:
            settings_patch.URL_BASE = "aHR0cHM6Ly93d3cubXlfd2Vic2l0ZS5jb20uYXU="
            game_http = GameHttpSession()
            return game_http


###########################
#  BaseHttpSession Tests  #
###########################
def test_when_base_http_session_then_object_configured():
    base_http = BaseHttpSession()

    assert isinstance(base_http.session, requests.Session)
    assert base_http.headers == {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.107 Safari/537.36"
    }


@patch("random.random")
@patch("random.randint")
@patch("time.sleep")
def test_when_base_http_get_and_min_args_given_then_calls_made_correctly(sleep, randint, rand, base_http, base_session):
    get_resp = Mock()
    randint.return_value = 12
    rand.return_value = 0.3456

    base_session.get = Mock(return_value=get_resp)
    actual = base_http.get("https://www.my_website.com.au/listings")

    base_session.assert_has_calls([
        call.get("https://www.my_website.com.au/listings", headers=base_http.headers)
    ])

    randint.assert_called_once_with(10, 45)
    rand.assert_called_once()
    sleep.assert_called_once_with(12.3456)

    assert actual == get_resp


@patch("random.random")
@patch("random.randint")
@patch("time.sleep")
def test_when_base_http_get_and_all_args_given_then_calls_made_correctly(sleep, randint, rand, base_http, base_session):
    get_resp = Mock()
    randint.return_value = 93
    rand.return_value = 0.7291423

    base_session.get = Mock(return_value=get_resp)
    actual = base_http.get(
        "https://www.my_website.com.au/listings",
        headers={"Content": "DERP"},
        delay_min=50,
        delay_max=100
    )

    base_session.assert_has_calls([
        call.get("https://www.my_website.com.au/listings", headers={"Content": "DERP"})
    ])

    randint.assert_called_once_with(50, 100)
    rand.assert_called_once()
    sleep.assert_called_once_with(93.7291423)

    assert actual == get_resp


@patch("time.sleep")
def test_when_base_http_get_and_delays_zero_then_no_delays(sleep, base_http):
    base_http.get("https://www.my_website.com.au/listings", delay_min=0, delay_max=0)
    sleep.assert_called_once_with(0)


@patch("random.random")
@patch("random.randint")
@patch("time.sleep")
def test_when_base_http_post_and_min_args_given_then_calls_made_correctly(sleep, randint, rand, base_http, base_session):
    post_resp = Mock()
    randint.return_value = 12
    rand.return_value = 0.3456

    base_session.post = Mock(return_value=post_resp)
    actual = base_http.post("https://www.my_website.com.au/login")

    base_session.assert_has_calls([
        call.post("https://www.my_website.com.au/login", headers=base_http.headers, data=None)
    ])

    randint.assert_called_once_with(10, 45)
    rand.assert_called_once()
    sleep.assert_called_once_with(12.3456)

    assert actual == post_resp


@patch("random.random")
@patch("random.randint")
@patch("time.sleep")
def test_when_base_http_post_and_all_args_given_then_calls_made_correctly(sleep, randint, rand, base_http, base_session):
    post_resp = Mock()
    randint.return_value = 93
    rand.return_value = 0.7291423

    base_session.post = Mock(return_value=post_resp)
    actual = base_http.post(
        "https://www.my_website.com.au/login",
        headers={"Content": "DERP"},
        payload={"user": "bill-nye", "password": "sc13nc3Guy"},
        delay_min=50,
        delay_max=100
    )

    base_session.assert_has_calls([
        call.post(
            "https://www.my_website.com.au/login",
            headers={"Content": "DERP"},
            data={"user": "bill-nye", "password": "sc13nc3Guy"}
        )
    ])

    randint.assert_called_once_with(50, 100)
    rand.assert_called_once()
    sleep.assert_called_once_with(93.7291423)

    assert actual == post_resp


@patch("time.sleep")
def test_when_base_http_post_and_delays_zero_then_no_delays(sleep, base_http):
    base_http.post("https://www.my_website.com.au/listings", delay_min=0, delay_max=0)
    sleep.assert_called_once_with(0)


###########################
#  GameHttpSession Tests  #
###########################
def test_when_game_http_then_configured_correctly():
    with settings.modify() as settings_patch:
        settings_patch.URL_BASE = "aHR0cHM6Ly93d3cubXlfd2Vic2l0ZS5jb20uYXU="
        game_http = GameHttpSession()

    assert isinstance(game_http.session, requests.Session)
    assert game_http.url_base == "https://www.my_website.com.au"
    assert game_http.headers == {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.107 Safari/537.36"
    }
    assert game_http.headers_login == {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded"
    }


def test_when_game_http_login_then_correct_calls_made(game_http, game_session):
    post_resp = Mock(
        url="https://www.my_website.com.au/nl/news.asp",
        status=200
    )

    with patch.object(game_http, "post") as post_mock:
        post_mock.return_value = post_resp
        actual = game_http.login("my_username", "hunter1234")

        post_mock.assert_called_once_with(
            "https://www.my_website.com.au/nl/login.asp",
            headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/92.0.4515.107 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                          "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "max-age=0",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            payload={"username": "my_username", "password": "hunter1234"}
        )

    assert actual == post_resp


def test_when_game_http_login_and_incorrect_creds_then_raise_error(game_http, game_session):
    post_resp = Mock(
        url="https://www.my_website.com.au/nl/login.asp",
        status=200
    )

    with raises(LoginError, match="Login has failed for the game website"):
        with patch.object(game_http, "post") as post_mock:
            post_mock.return_value = post_resp
            game_http.login("my_username", "hunter1234")
