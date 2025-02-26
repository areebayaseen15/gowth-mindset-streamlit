import streamlit as st
import pandas as pd
# import plotly.express as px
import random
import time


# 🌟 Session State for User Authentication & Progress
if "user" not in st.session_state:
    st.session_state.user = None
if "users" not in st.session_state:
    st.session_state.users = {}
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}
if "streaks" not in st.session_state:
    st.session_state.streaks = {}
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# 🎯 Growth Mindset Challenges
challenges = [
    "Aaj ek new skill seekho aur note karo.",
    "Ek mistake identify karo aur us se seekhne ka tareeqa likho.",
    "Ek positive mindset wali baat kisi aur se share karo.",
    "Ek naye cheez par research karo aur seekho.",
    "Apni koi ek weakness identify karo aur usko improve karne ka plan banao."
]

# 🌟 Motivational Quotes
quotes = [
    "Your only limit is your mind!",
    "Success is not final, failure is not fatal—it’s the courage to continue that counts.",
    "Mistakes are proof that you are trying.",
    "Hardships often prepare ordinary people for an extraordinary destiny."
]

# 🎨 Sidebar Title & Welcome Message
st.sidebar.markdown("## 🎯 Growth Mindset Hub")
st.sidebar.write("🌱 **Stay motivated & track your progress!**")



# 🚀 UI
st.title(f"🌱 Welcome {st.session_state.user if st.session_state.user else ''} to the Growth Mindset Challenge App")
st.write("Current Theme:", st.session_state.theme)


# 🔐 User Authentication
st.sidebar.header("🔐 Login / Sign Up")
if st.session_state.user:
    st.sidebar.success(f"✅ Welcome, {st.session_state.user}!")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
else:
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")
    if st.sidebar.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.user = username
            st.experimental_rerun()
        else:
            st.sidebar.error("❌ Invalid credentials! Try again.")
    if st.sidebar.button("Sign Up"):
        if username and password:
            if username in st.session_state.users:
                st.sidebar.error("🚫 Username already exists! Choose another.")
            else:
                st.session_state.users[username] = {"password": password, "completed_challenges": 0, "streak": 0}
                st.sidebar.success("✅ Account created! Please log in.")
        else:
            st.sidebar.error("⚠️ Please enter a username & password.")


# 🎨 Theme Toggle in Sidebar
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])
st.session_state.theme = theme.lower()

