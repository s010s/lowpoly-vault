# Baseline browser acceptance checks

The tested application source is `0cbef7c9826ddd1d83e7d0c941b7864dbaa6865c`. The final main run has 16 cases and 96 checks.

| Case | Result | Check |
| --- | --- | --- |
| mobile-390-navigation | FAIL | list URL identifies collection without a detail model |
| mobile-390-navigation | PASS | initial list is usable with multiple visible rows |
| mobile-390-navigation | PASS | mobile initial list makes zero GLB requests |
| mobile-390-navigation | PASS | mobile click opens requested identity |
| mobile-390-navigation | PASS | detail URL differs from collection URL |
| mobile-390-navigation | PASS | detail URL contains selected identity |
| mobile-390-navigation | PASS | poster-first detail does not fetch GLB |
| mobile-390-navigation | FAIL | Collection restores original collection URL |
| mobile-390-navigation | PASS | Collection restores list scroll position |
| mobile-390-navigation | PASS | Collection restores visible virtual rows |
| mobile-390-navigation | PASS | Collection keeps results |
| mobile-390-navigation | PASS | mobile fits viewport |
| mobile-390-navigation | FAIL | browser Forward returns to the detail after Collection |
| mobile-390-navigation | FAIL | browser Back restores a collection URL |
| mobile-390-navigation | PASS | browser Back leaves multiple visible rows |
| mobile-390-navigation | PASS | browser Forward opens the same detail identity |
| mobile-390-navigation | FAIL | Collection after live 3D restores visible virtual list |
| mobile-320-navigation | FAIL | list URL identifies collection without a detail model |
| mobile-320-navigation | PASS | initial list is usable with multiple visible rows |
| mobile-320-navigation | PASS | mobile initial list makes zero GLB requests |
| mobile-320-navigation | PASS | mobile click opens requested identity |
| mobile-320-navigation | PASS | detail URL differs from collection URL |
| mobile-320-navigation | PASS | detail URL contains selected identity |
| mobile-320-navigation | PASS | poster-first detail does not fetch GLB |
| mobile-320-navigation | FAIL | Collection restores original collection URL |
| mobile-320-navigation | PASS | Collection restores list scroll position |
| mobile-320-navigation | PASS | Collection restores visible virtual rows |
| mobile-320-navigation | PASS | Collection keeps results |
| mobile-320-navigation | PASS | mobile fits viewport |
| mobile-320-navigation | FAIL | browser Forward returns to the detail after Collection |
| mobile-320-navigation | FAIL | browser Back restores a collection URL |
| mobile-320-navigation | PASS | browser Back leaves multiple visible rows |
| mobile-320-navigation | PASS | browser Forward opens the same detail identity |
| mobile-320-navigation | FAIL | Collection after live 3D restores visible virtual list |
| mobile-filter-collection-scroll | PASS | real collection filter applies |
| mobile-filter-collection-scroll | PASS | collection/query/sort results survive return |
| mobile-filter-collection-scroll | FAIL | filter URL restored exactly |
| mobile-filter-collection-scroll | PASS | filtered scroll restored |
| mobile-filter-collection-scroll | PASS | filtered list remains populated on screen |
| direct-path-refresh | PASS | direct detail identity and open state match URL |
| direct-path-refresh | PASS | refresh preserves requested detail identity |
| direct-path-refresh | PASS | direct refresh retains GLB download for requested model |
| direct-path-refresh | FAIL | direct detail Back reaches a list URL |
| direct-path-refresh | PASS | direct detail Back reaches healthy list |
| direct-query-refresh | PASS | direct detail identity and open state match URL |
| direct-query-refresh | PASS | refresh preserves requested detail identity |
| direct-query-refresh | PASS | direct refresh retains GLB download for requested model |
| direct-query-refresh | FAIL | direct detail Back reaches a list URL |
| direct-query-refresh | PASS | direct detail Back reaches healthy list |
| direct-zh-path-refresh | PASS | direct detail identity and open state match URL |
| direct-zh-path-refresh | PASS | refresh preserves requested detail identity |
| direct-zh-path-refresh | PASS | direct refresh retains GLB download for requested model |
| direct-zh-path-refresh | FAIL | direct detail Back reaches a list URL |
| direct-zh-path-refresh | PASS | direct detail Back reaches healthy list |
| mobile-rapid-open-back | PASS | rapid repeated navigation ends with usable collection |
| mobile-rapid-open-back | FAIL | rapid navigation ends at list URL |
| mobile-rapid-open-back | PASS | rapid navigation has one renderer |
| mobile-network-scroll | PASS | scrolling mobile never fetches GLB |
| mobile-network-scroll | PASS | mobile explicit selection remains poster first |
| mobile-network-scroll | PASS | explicit Interact loads selected real GLB |
| mobile-network-scroll | PASS | offscreen detail exits live rendering |
| mobile-network-scroll | PASS | return after explicit 3D restores populated visible list |
| mobile-image-latency-concurrency | PASS | delayed image rapid scrolling leaves functional list |
| mobile-image-latency-concurrency | PASS | delayed image scrolling does not load GLB |
| desktop-hover-selection-cancel | PASS | brief hover under 100ms avoids GLB request |
| desktop-hover-selection-cancel | PASS | intentional hover actually requests a GLB |
| desktop-hover-selection-cancel | PASS | leaving pending hover cancels resource request |
| desktop-hover-selection-cancel | PASS | hover never changes selection |
| desktop-hover-selection-cancel | PASS | long hover has real model first frame |
| desktop-hover-selection-cancel | PASS | explicit desktop selection works |
| desktop-hover-selection-cancel | PASS | desktop fits viewport |
| desktop-hover-selection-cancel | PASS | single renderer remains |
| desktop-hover-selection-cancel | PASS | desktop browser Back restores prior selection |
| desktop-hover-selection-cancel | PASS | desktop browser Forward restores explicit selection |
| mobile-pending-glb-cancel-back | PASS | explicit 3D request was actually delayed |
| mobile-pending-glb-cancel-back | FAIL | Back cancels offscreen pending GLB transfer |
| mobile-pending-glb-cancel-back | PASS | offscreen detail does not become ready after return |
| mobile-pending-glb-cancel-back | FAIL | cancel leaves visible list populated |
| desktop-rapid-pending-selection | PASS | rapid delayed selections cancel superseded GLB |
| desktop-rapid-pending-selection | PASS | latest explicit selection owns final pixels |
| desktop-rapid-pending-selection | PASS | quick switching keeps one renderer |
| mobile-hidden-collection-return-frames | PASS | return after hidden collection update shows multiple model rows |
| mobile-hidden-collection-return-frames | FAIL | first painted return frame has a populated list |
| startup-delayed-js | PASS | delayed prerequisite retains useful real linked HTML |
| startup-delayed-js | PASS | fallback fits mobile viewport |
| startup-delayed-js | FAIL | delayed JS/CSS does not expose the old static grid layout |
| startup-delayed-js | PASS | enhancement succeeds with usable collection |
| startup-delayed-css | PASS | delayed prerequisite retains useful real linked HTML |
| startup-delayed-css | PASS | fallback fits mobile viewport |
| startup-delayed-css | FAIL | delayed JS/CSS does not expose the old static grid layout |
| startup-delayed-css | PASS | enhancement succeeds with usable collection |
| no-js-fallback | PASS | no-JS listing has real model links |
| no-js-fallback | PASS | no-JS detail navigates to real document |
| no-js-fallback | PASS | no-JS detail exposes GLB and source downloads |
| no-js-fallback | PASS | no-JS detail fits mobile viewport |
| no-js-fallback | PASS | no-JS Back restores listing |
