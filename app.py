from os import write
import streamlit as st
from src.sound import sound
from settings import DURATION


input_sentences = ["Wij zijn beschikbaar op", "Zin twee."]


def record_button(filename):
    sound.record(filename)


def main():
    if "count" not in st.session_state:
        st.session_state.count = 0

    if "sentence" not in st.session_state:
        st.session_state.sentence = ""

    title = "Stemgeluid recorder"
    st.title(title)
    st.caption("Klik 'Nieuwe zin' voor een nieuwe zin.")
    sentence = st.empty()

    sent = st.button("Nieuwe zin")

    if sent:
        try:
            # st.metric("Zin:", input_sentences[st.session_state.count])
            # st.text(input_sentences[st.session_state.count])
            st.session_state.sentence = input_sentences[st.session_state.count]
            sentence.text(st.session_state.sentence)
            st.session_state.count += 1
        except IndexError:
            sentence.text("Einde van de beschikbare zinnen.")

    record = st.button("Start/Stop")
    if record:
        sentence.text(st.session_state.sentence)
        with st.spinner(f"Neemt op voor {DURATION} seconden"):
            record_button(filename=f"DS_TEST_{st.session_state.count-1}.wav")


if __name__ == "__main__":
    main()
