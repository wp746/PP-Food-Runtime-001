# Setup Gate

Before production, confirm only the missing runtime items.

Required:

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

Credentials must remain in Secret / Environment / Connection storage. Do not echo API keys in normal chat.

## State

If any required item is missing or unknown:

```text
RUNTIME_STATE = SETUP_GATE
PRODUCTION_GATE = BLOCKED
```

If all declared capabilities are available:

```text
RUNTIME_CAPABILITIES_DECLARED = PASS
RUNTIME_STATE = READY_WAITING_FOR_START
```

Do not claim end-to-end verification unless a real production call or a matching verified runtime profile has proved it.
