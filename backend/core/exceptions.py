"""
カスタム例外クラス定義
PoC開発のため最小限の実装
"""

class InstagramAPIError(Exception):
    """Instagram API関連のカスタム例外"""
    def __init__(self, message: str, status_code: int = None, error_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.error_data = error_data
        super().__init__(self.message)

class TokenExpiredError(InstagramAPIError):
    """アクセストークン期限切れ"""
    def __init__(self, message: str = "アクセストークンの有効期限が切れています"):
        super().__init__(message, status_code=401)

class RateLimitError(InstagramAPIError):
    """APIレート制限"""
    def __init__(self, message: str = "API呼び出し制限に達しました。しばらく待ってから再試行してください"):
        super().__init__(message, status_code=429)

class DatabaseConnectionError(Exception):
    """データベース接続エラー"""
    def __init__(self, message: str = "データベースに接続できません"):
        self.message = message
        super().__init__(self.message)