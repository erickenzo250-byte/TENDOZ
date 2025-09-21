import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

st.set_page_config(page_title="Dating Site", page_icon="💖")

st.title("💖 Dating Site")

menu = ["Home", "Create Profile", "Matches"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to the Dating Site!")
    st.write("Find your perfect match and connect instantly.")

elif choice == "Create Profile":
    st.subheader("Create Your Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    bio = st.text_area("Bio")
    interests = st.text_input("Interests")

    if st.button("Save Profile"):
        db: Session = next(get_db())
        new_user = User(name=name, age=age, bio=bio, interests=interests)
        db.add(new_user)
        db.commit()
        st.success("Profile created successfully!")

elif choice == "Matches":
    st.subheader("Browse Matches")
    db: Session = next(get_db())
    users = db.query(User).all()
    if users:
        for u in users:
            with st.container():
                st.markdown(f"### {u.name}, {u.age}")
                st.write(u.bio)
                st.caption(f"Interests: {u.interests}")
                st.markdown("---")
    else:
        st.info("No matches found yet. Create a profile!")
