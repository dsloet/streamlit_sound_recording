import streamlit as st
from src.sound import sound


input_sentences = ["Zin 1.", "Zin twee."]


def record_button():
    sound.record()


def main():
    if "count" not in st.session_state:
        st.session_state.count = 0
    title = "Stemgeluid recorder"
    st.title(title)
    st.caption("Klik 'Nieuwe zin' voor een nieuwe zin.")
    sent = st.button("Nieuwe zin")

    if sent:
        try:
            st.metric("Zin:", input_sentences[st.session_state.count])
            st.session_state.count += 1
        except IndexError:
            st.write("Einde van de beschikbare zinnen.")

    record = st.button("Start/Stop")
    if record:
        with st.spinner("Neemt op"):
            record_button()


if __name__ == "__main__":
    main()
