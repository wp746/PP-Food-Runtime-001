# Execution Modes

## Mode A

User trigger:

```text
A
执行A
```

Behavior:

```text
CURRENT USER IMAGE
→ VISION_MODEL
→ CURRENT_JOB_FACTS
→ A_EXECUTOR
→ IMAGE_MODEL reference edit
→ A_QC
→ targeted retry if needed
→ deliver Stage A only
```

No KV copy gate. No Stage B.

## Mode B

User trigger:

```text
B
执行B
```

Behavior:

```text
CURRENT USER IMAGE
→ current Stage A
→ A_QC PASS
→ Stage B copy gate
→ current category route
→ B_EXECUTOR
→ IMAGE_MODEL reference edit using current Stage A PASS image
→ B_QC
→ targeted retry if needed
```

B can never skip current Stage A.

## Copy Gate

Default formal B requires:

```text
HEADLINE
SUBTITLE
AUXILIARY_INFORMATION_COUNT >= 1
```

Product/dish name may serve as HEADLINE.

If missing, ask only for the minimum missing item(s). Do not repeat fields already supplied.

Only after the user explicitly authorizes default copy, such as `按默认文案来`, may the runtime generate non-factual subtitle/slogan/sensory campaign copy.

Never invent phone, address, price, opening hours, certification, awards, origin, history, process, unverified ingredients/flavor, or medical/health claims.
