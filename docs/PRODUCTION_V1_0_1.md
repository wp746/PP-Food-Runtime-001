# PP Food Runtime 1.0.1 — Title Spatiality Hardening

## Scope

Runtime 1.0.1 is a bounded production hardening of Stage B typography. It does not change Stage A fidelity methodology, Product Truth authority, provider architecture, copy firewall, category routing, Golden floors, Production Fast retry caps, or evaluator protocol behavior established in 1.0.0.

## Live-discovered regression

A real Chinese hot-food KV test produced a commercially usable food hero but the headline/subtitle collapsed into flat graphic overlays with weak perspective and no meaningful scene depth. A subsequent corrected render demonstrated the desired behavior: product remained hero #1 while headline/subtitle had visible depth, perspective, material response, overlap and scene integration.

## 1.0.1 contract

- Headline remains visual hero #2; product remains visual hero #1.
- Headline and subtitle/supporting-title must occupy distinct depth roles.
- Spatial evidence may use perspective/foreshortening, layered thickness/relief, carrier depth, overlap/occlusion, contact/cast shadow, shared scene lighting, or foreground/midground/background crossing.
- Literal thick 3D extrusion is not mandatory in every category; restrained editorial categories may satisfy spatiality through layered planes, perspective, overlap/occlusion and light integration.
- Flat photo-plus-text title treatment is rejected as `TITLE_SPATIALITY_WEAK`.
- `TITLE_SPATIALITY_WEAK` is a Production Fast delivery hard gate.
- Its targeted retry freezes Stage A, product truth, authorized copy and passing visual dimensions, and repairs only title depth/perspective/overlap/material/light integration.
- Title repair must never solve spatiality by shrinking or demoting the product.

Canonical detailed rule: `docs/B_KV_TITLE_SPATIAL_RULES.md`.

## TDD evidence

The change was introduced test-first:

1. Runtime prompt/compiler and production-gate tests were added before implementation and failed on the 1.0.0 behavior.
2. Implementation then added the new failure code, prompt contract, art-direction spatial behaviors, evaluator evidence rules, production hard gate, and targeted retry mapping.
3. Pre-release implementation CI reached `88 passed / 3 skipped / 0 failed` before the 1.0.1 metadata freeze.

The 3 skipped tests remain opt-in private/real-provider tests and are not silently treated as PASS.
