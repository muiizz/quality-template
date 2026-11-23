import pytest

from qtemplate.__main__ import main


def test_demo_prints(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    out = capsys.readouterr().out
    assert "hello world" in out
    assert "total spend: 0.15" in out
