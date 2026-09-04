# Validation Status

## Current Status

```text
HANDOFF BASELINE: READY
PRODUCTION FREEZE: NOT YET
```

当前已验证方向：

### S01 椰椰西瓜冰

确认有效的原则：

- Product Hero 强
- Headline Hero 强
- 感官语义 -> 材质 -> 空间字体
- 多层空间共构
- 年轻、清凉、果感与商业信息共存

### S02 桔子罐头

确认有效的原则：

- Package Hero 强
- 主标题强
- 中高信息密度但秩序清晰
- 金黄果香/阳光/丰盛感能够形成成熟零售广告世界

## 还需要继续验证的品类

优先：

1. 中式热菜
2. 汤面/米线
3. 烘焙
4. 蛋糕/甜点
5. 酸菜鱼/川湘热菜
6. 煲类
7. 西餐
8. 炸物/快餐
9. 中式糕点
10. 夜市小吃

## 生产冻结前建议门槛

每个代表 Case 重复 3 次：

```text
Fidelity 3/3 PASS
Copy 3/3 PASS
Category 3/3 PASS
Catastrophic Drift = 0
Upper-Bound >= 2/3 PASS
Worst run >= strong commercial baseline
```

重点是提高 `QUALITY FLOOR`，而不是 Best-of-20。

## 开发公司现阶段应该做什么

可以：

- 按此仓库接入现有 Node 项目
- 做 Provider Adapter
- 做 A/B API 路由
- 做 Prompt Compiler
- 做 Artifact/QC 日志
- 做 IMAGE_NATIVE / HYBRID_COMPOSITE 两种文字模式

不要：

- 自己重新发明另一套 Prompt
- 静默删除 QC
- B 直接跳过 A
- 把所有模块合并为一个自由 Agent
- 把本版本标为最终冻结版
