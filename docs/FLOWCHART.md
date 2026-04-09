# 任務管理系統 - 流程圖與資料流

本文件基於 PRD 的需求與既定系統架構，使用 Mermaid 語法繪製了「使用者操作動線」與「核心功能的系統運作序列圖」，並提供初步的路由 (Routes) 路徑對照表。這將有助於確保開發實作不會脫離原本產品設計的預期。

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者進入網站後，在各個任務互動功能之間的完整操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 任務列表]
    
    Home --> Action{要執行什麼操作？}
    
    Action -->|新增| Add[在表單填寫任務名稱與描述]
    Add -->|點擊送出| SaveAdd[系統儲存任務]
    SaveAdd --> Home
    
    Action -->|切換狀態| Toggle[點擊「完成」或「未完成」按鈕]
    Toggle -->|系統變更狀態| Home
    
    Action -->|刪除| Delete[點擊「刪除」按鈕]
    Delete -->|確認並刪除資料| Home
    
    Action -->|篩選檢視| Filter[點擊狀態過濾標籤]
    Filter -->|顯示特定狀態任務| Home
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖進一步展示當使用者執行**「填寫表單並新增任務」**操作時，瀏覽器、Flask、資料處裡層 (Model) 與 SQLite 資料庫之間的完整溝通流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask Route (Controller)
    participant Model as Task Model
    participant DB as SQLite 資料庫

    User->>Browser: 填寫「繳交專題報告」並送出表單
    Browser->>Flask: POST /tasks/add (攜帶表單資料)
    Flask->>Model: 呼叫新增任務邏輯 (create_task)
    Model->>DB: 執行 SQL: INSERT INTO ...
    DB-->>Model: 指令執行成功
    Model-->>Flask: 成功建立實體資料
    Flask-->>Browser: 回傳 HTTP 302 (重導向至首頁 /)
    
    Browser->>Flask: GET / (重新要求載入首頁)
    Flask->>Model: 取得最新的任務列表
    Model->>DB: 執行 SQL: SELECT * FROM ...
    DB-->>Model: 回傳資料記錄
    Model-->>Flask: 取回 Python 資料列表
    Flask-->>Browser: 渲染 Jinja2 (index.html) 並呈現網頁
    Browser-->>User: 畫面顯示包含「繳交專題報告」的最新狀態
```

## 3. 功能清單對照表

根據 PRD 需求與上述流程，我們先簡單盤點系統中所需要的操作路徑 (URL Routing)。

| 功能名稱 | HTTP 方法 | URL 路徑 | 注意事項 / 處理邏輯 |
|---|---|---|---|
| 查看任務清單 | `GET` | `/` | 渲染首頁列表（可透過 `?status=completed` 等參數進行篩選）。 |
| 新增任務 | `POST` | `/tasks/add` | 接收入力資料 (Form Data)，建立後自動導回首頁。 |
| 切換完成狀態 | `POST` | `/tasks/<task_id>/toggle` | 用於勾選 / 取消勾選已完成的任務，並自動導回首頁。 |
| 刪除任務 | `POST` | `/tasks/<task_id>/delete` | 接收刪除請求並操作 DB，保護性質強的刪除行為避免用 GET 發動。 |

> **設計考量**：因為本專案技術環境為純 Flask 搭配 SSR（伺服器端渲染，不依賴龐大的 JavaScript AJAX 與前端路由），所有的操作在處理完邏輯後，皆直接透過 HTTP 重導向（Redirect）刷新使用者的畫面。
