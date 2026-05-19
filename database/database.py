"""
Database connection and session management
SQLite (local/Streamlit Cloud) veya PostgreSQL (production) — D1.

DATABASE_URL env değişkeni veya Streamlit secrets ile kontrol edilir.
Ayarlanmazsa SQLite varsayılan olarak kullanılır.

Streamlit Cloud için secrets.toml:
    DATABASE_URL = "postgresql://user:pass@host:5432/dbname"

Local .env:
    DATABASE_URL=postgresql://user:pass@localhost/pidl_research
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
import os


def _build_database_url() -> tuple[str, dict]:
    """
    DATABASE_URL'yi çözümle; Streamlit secrets → env → SQLite sıralamasıyla.
    Returns: (url, engine_kwargs)
    """
    url = None

    # 1. Streamlit secrets (Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "DATABASE_URL" in st.secrets:
            url = st.secrets["DATABASE_URL"]
    except Exception:
        pass

    # 2. Environment variable (local .env veya heroku/railway)
    if not url:
        url = os.getenv("DATABASE_URL")

    # 3. Fallback: SQLite
    if not url:
        db_path = os.path.join(os.path.dirname(__file__), "research_data.db")
        url = f"sqlite:///{db_path}"

    # SQLite için check_same_thread gerekli; PostgreSQL için değil
    if url.startswith("sqlite"):
        kwargs = {"connect_args": {"check_same_thread": False}}
    else:
        # PostgreSQL: connection pooling
        kwargs = {"pool_pre_ping": True, "pool_size": 5, "max_overflow": 10}

    return url, kwargs


DATABASE_URL, _engine_kwargs = _build_database_url()

# SQLite ise DB_PATH'i loglamak için
DB_PATH = DATABASE_URL.replace("sqlite:///", "") if DATABASE_URL.startswith("sqlite") else DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL, echo=False, **_engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Thread-safe session
SessionScoped = scoped_session(SessionLocal)


def init_db():
    """
    Veritabanını başlat - tüm tabloları oluştur.
    SQLite veya PostgreSQL — DATABASE_URL'ye göre otomatik seçilir (D1).
    """
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DB_PATH}")


def get_session():
    """
    Yeni bir database session döndür

    Kullanım:
        session = get_session()
        try:
            # Database işlemleri
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    """
    return SessionLocal()


def drop_all_tables():
    """
    UYARI: Tüm tabloları sil (sadece development için)
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped!")


def reset_database():
    """
    Veritabanını sıfırla (drop + create)
    """
    drop_all_tables()
    init_db()
    print("🔄 Database reset complete!")


# Context manager for sessions
class DatabaseSession:
    """
    Context manager for database sessions

    Kullanım:
        with DatabaseSession() as session:
            participant = Participant(uuid="...")
            session.add(participant)
            session.commit()
    """

    def __enter__(self):
        self.session = get_session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()


if __name__ == "__main__":
    # Test: Veritabanını başlat
    init_db()

    # Test: Tablo sayısını göster
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📊 Created {len(tables)} tables:")
    for table in tables:
        print(f"   - {table}")
