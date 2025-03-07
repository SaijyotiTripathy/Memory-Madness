import streamlit as st
import math
from streamlit_extras.let_it_rain import rain
import random
import time



def generate_num_map(num):
    values = [i for i in range(1, num // 2 + 1) for _ in range(2)]
    random.shuffle(values)
    return {f"A{i}": values[i] for i in range(num)}

def generate_emoji_map(num):
    emojis = [ "🍌", "🍇", "🍉", "🍍", "🥝", "🍓", "🍒", "🥑", "🥕", "✨", "🌸", "💫", "🌿", "🍂", "💎",  "🎊", "🌈", "💐", "🌞", "🍒", "🦄", "💜", "🎶", "💡", "🕊", "🎠", "🕯", "🪄", "🧿", "📜", "🔮", "🎭", "💌", "📖", "🎇", "💍", "🎵", "🪞", "💙", "🌠" ]
    print(len(emojis))

    selected_emojis = random.sample(emojis, num // 2) * 2
    random.shuffle(selected_emojis)
    return {f"A{i}": selected_emojis[i] for i in range(num)}


st.title("**Memory Madness 🎮🧠** ")
st.write("""
Welcome to **Memory Madness**, the ultimate brain-boosting challenge! 🧠✨ Test your memory, focus, and speed as you match hidden pairs of emojis in this fun and engaging game. Whether you're just warming up or aiming for **Galaxy Brain status 🛸**, there's a level for everyone!  

🔹 **How to Play:**  
1️⃣ Click on a button to reveal the hidden emoji.  
2️⃣ Click on another button to find its match.  
3️⃣ If the emojis match, the buttons **become unclickable!** 🎉  
4️⃣ If they don’t, they hide back—so **remember their locations!** 🔄  
5️⃣ Clear the board as fast as possible to win! ⏳🏆  

🎯 **Difficulty Levels:**  
1. **"Goldfish Memory 🐠"** – Perfect for those who forget what they had for breakfast.  
2. **"Brain in Training 🏋️‍♂️"** – Your neurons are stretching… but still need a warm-up.  
3. **"Einstein's Intern 🧠💡"** – You’re getting smart, but you still Google things.  
4. **"Big Brain Mode 🚀"** – Your memory is so sharp, even your browser history is jealous.  
5. **"Galaxy Brain 🛸"** – You remember things before they even happen. Are you from the future?  

💡 Play, train your brain, and have fun with **Memory Madness**! Can you match them all in least time? 🚀🔥  
""")

st.divider()

def run(num=4):
    rows = math.isqrt(num)
    cols = math.ceil(num / rows)
    button_labels = [[f"A{r * cols + c}" for c in range(cols) if r * cols + c < num] for r in range(rows)]
    
    if "game_won" not in st.session_state:
        st.session_state.game_won = False
    if "prev_selected_button" not in st.session_state:
        st.session_state.prev_selected_button = None
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0
    if "disabled_buttons" not in st.session_state:
        st.session_state.disabled_buttons = []
    if "num_map" not in st.session_state:
        st.session_state.num_map = generate_emoji_map(num)
    if "timer" not in st.session_state:
        st.session_state.timer = time.time()

    selected_button = None
    columns = st.columns(cols)
    
    for i in range(rows):
        for j in range(len(button_labels[i])):
            btn_label = button_labels[i][j]
            if btn_label in st.session_state.disabled_buttons:
                columns[j].button("❔", key=f"{i}_{j}", disabled=True)
            else:
                if columns[j].button("❔", key=f"{i}_{j}"):
                    selected_button = btn_label
                    st.write(f"**Selected:** {st.session_state.num_map[selected_button]}")
    
    if selected_button:
        if st.session_state.prev_selected_button is None:
            st.session_state.prev_selected_button = selected_button
        else:
            if selected_button == st.session_state.prev_selected_button:
                st.warning("Please select a different button.")
            else:
                if st.session_state.num_map[st.session_state.prev_selected_button] == st.session_state.num_map[selected_button]:
                    st.success("🎉 It's a Match!")
                    st.session_state.disabled_buttons.extend([st.session_state.prev_selected_button, selected_button])
                    if len(st.session_state.disabled_buttons) == num:
                        st.session_state.timer = time.time() - st.session_state.timer
                        st.session_state.game_won = True
                        st.success(f"🎉 You won in {st.session_state.timer:.2f} seconds! ⏳")
                        rain(emoji="🎈", font_size=54, falling_speed=4, animation_length=50)
                else:
                    st.warning("❌ Not a match! Try again.")
                st.session_state.prev_selected_button = None

st.write("⚠️ **Refresh the page before selecting a different level.**  ")
levels_map = {"Goldfish Memory 🐠": 4, "Brain in Training 🏋️‍♂️": 10, "Einstein's Intern 🧠💡": 16, "Big Brain Mode 🚀":26, "Galaxy Brain 🛸":40}
selection = st.pills("Select your level of difficulty 😈", levels_map, selection_mode="single")
st.markdown(f"Your selected level: {selection}.")

if selection:
    num= levels_map[selection]
    run(num)
    if st.session_state.get("game_won", False):
        st.write("Thanks for playing! 😊")
