# QC & Retry

## A QC

顺序：

1. product identity
2. geometry
3. visible count
4. ingredient/component topology
5. surface state
6. package/vessel
7. plating/physical relations
8. product hero
9. material reveal
10. background relevance
11. lighting
12. composition/depth
13. commercial finish

产品真值属于 hard gate，不能被创意分数抵消。

## B Golden Vector

0-10 分：

```text
product_hero_strength
headline_aggression
typography_product_symbiosis
one_big_idea_clarity
compositional_depth_tension
category_inevitability
information_density_control
commercial_finish
```

当前门槛：

```text
product_hero_strength >= 9.0
headline_aggression >= 8.8
typography_product_symbiosis >= 8.5
one_big_idea_clarity >= 8.3
compositional_depth_tension >= 8.8
category_inevitability >= 8.5
information_density_control >= 7.8
commercial_finish >= 9.0
```

## First Read

默认目标：

```text
1 PRODUCT
2 HEADLINE
3 BIG IDEA / SECONDARY MESSAGE
```

如果第一眼是场景/洞穴/建筑/木牌：`SCENE_DOMINATES_PRODUCT`。

如果第一眼只有大标题、产品弱：`HEADLINE_DOMINATES_PRODUCT`。

## Anti-Pattern

必须检查：

```text
SAFE_EDITORIAL_COLLAPSE
SCENE_DOMINATES_PRODUCT
CATEGORY_CLICHE_DEPENDENCE
GENERIC_PREMIUM_SKIN
PHOTO_PLUS_TEXT
TEMPLATE_REUSE
INFORMATION_STARVATION
INFORMATION_OVERLOAD
```

### SAFE_EDITORIAL_COLLAPSE

典型表现：

- 巨大留白
- 小而“高级”的字
- 漂亮商拍
- 低信息密度
- 缺乏标题压强 / Big Idea / 空间 tension

这种图可能“漂亮”，但不属于默认 PP Food Upper-Bound。

### PHOTO_PLUS_TEXT

如果产品图和文字可以轻易拆开，字体只是贴在空白区：FAIL/RETRY。

### SCENE_DOMINANCE

如果去掉产品后，场景本身比产品更像主视觉：FAIL/RETRY。

## Score Calibration

```text
0-3 severely broken
4-5 weak
6 functional
7 good commercial baseline
8 strong
9 Golden-range
10 exceptional / North-Star-range
```

Evaluator 不允许动不动给 9.5。

每个重要分数必须写：

- what is visible
- where it is visible
- why it helps/hurts

## Pairwise Rule

Primary > Challenger 不等于 Primary PASS。

如果两个都低于门槛：

```text
NO_QUALIFIED_WINNER
```

## Retry Mapping

```text
PRODUCT_IDENTITY_DRIFT -> FIDELITY_RETRY
PRODUCT_NOT_FIRST_HERO -> HERO_RETRY
HEADLINE_TOO_WEAK -> HEADLINE_PRESSURE_RETRY
TYPOGRAPHY_DISCONNECTED -> TYPOGRAPHY_SYMBIOSIS_RETRY
BIG_IDEA_WEAK -> BIG_IDEA_RETRY
COMPOSITION_FLAT -> COMPOSITION_RETRY
CATEGORY_GENERIC -> CATEGORY_TRANSLATION_RETRY
INFORMATION_STARVED -> INFORMATION_RETRY
INFORMATION_OVERLOAD -> INFORMATION_RETRY
COMMERCIAL_FINISH_WEAK -> COMMERCIAL_FINISH_RETRY
GOLDEN_DISTANCE_TOO_HIGH -> GOLDEN_DISTANCE_RETRY
```

## Pass Freeze

已经通过的维度必须冻结。

例：

```json
{
  "productTruth": true,
  "productHero": true,
  "headline": false,
  "typographySymbiosis": false,
  "bigIdea": true,
  "composition": true,
  "information": true,
  "commercialFinish": true
}
```

Retry 只修 false 及其必要依赖。

## Retry Levels

```text
1 targeted repair
2 concept adjustment
3 art-direction rebuild
```

B 最大 creative cycles = 3。

超过后：

```text
NEEDS_HUMAN_REVIEW
```

不要无限烧图碰运气。
