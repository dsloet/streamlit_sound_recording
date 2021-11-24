import csv
import streamlit as st
from recording import Recorder

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# TODO:
# input_sentences = ["Wij zijn beschikbaar op", "Zin twee."]

with open("input.csv") as f:
    input_sentences = [row.strip() for row in f]

recorder = Recorder()


def main():
    if "count" not in st.session_state:
        st.session_state.count = 0

    if "sentence" not in st.session_state:
        st.session_state.sentence = ""
    if "sentence_list" not in st.session_state:
        st.session_state.sentence_list = []
    if "filename_list" not in st.session_state:
        st.session_state.filename_list = []

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
        st.session_state.sentence_list.append(st.session_state.sentence)
        with st.spinner(text="In progress..."):
            filename = recorder.record_to_file(counter=st.session_state.count - 1)

            st.session_state.filename_list.append(filename)

    save = st.button("Save")
    if save:
        logger.info(st.session_state.filename_list)
        logger.info(st.session_state.sentence_list)
        results = {
            "filename": st.session_state.filename_list,
            "sentence": st.session_state.sentence_list,
        }
        logger.info(results)
        try:
            with open("output.csv", "w") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(results.keys())
                writer.writerows(zip(*results.values()))
        except IOError:
            print("I/O error")


if __name__ == "__main__":
    main()
