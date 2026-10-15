import pytest

from ucrel_sections import Color, Section, Timer, UnitTest, fmt


def test_fmt_pads_to_width():
    out = fmt("hi", Color.BOLD, width=20)
    plain = out.removeprefix(Color.BOLD).removesuffix(Color.RESET)
    assert len(plain) == 20
    assert " hi " in plain


def test_section_records_results(capsys):
    with Section("demo", width=40) as s:
        s.tryAssert(True, name="ok")
        s.tryAssert(False, detail="nope", name="bad")
        s.report("info", "hello")
        with s.timer("t"):
            pass
        with s.test("soft", canFail=True) as t:
            t.reject(True, "expected failure")

    names = [r.name for r in s.tests]
    assert names == ["<Assertion> ok", "<Assertion> bad", "<Report> info", "<Timer> t", "<Test> soft"]
    assert [r.failed for r in s.tests] == [False, True, False, False, True]
    assert "Test Results:" in capsys.readouterr().out


def test_hard_unit_test_propagates():
    with pytest.raises(AssertionError):
        with UnitTest("hard") as t:
            t.reject(True, "boom")


def test_timer_sets_detail():
    with Timer("x") as t:
        pass
    assert not t.failed
    assert t.detail.startswith("Complete in")


def test_fmt_pads_without_style():
    out = fmt("hi", width=20)
    assert len(out) == 20
    assert out.startswith("=") and " hi " in out
