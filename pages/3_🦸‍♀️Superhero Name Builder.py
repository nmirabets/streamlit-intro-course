import streamlit as st
import random

st.title("What's Your Superhero Name? 🦸‍♂️🦸‍♀️")

# Inputs for superhero name
favorite_color = st.text_input("What's your favorite color?", placeholder="Green")
favorite_animal = st.text_input("What's your favorite animal?", placeholder="Tiger")
lucky_number = st.number_input("Enter your lucky number:", min_value=1, step=1, value=7)

# Dropdown for superpower
superpower = st.selectbox("Choose your superpower:", 
                          ["Flying", "Invisibility", "Super Strength", "Mind Control", "Time Travel"])

# Generate superhero name on button click
if st.button("Generate My Superhero Name"):
    superhero_name = f"{favorite_color} {favorite_animal} of {lucky_number}"
    st.header(f"🦸 Your Superhero Name: {superhero_name}")
    st.write(f"🌟 Superpower: {superpower}")
    
    # Display a motto
    st.subheader("Your Superhero Motto:")
    st.write(f'"With great power comes great {superpower.lower()}!"')

# Bonus: Random catchphrase generator
if st.button("Generate Random Catchphrase"):
    catchphrases = [
        "Up, up, and away!",
        "Justice is served!",
        "Evil never rests, and neither do I!",
        "For truth, justice, and the [Your Name] way!",
        "The night is my ally!"
    ]
    st.write(f"Catchphrase: {random.choice(catchphrases)}")
