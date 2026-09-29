from streamlit.testing.v1 import AppTest
import bfup_ex4 as core


def test_course_values():
    r = core.ex4_compute()
    s = r["st"]
    assert abs(r["mRD1"] - 68) < 0.1 and r["ok1"]
    assert abs(s["sUD"] - 5.0) < 0.06 and abs(s["eD"] * 1e3 - 0.33) < 0.005
    assert abs(r["x"] - 77) < 1
    assert abs(s["m"] - 53.5) < 0.6
    assert abs(r["s_sU"] - 60) < 1.5 and abs(r["s_sc"] - 44) < 1
    assert abs(abs(s["rows"][3][3]) - 5.52) < 0.1
    assert r["ok_mat"]
    # itérations du corrigé : x = 80 → ΣF < 0 ; x = 75 → ΣF > 0
    assert r["iters"][0]["sumF"] < 0 < r["iters"][1]["sumF"]


def test_app_runs():
    at = AppTest.from_file("app.py", default_timeout=90).run()
    assert not at.exception
    for opt in at.selectbox[0].options:
        at.selectbox[0].set_value(opt).run()
        assert not at.exception, opt
    at.radio[0].set_value(core.LEVELS[1]).run()
    assert not at.exception
