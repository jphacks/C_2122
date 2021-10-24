# User（ユーザー）
- id[int]
- username[string]
- password[string]

# Purpose（目的）
- id[int]
- date[date]
- user_id[int] # userテーブルに依存
- content[string]
- reserved_id[?int] # 予約が完了していない場合はnull
aaaaa
# Reserve（予約）
- id[int]
- date[date]
- purpose_id[int] # purposeテーブルに依存
- purpose_id[int] # purposeテーブルに依存

# Chat（チャット）
- reserve_id[int] # reserveテーブルに依存
- date[date]
- content[string]
- user_id_sender[id] # userテーブルに依存