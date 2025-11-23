import streamlit as st
import pywhatkit
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
# For GEMINI API KEY: 
# Go to Google AI Studio
# Sign in with your Google account.
# Click "Get API Key" in the top-right corner.
# Accept the terms and conditions.
# Copy your API key.
def healthcare_chatbot(user_input):
    if "symptom" in user_input:
        return "Please consult a doctor for accurate advice."
    elif "appointment" in user_input:
        return "Would you like to schedule an appointment with the doctor?"
    elif "medication" in user_input:
        return "It's important to take prescribed medicines regularly."
    else:
        response = model.generate_content(user_input)
        return response.text

def set_reminder():
    add_reminder = st.text_input("Do you want to add a reminder? (Y/N)").strip().upper()

    if add_reminder == "Y":

        mobile_number = st.text_input("Enter the mobile number (with country code, e.g., +91xxxxxxxxxx):")


        note = st.text_area("Enter your note (optional):")


        time_input = st.text_input("Enter Time in HH:MM format:")
        try:
            hour, minute = map(int, time_input.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                st.error("Invalid time. Please enter a valid time in 24-hour format.")
                return
        except ValueError:
            st.error("Invalid format. Please enter time in HH:MM format.")
            return


        if st.button("Submit Reminder"):

            message = f"Take medicines. Note: {note}" if note else "Take medicines"
            pywhatkit.sendwhatmsg(mobile_number, message, hour, minute)
            st.success(f"Reminder set for {hour:02d}:{minute:02d} with message: {message}")

def main():
    st.title("Healthcare Assistant Chatbot")

    user_input = st.text_input("How can I assist you today?")
    if st.button("Submit Query"):
        if user_input:
            st.write("User:", user_input)
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
            st.write("Healthcare Assistant:", response)
        else:
            st.write("Please enter a message to get a response.")


    set_reminder()


main()