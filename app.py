import streamlit as st
from recording import Recorder

# TODO:
input_sentences = ["Wij zijn beschikbaar op", "Zin twee."]

recorder = Recorder()


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
            st.session_state.sentence = input_sentences[st.session_state.count]
            sentence.text(st.session_state.sentence)
            st.session_state.count += 1
        except IndexError:
            sentence.text("Einde van de beschikbare zinnen.")

    record = st.button("Start")
    if record:
        sentence.text(st.session_state.sentence)
        with st.spinner(text="In progress..."):
            recorder.record_to_file(counter=st.session_state.count - 1)


if __name__ == "__main__":
    main()
