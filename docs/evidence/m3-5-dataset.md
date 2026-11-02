# M3.5 dataset release

Started November 2, 2026, under the frozen [M3.5 collection brief](../collection-brief-m3-5.md) and Altan's November 2 decisions 6 and 7 recorded there. This note records the freeze first, then the collection as it happens. No row has been imported yet.

## Freeze, November 2

Altan changed the review protocol and confirmed the size rule on November 2. A new row is accepted when the AI screen's label and an independent blind AI check agree and neither flags it. Altan adjudicates every disagreement, flag or abstention and does not label every row. The 12-case timing pilot was not run, because the change removes per-row human labeling. The release will be disclosed as AI-labeled with human adjudication of disagreements; AI agreement is not human agreement. Lookup takes every reviewed row that passes, up to 500 (floor 350), and the other three classes split the rest to 2,000.

The agent wrote both answers into the brief's Review and "Before freezing" sections, then froze it. Guide v3 is the v2 annotation guide plus the brief's "Guide v3" section, so the two hashes below bind it.

| File | SHA-256 |
| --- | --- |
| `docs/collection-brief-m3-5.md` (frozen) | `5320797319b1206f4e11acae5ec7e16f90ea2500b14e21cc0f882ff80957e50e` |
| `docs/annotation-guide.md` (v2 guide, unchanged) | `dd78162cbf9dcbdaaa68f4ad0bd654aec8d1ea181fb453362d9ab1dcdcc8ba55` |
| `data/processed/m3-v1.jsonl` (parent release) | `4e9425fd65e2572bff1c7fefd9ef21692bf219479818903d4ec33a372fc55bbf` |
| `data/raw/m3-reviews-v1.jsonl` (parent ledger) | `e56b73a22a0e95893fb19efcbde1717ae803fb52ffa0ce668cbceb384a3248e9` |
| `data/splits/m3-split.json` (parent split) | `6d48e18bae6ac319bffecc98c68b6b02c8c4483f68a75eddb63db2a52213225f` |

Existing pools and orders at the freeze, all ignored under `work/`:

