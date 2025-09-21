import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
import os

# Create tables
Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Streamlit config
st.set_page_config(page_title="Dating Site", page_icon="💖", layout="wide")

# Sidebar menu
st.sidebar.title("💖 Dating Site")
menu = ["🏠 Home", "📝 Create Profile", "💑 Matches"]
choice = st.sidebar.radio("Navigate", menu)

# Ensure folder for pictures
os.makedirs("profile_pics", exist_ok=True)

# --- HOME ---
if choice == "🏠 Home":
    st.title("💘 Welcome to LoveConnect")
    st.markdown("Find your perfect match. Simple. Fun. Instant 💖")
    st.image("https://cdn-icons-png.flaticon.com/512/210/210545.png", width=200)

    db: Session = next(get_db())
    total_users = db.query(User).count()
    st.metric("Total Users", total_users)

# --- CREATE PROFILE ---
elif choice == "📝 Create Profile":
    st.header("📝 Create Your Profile")
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
        with col2:
            bio = st.text_area("Bio")
            interests = st.text_input("Interests (comma-separated)")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("💾 Save Profile")

        if submitted:
            pic_path = None
            if profile_pic:
                pic_path = os.path.join("profile_pics", profile_pic.name)
                with open(pic_path, "wb") as f:
                    f.write(profile_pic.getbuffer())

            db: Session = next(get_db())
            new_user = User(
                name=name,
                age=age,
                bio=bio,
                interests=interests,
                profile_pic=pic_path
            )
            db.add(new_user)
            db.commit()
            st.success("🎉 Profile created successfully!")

# --- MATCHES ---
elif choice == "💑 Matches":
    st.header("💑 Browse Matches")

    db: Session = next(get_db())
    users = db.query(User).all()

    # Search and filters
    st.subheader("🔍 Search Filters")
    min_age, max_age = st.slider("Age Range", 18, 100, (20, 40))
    interest_filter = st.text_input("Filter by interest")

    filtered_users = [
        u for u in users
        if min_age <= u.age <= max_age and
           (interest_filter.lower() in u.interests.lower() if interest_filter else True)
    ]

    if filtered_users:
        cols = st.columns(2)
        for i, u in enumerate(filtered_users):
            with cols[i % 2]:
                st.markdown(f"### {u.name}, {u.age}")
                if u.profile_pic and os.path.exists(u.profile_pic):
                    st.image(u.profile_pic, width=200)
                st.write(u.bio)
                st.caption(f"Interests: {u.interests}")
                if st.button(f"❤️ Like {u.name}", key=f"like_{u.id}"):
                    st.success(f"You liked {u.name}!")
                st.markdown("---")
    else:
        st.info("⚠️ No matches found. Try changing your filters.")
