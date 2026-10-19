# Third-party notices

This project’s own code is licensed under MIT. Third-party components retain their original licenses; this document does not relicense them.

## Three.js 0.180.0 — bundled browser dependency

The gallery bundles Three.js, including its GLTFLoader and OrbitControls addons, locally. No runtime CDN is required.

- Official project: https://github.com/mrdoob/three.js
- Versioned license source: https://github.com/mrdoob/three.js/blob/r180/LICENSE
- License: MIT

The following notice is reproduced verbatim from the installed Three.js 0.180.0 package:

```text
The MIT License

Copyright © 2010-2025 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## Build and test tools

The following direct development dependencies are used for building or testing. Their packages are not shipped as gallery runtime dependencies. Their original package licenses remain applicable; the repository’s MIT license does not replace them.

| Package | Locked version | Original license | Official project |
| --- | --- | --- | --- |
| Vite | 7.3.7 | MIT | https://github.com/vitejs/vite |
| Playwright | 1.56.1 | Apache-2.0 | https://github.com/microsoft/playwright |
| Khronos glTF Validator | 2.0.0-dev.3.10 | Apache-2.0 | https://github.com/KhronosGroup/glTF-Validator |

Transitive tooling dependencies likewise retain their respective package notices and licenses. See package-lock.json and the installed packages for their exact versions and license information.

Original asset models, renders and collection documentation have their separate CC BY 4.0 terms, described in the repository’s LICENSE and ATTRIBUTION.md.

## Emil Kowalski animation skills — development references

Official source: https://github.com/emilkowalski/skills at commit `2d228630ba1446365f614a108cb8252f1feda202`. The find-animation-opportunities, animate (including RECIPES.md), and review-animations (including STANDARDS.md) references are retained verbatim under `.agents/skills/emil-animation/`. These references are not gallery runtime code.

```text
MIT License

Copyright (c) 2026 Emil Kowalski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


## Gallery scale-reference geometry

The 18 cm hand and 1.8 m human comparison references are adaptations of MakeHuman core graphical assets and the Innerscene anatomical hand, provided under CC0 1.0. These illustrative references are separate from the CC BY 4.0 catalog models. Calibration, source links and license texts are retained in `site/public/gallery/scale-reference/SCALE-REFERENCE-LICENSES.txt` in the source repository. Deployed copies are available under `gallery/scale-reference/`.

The gallery uses Three.js and its OrbitControls/GLTFLoader under the existing MIT notice above.

## Marine quartet factual references

The Emeraldella, Burgessia, Tuzoia and Sanctacaris pages of the Royal Ontario Museum Burgess Shale site were consulted as factual references only. Source URLs and the limited claims they support remain beside each published model and in the frozen candidate evidence. No third-party image, model, texture or code was included. Tuzoia soft anatomy is explicitly a genus-inspired composite; all four palettes and simplified details are original artistic choices.
