# 資料庫設計：食譜管理系統

## 資料表：recipes
| 欄位名稱 | 資料型態 | 屬性 | 說明 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, Auto-increment | 唯一識別碼 |
| title | VARCHAR(100) | Not Null | 食譜名稱 |
| ingredients | TEXT | Not Null | 食材清單 |
| instructions | TEXT | Not Null | 烹飪步驟 |
| created_at | DATETIME | Default: CURRENT_TIMESTAMP | 建立日期 |
