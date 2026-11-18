# Hydropteris / Dorfiella knowltonii: matching-poster repair

Source baseline: `7f20f92544c2708b1c11187e086a7dc128bb27ba`. The existing scientific name, interpretation limits and references are retained. This is not a model reconstruction.

## Finding and change

The historical 512 px static posters show another view and an opaque grey background. Switching to the actual shared WebGL view visibly changed the plant orientation, projection and background. Replace both posters, and the downloadable preview, with transparent captures from the exact unchanged model using the production renderer. The GLB `fe41fc3bcfd8635b0ab16d8ec48bc5b6f89639690f45d6ed740032532399e835` and Blender source `f9c07aba9eb1c7d60fcfbbf13397ab680e4a78fba022c52e0c53e268d164cf64` are retained byte-for-byte. Geometry, UV, embedded texture and material are unchanged.

A runtime material comparison explicitly redrew four directions on desktop and phone. Setting metalness to zero made the leaves paler but did not establish a better artistic result; that experiment was not adopted. Fine roots, leafy silhouette and brown uncertain appendages remain unchanged. The source file is the previously supplied editable GLB import, not a newly reconstructed historical authoring session.

## Scoped verification

Unmodified current Vite source and official asset-delivery/catalog/static-route functions built a three-model local site (this model plus two switching anchors). No substituted renderer or intercepted model body was used. The original handoff has 27 desktop and 6 phone samples; the replacement has 7 desktop and 6 phone samples. The replacement phone sequence contains a 3.213 ms timestamp reversal at samples 1→2, so the files do not establish a continuous frame timeline. Held-poster and ready-model views were visually compared at 1440 and 390 px: the major orientation, position, scale and colour mismatch is resolved; shadow and edge sampling are not pixel-identical.

Eight browser cases passed: two viewports × rapid ready-state reselection, delayed response after selection change, failed-load retry with at least two requests, and drag/reset. Reset waits for the actual animation endpoint and checks camera/target within `1e-4`, quaternion within `1e-7`. Phone viewport emulates touch capability, but reset rotation uses mouse input, not certified physical-device touch.

Focused tests check unchanged GLB/source and scientific scope, poster source/hash bindings, actual generated ZIP/credits and target-only catalog changes. This report is not whole-inventory acceptance or deployment. Independent review and final shared-branch integration are required before marking the task complete.