| Pool or order | SHA-256 |
| --- | --- |
| `m3-5-groups/option-b/databench/order.jsonl` | `119f64d1d7cb2faa6d48e81d2535ee4f23944f7daf9b28369865586d5ce8eaab` |
| `m3-5-groups/option-b/databench/contract.json` | `a4d270ed8e5cac1cb0258a32c3a71e869c299e07f9a94cf61e29c2a06f45a5a6` |
| `m3-5-groups/discovery/intents/clinc150-lookup-pool.jsonl` | `c4adc41a286c655d9d4fed9341dadc06ad0968e4ffbdbe705074885c9d3051ba` |
| `m3-5-groups/discovery/intents/clinc150-lookup-order.json` | `3d7c1232cd2da34478e367ffadc5adfe86f040632d04905095443cb4d337d0e8` |
| `m3-5-groups/discovery/intents/massive-lookup-pool.jsonl` | `a3e47fc978735ca6ea2965e3918ef796dc89f4805dae27d9e00def88a5eea0c3` |
| `m3-5-groups/discovery/intents/massive-lookup-order.json` | `0e47eeb9e42594a7eb067d93f97ce08f66294da80b9777ef87ac1b5cc321d7b6` |
| `m3-5-groups/lookup/ToolACE-focused-order.jsonl` | `11cce71a19d144fac08e985b1889ddefdaed559926b20ad90deee347eddb3d59` |
| `m3-5-groups/option-b/keyed/ToolACE-remainder-order.jsonl` | `2fabd59fa5b2b78a6fdc2bfd3833eef34e6e606f388a4df7f26b70327eaed4fc` |
| `m3-5-groups/lookup/ToolAlpaca-focused-order.jsonl` | `015970cfcb420939988da76873294a20972ccb5f15c968d518c429d77a35a51c` |
| `m3-5-groups/option-b/keyed/Glaive-skip.json` | `2922c2e89afdaba63b5ecb895a5cd9f55683436ade91758a7578e6cf7f06dc2b` |
| `m3-5-groups/audit/integrated-inventory.jsonl` | `a4fa2da71a8328551a641b091f7f7140cd35871e8c54938d7e3d6b93138ca131` |
| `m3-5-groups/discovery/intents/clinc150-calc-pool.jsonl` | `581f59dbae9f1d63c696b08e14e0846a3f45b9c0b95b2dc7bc7ac4122666842f` |
| `m3-5-groups/discovery/intents/clinc150-calc-order.json` | `0dbae1ef2aad4d901f05f66c8087a94214584241b7cac9cd4219fe39afd7667f` |
| `m3-5-groups/discovery/intents/massive-calc-pool.jsonl` | `f7d79a394bd9a2de86f94623408140a453bd1d491ee076c24102a65d4bd246fc` |
| `m3-5-groups/discovery/intents/massive-calc-order.json` | `ced861c67c81de0f598375b905116053db01a05fbefd30f5fa2768c3ee96e270` |
| `m3-5-groups/discovery/prompts/theoremqa-pool.jsonl` | `b9e4fae5b96b3b2cb303d913fee0dc44bb471b87127debe0ddf639e6d8bc63d5` |
| `m3-5-groups/discovery/prompts/theoremqa-self-order.json` | `ba2486c7ace7a0411bce4b652740ef4c9a847b850c1f798121d79dddcc921f46` |
| `m3-5-groups/discovery/prompts/oasst2-calculation-pool.jsonl` | `6db4b46221276ef0bc4e44bc40cd94fd6cb6507c8cc8d2a6a6b31de4e78d20b6` |
| `m3-5-groups/discovery/prompts/oasst2-calc-focused-order.json` | `b65c50d1ecb1f865d8461c02a7b25467c9de2accbcacbb403be04bb7c0888e5d` |
| `m3-5-screen/existing/gsm8k_test-pool.jsonl` | `7fc84820167874b36a751a6da34f8b68cc605bc1b8e8653c704424b57d56e5df` |
| `m3-5-screen/existing/dolly_closed_qa-pool.jsonl` | `83e74359d4fdf6c1f90afe34cebcb13a8ce978dd921bb171dcd1696964f38691` |
| `m3-5-screen/existing/dolly_information_extraction-pool.jsonl` | `9e56e0303ae314dc6ff9521dd3e65fa673e77a68a563802120d8513505018611` |
| `m3-5-screen/existing/dolly_summarization-pool.jsonl` | `cf35f86ccbd88ab831303dc54965d10d1a13b23e3f5d8d997165b658bd2dc554` |
| `m3-5-screen/existing/no_robots_passage_train-pool.jsonl` | `f8e858d28336c69255e16649b3ebce4421da91608ed389b24ea4d8e6305d4933` |
| `m3-5-screen/existing/no_robots_direct_train-pool.jsonl` | `b0c8d1e5f664d773a2e3bf717eceb246b277ec1fc23dbcdad7a2cfe3ae0b77e6` |
| `m3-5-screen/existing/dolly_direct-pool.jsonl` | `0d62df76f7880f56ec8d413701688d0a3ae5fe24eb92011f4c06966363739c14` |

## Size change after freezing, November 2

After the first adjudication round, Altan asked for more data ("We can make rules less strict than before to even obtain more dataset as it is one of the most important") and then chose "Up to 1,000 per class" and "Keep all rules". The brief's new section "Change after freezing" records it as decision 8, replacing the 2,000 total; every quality rule stays. The amended brief's SHA-256 is `5f881f83df5ed6a96585a3788ca9bd8c568286bba2570bf9bc6b9bdae8163f92`; the frozen version above stays the reference for rows screened before the change.

The `m3-5-screen/existing` pools saved only a seed-42 sample, not a full order. Their full orders keep that sample first and add the rest in a seed-42 shuffle, as the M3 import did; they are built with the two new pools and hashed below before any review. The full hash list, including the samples, is in ignored `work/m3-5-dataset/freeze.json`, written by `work/m3-5-dataset/freeze_hashes.py`.
