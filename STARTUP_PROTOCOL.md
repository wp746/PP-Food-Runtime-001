# Startup Protocol

When `SETUP_GATE.md` passes:

```text
RUNTIME_STATE = READY_WAITING_FOR_START
```

Reply briefly that the runtime is ready and wait for the user to say:

```text
启动
```

Only then:

```text
RUNTIME_STATE = PRODUCTION
```

In PRODUCTION do not repeatedly ask for model names, base URL, or credentials unless the runtime actually fails or configuration changes.

The user should not need to understand internal contracts, JSON, category IDs, or prompt compilation.
