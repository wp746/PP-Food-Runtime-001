# Developer Acceptance Checklist

开发公司初次接入完成后，请逐项确认：

## Architecture

- [ ] A 与 B 是两条明确状态机
- [ ] B 只能使用当前 Job 的 A PASS
- [ ] Vision / Director / Image / Evaluator 角色分离
- [ ] 业务 Controller 不直接自由拼 Prompt
- [ ] Prompt 唯一真源来自 `src/ppFoodPrompts.ts`

## Product Fidelity

- [ ] A 使用 source reference
- [ ] B 使用 current-job A PASS reference
- [ ] package/vessel 不被重设计
- [ ] ingredient topology 不被随意修改
- [ ] Product Truth failure 能阻断继续生成

## B Creative System

- [ ] Product Hero #1
- [ ] Headline Hero #2
- [ ] One Big Idea 恰好一个主导概念
- [ ] Typography material 来自当前产品感官语义
- [ ] 不套统一品类皮肤
- [ ] Primary / Challenger 至少两个结构维度不同
- [ ] 两张都不够好时可返回 NO_QUALIFIED_WINNER

## QC

- [ ] A 有独立 QC
- [ ] B 有独立 Evaluator
- [ ] Evaluator 看图，不读取生成器自评分
- [ ] 有 First Read 检查
- [ ] 有 Golden Vector
- [ ] 有 Anti-Pattern 检查
- [ ] Retry 按 failure code 定向修复
- [ ] 最大 B creative cycles = 3

## Copy / Security

- [ ] API Key 只在服务端
- [ ] 未支持硬事实不会被自动编造
- [ ] LAYOUT_TEST_MODE 与 production facts 隔离
- [ ] 日志不输出 Authorization / API Key
- [ ] 小程序前端不直连模型 Provider

## Text Rendering

- [ ] IMAGE_NATIVE 模式可用
- [ ] 文案准确度 QC 可用
- [ ] HYBRID_COMPOSITE 预留或已实现

## Delivery Back to Owner

请返回：

- [ ] 接入 commit SHA
- [ ] 使用的 Vision / Image / QC 模型
- [ ] A 调用示例
- [ ] B 调用示例
- [ ] 一条完整脱敏 Job 日志
- [ ] A 输出图
- [ ] B Primary / Challenger / Final 图
- [ ] 对 Prompt 的任何本地改动 diff
