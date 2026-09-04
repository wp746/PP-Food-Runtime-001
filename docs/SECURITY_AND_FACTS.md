# Security & Fact Policy

## 1. API Key

API Key 只能存在于后端 Secret / Environment。

禁止：

- 放进小程序前端
- 写进 Git
- 写进 Prompt
- 写进日志
- 写进 Artifact JSON
- 截图回传

`.env.example` 只能留空值。

## 2. 事实分层

```text
OBSERVED_FACT
USER_VERIFIED_FACT
HIGH_CONFIDENCE_INFERENCE
UNKNOWN
```

硬商业信息只有 `USER_VERIFIED_FACT` 或可靠可读的当前包装信息才能用于正式成图。

## 3. 禁止编造

```text
price
address
phone
certification
award
origin
brand history
sales volume
ingredient claim
health claim
process claim
net weight
discount
store count
```

## 4. 测试模式

为了测试板式可以使用随机文案，但必须：

```text
LAYOUT_TEST_MODE=true
```

并在内部把所有测试字段标记为 `TEST_ONLY`。

测试假信息不能进入：

- 正式用户元数据
- 正式商品资料
- 正式发布文案
- 训练/Golden 事实字段

## 5. Current Job Isolation

每个请求只使用当前 Job 数据。

禁止从历史任务继承：

- brand
- copy
- address
- phone
- product name
- exact props
- layout skin
- background skin
- color palette

## 6. 用户图片

生产图片建议放对象存储，使用短期签名 URL 或后端二进制传递。

日志不要保存原始图片 base64。

## 7. Prompt / Artifact 审计

建议每个 Job 记录：

```text
runtimeVersion
promptVersion
promptSha256
provider
model
sourceSha256
stageASha256
outputSha256
evaluation
retryCode
```

## 8. 小程序前端边界

前端只能调用你们自己的后端：

```text
Mini Program
-> Your Node Backend
-> AI Providers
```

禁止：

```text
Mini Program
-> SiliconFlow/Yunwu/Image Provider directly
```

否则 Key、Runtime 规则和计费控制都会暴露。
