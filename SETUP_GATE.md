# Setup Gate

Before production, confirm only the missing runtime items.

Required for A:

```text
VISION_MODEL
IMAGE_MODEL
API_BASE_URL
CREDENTIAL_PRESENT
REFERENCE_IMAGE_EDIT = TRUE
VISION_CAN_READ_USER_IMAGE = TRUE
VISION_CAN_READ_GENERATED_OUTPUT = TRUE
USER_IMAGE_CAN_REACH_IMAGE_MODEL = TRUE
STAGE_A_OUTPUT_CAN_FEED_STAGE_B = TRUE
```

Required for stable upper-bound B:

```text
B_CAN_RENDER_AT_LEAST_2_CANDIDATES_FROM_SAME_STAGE_A = TRUE
VISION_CAN_COMPARE_MULTIPLE_GENERATED_B_IMAGES = TRUE
WINNER_IMAGE_CAN_FEED_TARGETED_REFINEMENT = TRUE
```

Credentials must remain in Secret / Environment / Connection storage. Do not echo API keys in normal chat.

## State

If A capabilities are missing:

```text
RUNTIME_STATE = SETUP_GATE
PRODUCTION_GATE = BLOCKED
```

If A capabilities pass but multi-candidate B capabilities are unavailable:

```text
A_MODE = READY
B_QUALITY_MODE = DEGRADED
UPPER_BOUND_STABLE_CLAIM = FORBIDDEN
```

If all capabilities pass:

```text
RUNTIME_CAPABILITIES_DECLARED = PASS
B_QUALITY_MODE = VISUAL_AUDITION
RUNTIME_STATE = READY_WAITING_FOR_START
```

Do not claim end-to-end verification unless a real production call or matching verified runtime profile has proved it.