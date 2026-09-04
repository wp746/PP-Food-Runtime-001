# HANDOFF — 小程序开发公司交接说明

## 1. 你们接手的是什么

这是 PP Food 的 Node/TypeScript Prompt Runtime 交接基线。

它不是一个“把一大段 Prompt 塞给模型”的方案，而是一条固定生产链。

目标：

- 用户上传食品/商品图片
- 选择 A 或 B
- 后端稳定产出：
  - A：高保真商业商拍
  - B：高张力商业 KV

## 2. 不要改的核心行为

以下行为属于产品方法论，不是实现建议：

1. 当前 source image 是产品视觉真值。
2. A 只做商拍，不做 KV、不加字。
3. B 必须基于当前 Job 的 A PASS 图。
4. B 锁 Product DNA，但不锁死 A 相机。
5. Product Hero #1，Headline Hero #2。
6. Category 只提供约束和语境，不直接套固定视觉模板。
7. 当前产品感官语义是视觉语言的第一来源。
8. 字体材质必须能追溯到当前产品，而不是品类标签。
9. B 默认允许中高信息密度，不默认极简。
10. 生成模型不得自己宣布自己“世界级”。QC 必须独立。
11. 两个候选里较好的一张，不代表它已经合格；都低于门槛时返回 `NO_QUALIFIED_WINNER`。
12. Retry 必须按失败码定向修复，不允许随机整图重做。

## 3. 推荐后端状态机

### A

```text
A_REQUEST
-> VISION_ANALYSIS
-> PRODUCT_TRUTH_READY
-> A_DIRECTION_READY
-> A_PROMPT_READY
-> A_RENDER
-> A_QC
-> A_PASS | A_RETRY | FAIL
```

### B

```text
B_REQUEST
-> REQUIRE_CURRENT_A_PASS
-> COPY_FIREWALL
-> CATEGORY_TRANSLATION
-> PRIMARY_DIRECTION
-> CHALLENGER_DIRECTION
-> PRIMARY_RENDER
-> CHALLENGER_RENDER
-> INDEPENDENT_EVAL
-> QUALIFIED_WINNER?
     NO -> TARGETED_RETRY
     YES -> FINAL_QC
-> B_PASS
```

## 4. 接口建议

开发公司可以保留现有 Node 项目结构，只需把 Prompt Runtime 抽成服务层：

```ts
analyzeSourceImage()
runStageA()
evaluateStageA()
buildCopyAllowlist()
translateCategoryVisualLanguage()
buildPrimaryDirection()
buildChallengerDirection()
compileStageBPrompt()
renderStageB()
evaluateStageB()
planTargetedRetry()
```

## 5. Image Provider 约束

图片模型必须支持 reference image / image editing。

对每次生成保存：

- 当前 job id
- source hash
- A PASS hash
- prompt hash
- provider / model id
- output image
- QC result

不能静默退化成纯 text-to-image。

## 6. 文本生成模式

提供两种模式：

### `IMAGE_NATIVE`
图片模型直接渲染中文。

优点：空间融合更自然。

风险：中文可能错字。

### `HYBRID_COMPOSITE`
图片模型负责：

- 产品
- 场景
- 文字承载结构
- 标题空间规划
- 材质/光影提示

Node/Canvas/Sharp 后处理负责最终准确中文、品牌、价格、地址、二维码。

正式商业上线更推荐保留 Hybrid 作为兜底。

## 7. Prompt 文件怎么用

不要把 `docs/PROMPT_RUNTIME_FULL.md` 整段作为一个 system prompt。

请使用 `src/ppFoodPrompts.ts` 中对应模块：

- `GLOBAL_ORCHESTRATOR_SYSTEM`
- `VISION_OBSERVER_SYSTEM`
- `STAGE_A_DIRECTOR_SYSTEM`
- `COPY_FIREWALL_SYSTEM`
- `CATEGORY_TRANSLATOR_SYSTEM`
- `B_ART_DIRECTOR_SYSTEM`
- `B_EVALUATOR_SYSTEM`
- `RETRY_PLANNER_SYSTEM`
- `compileStageAPrompt()`
- `compileStageBPrompt()`

## 8. 当前验证状态

当前已明确达到预期方向的视觉母版包括：

- S01 椰椰西瓜冰：感官 -> 材质 -> 空间字体世界
- S02 桔子罐头：包装 Hero + 中高信息密度 + 成熟零售广告完成度

其他品类仍需继续做泛化稳定性验证，因此：

```text
HANDOFF STATUS = VALIDATED_BASELINE
PRODUCTION FREEZE = NOT YET
```

开发时不要擅自把此版本标记为最终冻结版。

## 9. 事实安全

永远禁止自行编造：

- 价格
- 地址
- 电话
- 认证
- 奖项
- 产地
- 品牌历史
- 配方/成分
- 健康功效
- 销量
- 折扣
- 净含量
- 门店数

测试板式需要假数据时，后端必须标记：

```text
LAYOUT_TEST_MODE=true
```

并且禁止把测试假数据写回正式产品事实。

## 10. 验收时重点看什么

A：

- 产品是否还是原产品
- 表面/数量/结构是否漂移
- 背景是否高级但不抢产品
- 灯光是否真正提升材质
- 是否仍是商拍而不是海报

B：

- 产品是否第一眼
- 标题是否第二眼
- 标题有没有视觉质量和空间存在感
- 字体材质是否来自产品属性
- 是否有一个明确 Big Idea
- 是否有多层空间
- 是否有品类必然性
- 信息是否丰富但不乱
- 是否像成熟 Campaign，而不是 AI 海报草稿

## 11. 需要开发公司返回给甲方的内容

完成初次接入后，请提供：

1. Node 接入文件路径
2. 实际使用的 Vision / Image / QC 模型名
3. A 请求与响应样例
4. B 请求与响应样例
5. 一次完整 Job 的日志（脱敏）
6. Prompt hash
7. A/B 生成图
8. 是否启用 Hybrid Composite
9. 是否存在任何你们自行修改的 Prompt 规则

任何对本仓库规则的修改，都必须单独列出 diff，不要静默修改。