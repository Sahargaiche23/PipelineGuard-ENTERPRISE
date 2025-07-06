#!/usr/bin/env python3
from database import SessionLocal
from models import User
from passlib.context import CryptContext

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(username, password):
    db = SessionLocal()
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.username == username).first()
        
        if existing_user:
            print(f"✅ Utilisateur '{username}' existe déjà (ID: {existing_user.id})")
            return existing_user
        
        # Créer le nouvel utilisateur
        print(f"🔧 Création de l'utilisateur '{username}'...")
        hashed_password = get_password_hash(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ Utilisateur '{username}' créé avec succès (ID: {new_user.id})")
        return new_user
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n👥 Utilisateurs dans la base de données ({len(users)}):")
        for user in users:
            print(f"  - Username: {user.username}, ID: {user.id}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des utilisateurs: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Créer l'utilisateur Hibaaa
    create_user("Hibaaa", "Hibaaa")
    
    # Lister tous les utilisateurs
    list_users()
