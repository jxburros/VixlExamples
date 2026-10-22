"""Build every scene document into ../scenes/ (about 5 minutes; needs network for Google Fonts, and the
assets from prepare_assets.py for the "real stuff" scenes). Run: python promo/vixl-is-fun/build/build_scenes.py"""
import json, sys
from lib import *
import s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, p2a, p2b, p2c

def build_all():
    out = {}
    out["s01"] = save(s01.build(), "s01"); out["s02"] = save(s02.build(), "s02"); out["s03"] = save(s03.build(), "s03")
    out["s04i"] = save(s04.intro(), "s04i")
    for name, make in s04.STYLES: out[name] = save(make(), name)
    out["s05"] = save(s05.build(), "s05")
    p = s06.build(); s06.motion(p); out["s06"] = save(p, "s06")
    out["s07"] = save(s07.build(), "s07"); out["s08"] = save(s08.build(), "s08")
    out["s09"] = save(s09.build(), "s09"); out["s10"] = save(s10.build(), "s10")
    for name, make in (("x0", p2a.x0), ("x1", p2a.x1), ("x2", p2b.x2), ("x3", p2b.x3),
                       ("x4", p2c.x4), ("x5", p2c.x5), ("x6", p2c.x6), ("x8", p2c.x8)):
        out[name] = save(make(), name)
    return out

if __name__ == "__main__":
    print(json.dumps(build_all(), indent=1))
