import streamlit as st

# Define the topics for the poll
topics = ["Topic 1: The effect of 5g towers on pigeons", "Topic 2: Mango production decline", "Topic 3"]

# Initialize votes for each topic
votes = {topic: 0 for topic in topics}

# Function to display the poll and handle user votes
def conduct_poll():
    st.title("Poll")

    selected_topic = st.radio("Choose a topic to vote for:", topics)

    if st.button("Vote"):
        votes[selected_topic] += 1
        st.success("Vote recorded!")

    st.subheader("Current Results:")
    for topic, vote_count in votes.items():
        st.write(f"{topic}: {vote_count} votes")

# Run the app
if __name__ == "__main__":
    conduct_poll()
