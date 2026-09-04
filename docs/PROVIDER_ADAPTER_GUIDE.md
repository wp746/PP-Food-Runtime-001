# Provider Adapter Guide

## 1. 角色分离

建议三种 provider role：

```text
VISION_PRIMARY
IMAGE_PRIMARY
QC_PRIMARY
```

Vision 与 QC 即使使用同一个多模态模型，也应当以不同 system prompt / role 调用，避免生成器自评。

## 2. 当前已验证目标模型配置

当前验证环境曾使用：

```text
Vision / QC:
SiliconFlow
Qwen/Qwen3-VL-32B-Instruct

Image:
Yunwu
 gpt-image-2
```

模型 ID 必须来自环境变量，不要硬编码在业务逻辑。

## 3. SiliconFlow

推荐环境变量：

```text
SILICONFLOW_API_KEY
SILICONFLOW_BASE_URL
SILICONFLOW_VISION_MODEL
SILICONFLOW_QC_MODEL
```

Vision 调用：

- source image + `VISION_OBSERVER_SYSTEM`
- JSON 输出
- 本地 schema 校验

QC 调用：

- source + candidate（A）
- source + A PASS + Primary + Challenger（B）
- 独立 evaluator system prompt

## 4. Yunwu / Image

推荐环境变量：

```text
YUNWU_API_KEY
YUNWU_BASE_URL
YUNWU_IMAGE_MODEL
```

硬要求：

- 必须实际发送参考图
- A 使用 source image 作为 reference
- B 使用 current-job Stage A PASS 作为 reference
- 9:16
- 返回可解码图片

不要静默退化到 text-to-image。

## 5. 请求协议

聚合平台的 reference-image 协议可能因网关版本不同而不同。

开发公司应以其当前实际可工作的 Yunwu/gpt-image-2 接口为准，并做最小能力 probe。

**不要为了适配某个 SDK 改写 PP Food Prompt 方法论。**

把 provider 差异留在 Adapter 层：

```ts
interface ImageProvider {
  edit({ image, prompt, aspectRatio }): Promise<ImageResult>;
}
```

## 6. Reference Binding

建议每次调用计算：

```text
sha256(reference image bytes)
sha256(prompt)
```

记录：

- jobId
- role
- model
- referenceSha256
- promptSha256
- outputSha256
- safe request id

如果 B 请求没有真正绑定 A PASS reference，应判：

```text
PROVIDER_FAILURE
```

而不是 Creative Retry。

## 7. Transport Retry 与 Creative Retry 分离

Transport retry：

- timeout
- connection reset
- 429
- 5xx

必须重用**完全相同的 prompt 和 reference**。

Transport retry 不增加 B creative cycle。

Creative retry 只处理视觉失败码。

## 8. API Key 安全

Key 不得：

- 下发到微信小程序
- 写进仓库
- 输出到日志
- 返回到客户端

所有 provider 调用必须在服务端进行。