# 🌙 Apply Dark Mode Styling
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
            body, .stApp {
                background-color: #121212;
                color: white;
            }
            .stSidebar, .stTextInput>div>div>input, .stTextArea>div>textarea {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #555;
            }
            .stButton>button {
                background-color: #333;
                color: white;
                border: 1px solid #444;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #555;
                border: 1px solid #888;
            }
            /* Reflection Journal Background Fix */
            .stTextArea>div {
                background-color: #1E1E1E !important;
                color: white !important;
            }
            /* Leaderboard Chart Fix */
            .stDataFrame { 
                background-color: #2C2F33 !important;
                color: white !important;
            }    

        </style>
        """,
        unsafe_allow_html=True
    )

# 📊 Progress Poll
st.sidebar.header("📊 Your Progress Poll")
st.sidebar.write("How's your growth journey?")
poll_choice = st.sidebar.radio("Choose One:", ["🔥 Going Great!", "📚 Need More Practice", "🚀 Just Started"])

if st.sidebar.button("✅ Submit Poll"):
    st.sidebar.success(f"👏 Great choice! Keep going strong. 🚀")

# 🎯 Daily Challenge with Timer
daily_challenge = random.choice(challenges)
st.subheader("🎯 Your Daily Challenge")
st.write(f"👉 **{daily_challenge}**")

time_left = st.slider("Set Challenge Timer (minutes):", 1, 60, 10)
if st.button("Start Timer"):
    with st.empty():
        for seconds in range(time_left * 60, 0, -1):
            mins, secs = divmod(seconds, 60)
            st.write(f"⏳ Time Remaining: {mins}:{secs}")
            time.sleep(1)
        st.success("⏰ Time's up! Complete your challenge now!")

# 📝 Reflection Journal
st.subheader("📖 Reflection Journal")
journal_input = st.text_area("Aaj ka learning yahan likhein:")
if st.button("Save Reflection"):
    if journal_input and st.session_state.user:
        st.success("✅ Reflection saved successfully!")
    else:
        st.warning("⚠️ Please log in and write something before saving.")


st.subheader("📊 Your Progress")
if st.session_state.user:
    user_data = st.session_state.users[st.session_state.user]
    progress = user_data["completed_challenges"]
    st.write(f"✅ Challenges Completed: **{progress}**")
    st.progress(min(progress / 10, 1)) 

    if st.button("Mark Challenge as Completed"):
        user_data["completed_challenges"] += 1
        user_data["streak"] += 1
        st.session_state.leaderboard[st.session_state.user] = user_data["completed_challenges"]
        st.success("🎉 Great job! Challenge marked as completed.")

    if user_data["streak"] >= 5:
        st.balloons()
        st.success("🔥 Streak Bonus! You've completed 5 challenges in a row!")
else:
    st.warning("⚠️ Please log in to track your progress.")




# 🏆 Leaderboard (Interactive Chart)
st.header("🏅 Your Performance")
if st.session_state.leaderboard:
    sorted_leaderboard = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)
    st.write(" Your Performance")
    for i, (user, score) in enumerate(sorted_leaderboard[:5], 1):
        st.write(f"**{i}. {user}** - {score} Challenges Completed")
else:
    st.warning("⚠️ No leaderboard data yet. Start completing challenges!")

# Dummy Data 
data = {
    "User": ["Amna", "Ali", "Fatima", "Hassan", "Sara"],
    "Challenges Completed": [10, 8, 6, 5, 4]
}
df = pd.DataFrame(data)
# 🏆 Display Leaderboard Table
st.header("🏆Leaderboard")
st.write(df)  


# 🧠 Mind Games Section
st.sidebar.header("🧩 Mind Games")
game_choice = st.sidebar.radio("Choose a game:", ["Solve a Puzzle", "MCQs", "Riddles"])
if game_choice == "Solve a Puzzle":
    st.subheader("🧩 Solve This Puzzle:")
    st.write("Rearrange the letters: 'COTARE' to form a meaningful word.")
    answer = st.text_input("Your Answer:")
    if st.button("Submit Answer"):
        if answer.lower() == "react":
            st.success("🎉 Correct! React is the right answer.")
        else:
            st.error("❌ Incorrect! Try Again.")

elif game_choice == "MCQs":
    st.subheader("📚 Answer This MCQ:")
    question = "Which of the following is a JavaScript framework?"
    options = ["Django", "Flask", "React", "Laravel"]
    choice = st.radio("Choose One:", options)
    if st.button("Submit MCQ"):
        if choice == "React":
            st.success("🎉 Correct Answer!")
        else:
            st.error("❌ Incorrect! The right answer is React.")

elif game_choice == "Riddles":
    st.subheader("🤔 Solve This Riddle:")
    st.write("I speak without a mouth and hear without ears. I have nobody, but I come alive with the wind. What am I?")
    riddle_answer = st.text_input("Your Answer:")
    if st.button("Check Answer"):
        if riddle_answer.lower() == "echo":
            st.success("🎉 Correct! The answer is 'Echo'.")
        else:
            st.error("❌ Try Again!")


# 🔥 Motivational Quotes
st.subheader("💡 Today's Motivational Quote")
quote = random.choice(quotes)
st.write(f"📢 **{quote}**")
if st.button("🔄 New Quote"):
    st.rerun()


# 🌟 Footer
st.markdown("---")
st.write("🚀 **Keep Growing & Learning Every Day!** 🚀")
