# Category Profiles

> Category 只负责合理性约束、禁区和商业行为，不直接输出固定皮肤。

## CHINESE_HOT_FOOD

```text
Core:
heat, steam, oil, sauce, fresh-cooked, savory, wok/broth energy

Prefer:
strong close product hero
warm directional light
steam bridge
medium-high information density
bold but product-derived Chinese typography

Avoid:
generic red-gold festival template
fake black-gold luxury
restaurant signboard cliché
```

## NOODLES_RICE_NOODLES

```text
Core:
steam, broth, slurp, texture, ingredient layering, regional identity

Prefer:
bowl depth
noodle surface clarity
steam trajectory
regional-but-modern typography
strong close foreground

Avoid:
generic noodle-shop signage
flat bowl + text layout
```

## BAKERY

```text
Core:
baked, grain, warm, crust, chew, handmade, fresh

Possible:
warm cream
amber
grain texture
paper
ceramic
restrained wood
morning/window light

Avoid default:
wood sign
old bakery
oven tunnel
cave/portal
kraft everywhere
wheat field cliché
```

## DESSERT_CAKE

```text
Core:
cream, softness, delicacy, layering, floral/tea/fruit nuance

Possible:
soft sculptural light
porcelain
silk
cream relief
controlled transparency

Avoid default:
pink
female-luxury cliché
glass-only language
perfume-ad impersonation
```

## COLD_DRINK_FRUIT_DESSERT

```text
Core:
cold, juicy, translucent, condensation, bright, refreshing

Possible:
liquid light
ice-like highlight
fresh plant shadow
gel / transparent material only when traceable to product

Avoid:
every drink = jelly 3D type
cheap neon
generic tropical template
```

## RETAIL_PACKAGED_FOOD

```text
Core:
package identity, label clarity, product conversion, shelf-ready commercial finish

Mandatory:
package fidelity
label readability
pack silhouette
brand hierarchy

Environment may be bold.
Package may not change.
```

## WESTERN_BISTRO

```text
Core:
precision plating, sauce control, sear, refined restaurant atmosphere

Prefer:
controlled directional key
modern type
less folkloric decoration
balanced negative space
premium restaurant finish

Avoid:
luxury black-gold by default
generic wine-cellar skin
```

## STREET_FAST_FOOD

```text
Core:
energy, crunch, heat, speed, abundance, indulgence

Prefer:
dynamic perspective
bold headline rhythm
close hero crop
high but controlled contrast
motion cues

Avoid:
cheap promo flyer chaos
too many stickers
```

## CLAYPOT_STEW

```text
Core:
heat, vessel presence, steam, bubbling sauce/broth, comfort, abundance

Prefer:
container as structural support, not hero replacement
steam-driven vertical depth
warm local contrast
headline integrated around vessel/steam field

Avoid:
generic old-kitchen set
oversized pot becoming the main visual idea
```

## CHINESE_PASTRY

```text
Core:
grain, powder, soft crumb, light sweetness, handmade, seasonal calm

Prefer:
light Chinese refinement
soft neutral materials
paper/porcelain/fabric only when product semantics support it
clean but not empty typography

Avoid:
automatic red-gold guochao
automatic palace/ink-painting cliché
```

---

# Cross-Category Firewall

每个 Job：

```text
1 PRIMARY CATEGORY
+ optional 1 AUXILIARY CATEGORY <= 25%
```

禁止多个品类视觉语法混合成“效果大杂烩”。

## Category Replacement Test

Evaluator 必须问：

> 如果把当前产品换成一个完全不同的品类，当前材质、灯光、字体、信息系统和空间是否还基本成立？

如果答案是 YES，则 Category Inevitability 偏低，说明视觉世界过于通用。
