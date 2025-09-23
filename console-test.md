# ブラウザのConsoleでAPIテストする方法

## 手順

1. **ブラウザでサイトを開く**
   - https://instagram-analysis-5-asfy.vercel.app にアクセス
   - ログインする

2. **Developer Tools（開発者ツール）を開く**
   - Windows: `F12` または `Ctrl + Shift + I`
   - Mac: `Command + Option + I`

3. **Consoleタブをクリック**
   - 画面下部に黒い画面が出る
   - `Console`と書かれたタブを選択

4. **以下のコードをコピー&ペースト**
   ```javascript
   fetch('https://instagram-analysis-5-production.up.railway.app/accounts/', {
     headers: { 
       'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
       'Content-Type': 'application/json'
     }
   })
   .then(response => {
     console.log('Status:', response.status);
     return response.json();
   })
   .then(data => {
     console.log('Accounts:', data);
   })
   .catch(error => {
     console.error('Error:', error);
   });
   ```

5. **Enterキーを押す**
   - 結果がConsoleに表示される

## 結果の見方
- `Status: 200` + `Accounts: [...]` → 成功
- `Status: 401` → 認証エラー
- `Status: 200` + `Accounts: []` → データなし

---

## 投稿データテスト（日付範囲を変更）

アカウントデータが確認できたら、投稿データを確認：

```javascript
// 投稿データテスト（正しい日付形式）
fetch('https://instagram-analysis-5-production.up.railway.app/analytics/posts/17841416839641597?start_date=2025-08-01&end_date=2025-08-31', {
  headers: { 
    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('Posts Status:', response.status);
  return response.json();
})
.then(data => {
  console.log('Posts Data:', data);
})
.catch(error => {
  console.error('Posts Error:', error);
});
```

### 投稿データ結果の見方
- `Posts Status: 200` + `Posts Data: [...]` → 投稿データ存在
- `Posts Status: 200` + `Posts Data: []` → 投稿データなし（日付範囲を変更してテスト）
- `Posts Status: 401` → 認証エラー

---

## 詳細デバッグ（ローカルでは表示されるが本番で空の場合）

### 1. 現在のユーザー確認
```javascript
// 現在のユーザー情報を確認
fetch('https://instagram-analysis-5-production.up.railway.app/auth/me', {
  headers: { 
    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(user => {
  console.log('Current User:', user);
});
```

### 2. 詳細なAPIレスポンス確認
```javascript
// より詳細なAPIレスポンス確認
fetch('https://instagram-analysis-5-production.up.railway.app/analytics/posts/17841416839641597?start_date=2025-08-01&end_date=2025-08-31', {
  headers: { 
    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('Full Response:', response);
  console.log('Headers:', response.headers);
  return response.text(); // JSONではなくテキストで取得
})
.then(text => {
  console.log('Raw Response:', text);
  try {
    const data = JSON.parse(text);
    console.log('Parsed Data:', data);
  } catch(e) {
    console.log('Parse Error:', e);
  }
});
```

### デバッグ結果の確認ポイント
- **Current User**: ローカルと同じユーザーIDか？
- **Raw Response**: 空配列`[]`以外の情報があるか？
- **Railway Logs**: この時間のAPIアクセスログを確認