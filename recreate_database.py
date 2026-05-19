"""
Database'i yeniden oluştur - Yeni TaskComparison tablosu eklendi
"""
from database.database import engine, Base
from database.models import *

print("🗄️  Database yeniden oluşturuluyor...")
print("⚠️  Eski tablolar silinecek!")

# Tüm tabloları sil
Base.metadata.drop_all(engine)
print("✅ Eski tablolar silindi")

# Yeni tabloları oluştur
Base.metadata.create_all(engine)
print("✅ Yeni tablolar oluşturuldu")

print("\n📊 Oluşturulan tablolar:")
for table_name in Base.metadata.tables.keys():
    print(f"  - {table_name}")

print("\n✅ Database hazır!")
