# SPDX-License-Identifier: MIT
"""Exact-export previews using the bundled canonical renderer.
--clay-all is a low-cost authoring diagnostic, never final material evidence.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,35.264389682754654)
if '--clay-all' in sys.argv:
    sys.argv.remove('--clay-all')
    # Source-controlled substitution for the diagnostic branch only.
    original=renderer.main
    import inspect
    code=inspect.getsource(original).replace("clay if frame['view'] in {'clay','clayalt'} else wire if frame['view']=='wire' else None","clay")
    scope=renderer.__dict__;exec(compile(code,__file__,'exec'),scope);scope['main']()
else:
    renderer.main()
