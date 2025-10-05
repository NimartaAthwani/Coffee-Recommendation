import streamlit as st
import sqlite3

# ---------------- Database Setup ---------------- #
def init_db():
    conn = sqlite3.connect("coffee_data.db")
    c = conn.cursor()

    # Coffee Options Table
    c.execute('''CREATE TABLE IF NOT EXISTS coffee_options (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    flavor TEXT,
                    temperature TEXT,
                    caffeine TEXT
                )''')

    # User History Table
    c.execute('''CREATE TABLE IF NOT EXISTS user_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flavor TEXT,
                    temperature TEXT,
                    caffeine TEXT,
                    suggestion TEXT
                )''')

    # Always refresh options (delete old and insert new)
    c.execute("DELETE FROM coffee_options")

    coffee_list = [
        # SWEET
        ("Hot Mocha", "Sweet", "Hot", "Medium"),
        ("Caramel Latte", "Sweet", "Hot", "Light"),
        ("Hot Chocolate Espresso", "Sweet", "Hot", "Strong"),
        ("Iced Mocha", "Sweet", "Iced", "Medium"),
        ("Frappuccino", "Sweet", "Iced", "Light"),
        ("Iced Caramel Macchiato", "Sweet", "Iced", "Strong"),

        # MILD
        ("Hot Latte", "Mild", "Hot", "Medium"),
        ("Cappuccino", "Mild", "Hot", "Light"),
        ("Flat White", "Mild", "Hot", "Strong"),
        ("Iced Latte", "Mild", "Iced", "Medium"),
        ("Iced Cappuccino", "Mild", "Iced", "Light"),
        ("Iced Flat White", "Mild", "Iced", "Strong"),

        # BITTER
        ("Espresso", "Bitter", "Hot", "Strong"),
        ("Americano", "Bitter", "Hot", "Medium"),
        ("Ristretto", "Bitter", "Hot", "Light"),
        ("Iced Americano", "Bitter", "Iced", "Medium"),
        ("Iced Americano (Light)", "Bitter", "Iced", "Light"),
        ("Iced Espresso Shot", "Bitter", "Iced", "Strong"),

        # SMOOTH
        ("Cafe au Lait", "Smooth", "Hot", "Medium"),
        ("Hot Milk Coffee", "Smooth", "Hot", "Light"),
        ("Cafe Breve", "Smooth", "Hot", "Strong"),
        ("Cold Brew", "Smooth", "Iced", "Strong"),
        ("Iced Cafe au Lait", "Smooth", "Iced", "Medium"),
        ("Iced Milk Coffee", "Smooth", "Iced", "Light"),
    ]
    c.executemany("INSERT INTO coffee_options (name, flavor, temperature, caffeine) VALUES (?, ?, ?, ?)", coffee_list)

    conn.commit()
    conn.close()

# Function to save user choice
def save_user_choice(flavor, temperature, caffeine, suggestion):
    conn = sqlite3.connect("coffee_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO user_history (flavor, temperature, caffeine, suggestion) VALUES (?, ?, ?, ?)",
              (flavor, temperature, caffeine, suggestion))
    conn.commit()
    conn.close()

# Function to recommend coffee
def recommend_coffee(flavor, temperature, caffeine):
    conn = sqlite3.connect("coffee_data.db")
    c = conn.cursor()
    c.execute("SELECT name FROM coffee_options WHERE flavor=? AND temperature=? AND caffeine=?",
              (flavor, temperature, caffeine))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "No exact match found ☹, But how about trying a Latte?"

# ---------------- Streamlit UI ---------------- #
def main():
    st.set_page_config(page_title="Coffee Recommendation Engine ☕", page_icon="☕")
    st.title("☕ Coffee Recommendation")
    st.write("Choose your preferences and get your perfect coffee suggestion!")

    # Form
    with st.form("coffee_form"):
        flavor = st.selectbox("Choose Flavor", ["Sweet", "Mild", "Bitter", "Smooth"])
        temperature = st.radio("Preferred Temperature", ["Hot", "Iced"])
        caffeine = st.selectbox("Caffeine Level", ["Light", "Medium", "Strong"])

        submit = st.form_submit_button("Get Recommendation")

    if submit:
        suggestion = recommend_coffee(flavor, temperature, caffeine)
        st.success(f"✅ Based on your choice, we recommend: **{suggestion}** ☕")

        # Save user choice
        save_user_choice(flavor, temperature, caffeine, suggestion)
        st.info("📌 Your selection has been saved in history.")

   

# ---------------- Run ---------------- #
if __name__ == "__main__":
    init_db()
    main()

