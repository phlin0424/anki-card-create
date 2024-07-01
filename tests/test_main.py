import pytest
import sys
from argparse import Namespace
from main import get_args_parser
from config import settings


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(
            ["--file", "test.txt"],
            Namespace(
                file="test.txt",
                word=None,
                deck_name=settings.deck_name,
                model_name=settings.model_name,
            ),
        ),
        pytest.param(
            ["--word", "안녕하세요"],
            Namespace(
                file=None,
                word="안녕하세요",
                deck_name=settings.deck_name,
                model_name=settings.model_name,
            ),
        ),
        pytest.param(
            ["--file", "test.txt", "--deck_name", "test"],
            Namespace(
                file="test.txt",
                word=None,
                deck_name="test",
                model_name=settings.model_name,
            ),
        ),
        pytest.param(
            ["--file", "test.txt", "--model_name", "TestModel"],
            Namespace(
                file="test.txt",
                word=None,
                deck_name=settings.deck_name,
                model_name="TestModel",
            ),
        ),
    ],
)
def test_get_args_parser(args, expected, monkeypatch):
    # Simulate command-line arguments
    monkeypatch.setattr(sys, "argv", ["prog"] + args)

    assert get_args_parser() == expected
