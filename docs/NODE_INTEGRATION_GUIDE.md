# Node Integration Guide

## 1. 推荐模块边界

```text
src/
  ppFoodPrompts.ts   # 唯一 Prompt 真源
  types.ts           # 数据结构
  pipeline.ts        # 固定状态机
  index.ts           # export
```

业务 Controller 不应直接拼 Prompt。

## 2. 推荐业务接口

```ts
analyzeSourceImage(input)
runStageA(input)
evaluateStageA(input)
runStageB(input)
evaluateStageB(input)
```

如果项目已有 Service/Controller 分层，把 PP Food 放进 Service 层即可。

## 3. 建议 Job 数据

```ts
{
  jobId,
  mode,
  sourceImageUrl,
  sourceImageSha256,
  stageAPassImageUrl,
  stageAPassSha256,
  productTruth,
  userFacts,
  copyAllowlist,
  categoryTranslation,
  primaryDirection,
  challengerDirection,
  compiledPrompts,
  providerProfile,
  outputs,
  evaluations,
  retries,
  finalDecision
}
```

## 4. A 调用链

```ts
const vision = await visionModel({
  system: VISION_OBSERVER_SYSTEM,
  images: [sourceImage],
  responseFormat: "json"
});

const direction = await llm({
  system: STAGE_A_DIRECTOR_SYSTEM,
  input: { productTruth: vision }
});

const prompt = compileStageAPrompt({
  productTruth: vision,
  artDirection: direction
});

const candidate = await imageProvider.edit({
  image: sourceImage,
  prompt,
  aspectRatio: "9:16"
});

const qc = await visionModel({
  system: STAGE_A_QC_SYSTEM,
  images: [sourceImage, candidate],
  input: { productTruth: vision }
});
```

A QC `PASS` 后，保存 candidate 作为当前 Job 的 `stageAPassImage`。

## 5. B 调用链

```ts
assert(stageAPassImage);

const copy = await llm({
  system: COPY_FIREWALL_SYSTEM,
  input: userFacts
});

const translation = await llm({
  system: CATEGORY_TRANSLATOR_SYSTEM,
  input: { productTruth, userFacts, copy }
});

const primary = await llm({
  system: B_ART_DIRECTOR_SYSTEM,
  input: { productTruth, translation, copy, variant: "PRIMARY" }
});

const challenger = await llm({
  system: B_ART_DIRECTOR_SYSTEM,
  input: {
    productTruth,
    translation,
    copy,
    variant: "CHALLENGER",
    diversityRequirement:
      "must differ from Primary in at least two structural dimensions"
  }
});

const promptA = compileStageBPrompt({ ...job, direction: primary });
const promptB = compileStageBPrompt({ ...job, direction: challenger });

const [imgA, imgB] = await Promise.all([
  imageProvider.edit({ image: stageAPassImage, prompt: promptA, aspectRatio: "9:16" }),
  imageProvider.edit({ image: stageAPassImage, prompt: promptB, aspectRatio: "9:16" })
]);

const evaluation = await visionModel({
  system: B_EVALUATOR_SYSTEM,
  images: [sourceImage, stageAPassImage, imgA, imgB],
  input: { productTruth, translation, copy }
});
```

## 6. 不能把 B 直接写成一次调用

不要：

```text
source image + 所有规则 + 用户文案 -> image model
```

原因：

- Product Truth 不稳定
- Category 路由不可控
- 生成器会自我合理化
- Retry 无法定位
- Host/Agent 换了就会漂

## 7. Provider 适配

图片模型必须支持参考图。

Provider Adapter 至少暴露：

```ts
interface ImageProvider {
  edit(input: {
    image: Buffer | string;
    prompt: string;
    aspectRatio: "9:16";
  }): Promise<ImageResult>;
}
```

Vision/QC：

```ts
interface VisionProvider {
  analyze(input: {
    system: string;
    images: Array<Buffer | string>;
    input?: unknown;
  }): Promise<unknown>;
}
```

## 8. Reference Binding

每次图片生成前记录：

- reference sha256
- job id
- prompt sha256
- provider/model

如果 provider 实际请求未携带 current-job reference：

```text
PROVIDER_FAILURE
```

不要把这种错误当成 Prompt 创意问题重试。

## 9. 中文文字

建议实现：

```ts
type TextMode = "IMAGE_NATIVE" | "HYBRID_COMPOSITE";
```

### IMAGE_NATIVE

图片模型直接生成文字。

QC 必须检查 100% 文案准确。

### HYBRID_COMPOSITE

图片模型设计整体 KV 与文字空间；Node 侧用 Canvas/Sharp/SVG 等后处理准确中文。

正式商业上线建议保留 Hybrid 兜底。

## 10. Artifact / Logging

保存：

- runtime version
- prompt version
- prompt hash
- provider/model id
- source/A/B image hash
- evaluator JSON
- retry code

不要保存：

- API Key
- Authorization header
- 完整敏感 provider response

## 11. 版本控制

Prompt 规则修改必须：

- 修改 `VERSION`
- 保留 Git diff
- 重新跑跨品类验证

不要让开发人员在业务代码里单独改一份 Prompt，造成运行逻辑与仓库不一致。
