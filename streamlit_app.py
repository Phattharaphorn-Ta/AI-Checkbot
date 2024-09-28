import streamlit as st
import google.generativeai as genai
 
st.title("🏞️ Professional Tour Guide - Thailand Travel Advisor")
st.subheader("Conversation")
 
# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")
 
# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
 
# Initialize session state for storing chat history and prompt history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list
 
if "prompt_chain" not in st.session_state:
    st.session_state.prompt_chain = "I am a professional tour guide. I will first ask you what type of place or attraction you're interested in, such as beaches, mountains, temples, or shopping. "
    "Then, I will provide recommendations for famous locations in Thailand based on your preferences. "
    "Additionally, I will give you advice on how to prepare for your trip, including what to pack, necessary travel documents, budgeting tips, and estimated trip costs for different types of vacations in Thailand."
 
# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)
 
# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)
   
    # Append the new question to the prompt chain
    st.session_state.prompt_chain += f"\nCustomer: {user_input}"
   
    # Combine the predefined prompt chain with the current user input
    full_input = st.session_state.prompt_chain
   
    # Use Gemini AI to generate a bot response
    if model:
        try:
            response = model.generate_content(full_input)
            bot_response = response.text
           
            # Append bot response to the chat history and update the prompt chain
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
           
            # Update the prompt chain with the bot's response
            st.session_state.prompt_chain += f"\nAssistant: {bot_response}"
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")

