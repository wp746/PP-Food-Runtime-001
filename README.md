# PP Food MiniProgram Node Handoff

这是给小程序开发公司的 **Node/TypeScript 交接基线**。

> 当前版本：`handoff-v1.0.0`
>
> 状态：**已验证方向基线，不是最终冻结版**。S01「椰椰西瓜冰」与 S02「桔子罐头」已证明当前 B/KV 视觉方向接近目标；跨更多品类的稳定性验证仍在继续。

## 开发公司先读什么

按顺序阅读：

1. `HANDOFF.md`
2. `docs/NODE_INTEGRATION_GUIDE.md`
3. `docs/PROMPT_RUNTIME_FULL.md`
4. `docs/CATEGORY_PROFILES.md`
5. `docs/QC_RETRY.md`
6. `docs/SECURITY_AND_FACTS.md`
7. `src/ppFoodPrompts.ts`
8. `src/pipeline.ts`

## 这套东西解决什么

小程序用户只需要：

- 上传一张食品/商品图片
- 选择 `A`（商拍）或 `B`（海报 KV）
- B 可额外填写标题、副标题、slogan、品牌、卖点等

后端负责：

```text
上传原图
  -> Vision Observer
  -> Product Truth
  -> A 商拍
  -> A QC
  -> A PASS
  -> B Copy Firewall
  -> Category Visual Translation
  -> B Art Director
  -> Primary + Challenger
  -> B Prompt Compiler
  -> Image Model
  -> Independent B Evaluator
  -> Targeted Retry
  -> Final
```

## 最重要的接入原则

**不要**把所有规则拼成一个超长 system prompt 后让一个模型自由理解。

职责必须拆开：

- Vision：只识图、抽 Product Truth
- A Director：只做商拍艺术指导
- A Image Model：执行商拍
- A QC：只判保真/商拍质量
- Copy Firewall：只做文案事实隔离
- Category Translator：只输出当前产品视觉语言
- B Art Director：只输出结构化方向
- B Image Model：执行 KV
- B Evaluator：独立看图打分/判失败码
- Retry：只修失败维度

## A / B 定义

### A = 高保真商业商拍

- 保留真实产品 DNA
- 升级灯光、背景、空间、景深、质感、镜头
- **不做海报，不加字**

### B = 商业 KV

- 必须基于当前 Job 的 A PASS 图
- 锁 Product DNA，不锁死 A 的相机机位
- 产品是 Hero #1
- 主标题是 Hero #2
- 标题材质必须从当前产品感官属性里“长出来”
- 默认不追求极简
- 允许中高信息密度，但必须有层级

## 推荐技术栈

现有 Node 项目可直接使用：

- TypeScript
- 任意 HTTP client
- Vision/QC：多模态 LLM
- Image：支持 reference image / image edit 的图像模型
- 后端环境变量保存 API Key

## 文件结构

```text
src/
  types.ts
  ppFoodPrompts.ts
  pipeline.ts
  index.ts

docs/
  PROMPT_RUNTIME_FULL.md
  CATEGORY_PROFILES.md
  NODE_INTEGRATION_GUIDE.md
  QC_RETRY.md
  SECURITY_AND_FACTS.md

examples/
  request-a.json
  request-b.json

tests/
  promptCompiler.test.ts
```

## 当前视觉母版原则

PP Food 当前上限 KV 不是“统一皮肤”，而是统一质量结构：

```text
强产品
+ 强标题
+ 产品感官属性驱动的字体材质
+ 一个明确的大创意
+ 前中后景共构
+ 丰富但受控的信息系统
+ 品类专属氛围
+ 高商业完成度
```

## 明确禁止

- 产品漂移
- 包装/器皿重设计
- 旧任务品牌/文案泄漏
- `面包 -> 巨型烤炉洞穴` 这类字面联想
- `巨大留白 + 小字 + 产品摆件化` 的安全编辑海报塌缩
- `照片 + 贴字`
- 所有品类统一黑金/木牌/玻璃/牛皮纸模板
- 为了填版式而编造价格、地址、电话、奖项等硬事实

## 版本冻结提醒

开发公司可以按本仓库接入 **当前验证基线**，但正式上线前应以业主最终确认的 Runtime 版本为准。跨品类稳定性验证完成后，仓库会再标注 `FROZEN_FOR_PRODUCTION`。