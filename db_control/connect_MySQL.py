from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
import tempfile

# 環境変数の読み込み
base_path = Path(__file__).parents[1]
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)
# load_dotenv()

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))  # パスワードを URL エンコード
# DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス（DigiCert のルート証明書）
# SSL_CA_PATH = str(base_path / 'DigiCertGlobalRootCA.crt.pem')  # 証明書のパスを指定
# SSL_CA_PATH = "C:/Users/nomur/POSApp_Nomurin/backend/DigiCertGlobalRootCA.crt.pem"

# SSL証明書の取得
SSL_CA_CERT = os.getenv("SSL_CA_CERT")
if not SSL_CA_CERT:
    raise ValueError(":x: SSL_CA_CERT が設定されていません！")

# # SSL証明書の一時ファイル作成
def create_ssl_cert_tempfile():
    pem_content = SSL_CA_CERT.replace("\\n", "\n").replace("\\", "")
    temp_pem = tempfile.NamedTemporaryFile(delete=False, suffix=".pem", mode="w")
    temp_pem.write(pem_content)
    temp_pem.close()
    return temp_pem.name

SSL_CA_PATH = create_ssl_cert_tempfile()

# MySQLのURL構築（特殊文字をエンコード）
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"ssl": {"ca": SSL_CA_PATH}}
)
