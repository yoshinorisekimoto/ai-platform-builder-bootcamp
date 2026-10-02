# AI Platform Builder Bootcamp — Day41-50シリーズ 執筆ルール

Day41から、複数ステージにまたがる「End-to-End Partner Workflow」という
連載を書いている。各Day記事は以下の軽量テンプレートに従うこと。

## 記事の型(Day44以降、固定)

# Day [N]: [Stage Name]

## Objective
[このステージの目的、1-2文]
Common rules, vocabulary, roles, and AI–Human boundaries are defined in
the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).
This is Stage [X] of the End-to-End Partner Workflow (Days 41–50).

## Stage Specification
### Inputs
### Stage-Specific Role(s)  ※新しい役割が出たら必ず1行で定義する
### [このステージ固有のルール名]
### Outputs
### Stop Conditions
### Workflow

## Applied to This Case
### Case
### Actions
  各パターンごとに:
  - Action: `UPPERCASE_SNAKE_CASE`(命令形の動詞から始める)
  - Status: ...
  - Next owner: ...
  - Resume Condition: ...(停止がある場合)
### Test Result(表形式: Test case / Expected result / Result)

## Governance
### Stage-Specific Audit Requirements
### Human Review Points
### Future Compatibility

## 禁止事項(重要)

- 共通ルール(AIの禁止事項8項目、Notify/Escalate/Resume Conditionの定義、
  AI and Human Boundaryの定型文)は書かない。必ずAGENTS.mdの
  Shared Frameworkへのリンクで済ませる。
- 日本語の説明セクション(「中学生向け説明」等)は入れない。
  Day36時点で廃止済みの方針。全文英語で統一する。
- Day41-43は旧フォーマットのまま残しており、遡って修正しない。
  Day44以降のみこのテンプレートを使う。

## 目的

1記事あたりの長さを150-200行程度に抑えるため。Day41→43で
343行まで肥大化し、外部の読者(採用担当者)に読まれなくなる
リスクが高いと判断し、Day44からこの方式に切り替えた。