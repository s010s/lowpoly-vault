/** One-time frozen history boundary: the five already reviewed PR60 bridges.
 * These are historical records, not a new current-code approval or asset grant.
 * Callers MUST still verify the original descriptor, snapshots, reviews and assets.
 * Any byte/path change is refused by the caller; new bridges are not supported. */
import {createHash} from 'node:crypto';
const sha256=b=>createHash('sha256').update(b).digest('hex');
const preserved=[
  [
    "production/poster-inspection-compatibility-20261023/first3-bridge.json",
    "5c0aea99fa36d48a7b47843dfbdf64d2788868dfcba2ba1e1c9c9b6064afdbf9",
    "production/poster-inspection-compatibility-20261023/first3-review.json",
    "bfc874143258ebbb3e8007b787c4ebd8f27a7ee6725c125a2e2871cc83d80122"
  ],
  [
    "production/poster-inspection-compatibility-20261023/next11-bridge.json",
    "2a01dbe892ef934471fd3c9785de4d1f56ee217379f19b29b4e89d451b883565",
    "production/poster-inspection-compatibility-20261023/next11-review.json",
    "704b904ea09fb76043e88999f13a010c65a8188a6d59ccef8381a20e0a05b5d8"
  ],
  [
    "production/poster-inspection-compatibility-20261023/drive10-bridge.json",
    "af9bd0bdec05524ab898d15028c0266f3a7e027d4c74786905657d5850b8fdce",
    "production/poster-inspection-compatibility-20261023/drive10-review.json",
    "6c747ce825cd3f541e07767711f414ef5446ee01d0f18fc241e9551052d3a79b"
  ],
  [
    "production/poster-inspection-compatibility-20261023/ready72-legacy-bridge.json",
    "358ff8326084b06febcbd2487a1848709b110db1efee9684e4958d02933cbbad",
    "production/poster-inspection-compatibility-20261023/ready72-legacy-review.json",
    "af2a04bb4b3834fda3c7fdf015e94cfc81d5ed6dda7ca57ae352166a0b8c0505"
  ],
  [
    "production/poster-inspection-compatibility-20261023/ready72-v2-bridge.json",
    "60eb8e12a8bb5a37e37067dc5b9ce573098775b95422ffe4a441292a30af5216",
    "production/poster-inspection-compatibility-20261023/ready72-v2-review.json",
    "3ab8c8177166af072b1b6a229bf589011673ffd9de94b84752caed066e8938fa"
  ]
];
export function isPreservedImplementationBridge(path,raw,reviewPath,reviewRaw){
 return preserved.some(([p,h,r,rh])=>path===p&&reviewPath===r&&sha256(raw)===h&&sha256(reviewRaw)===rh);
}
