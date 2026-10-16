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
