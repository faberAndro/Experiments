# NLP-studio_2
This python script uses as a basis a text file: a transcript from "The Matrix" movie, downloadable at the URL: http://www.scifiscripts.com/scripts/matrix_97_draft.txt. 

Running the file will perform the following operations of natural language processing:
- extracting and normalizing keywords (deleting stop words, punctuation, etc.)
- analyzing word frequencies
- extracting proper names
- summarizing the transcript
- assigning additional unknown text to one of the characters

NOTE: this code uses a heavy file; a Google GloVe vector. It loads the file from internet. This could take one minute.
To be able to run the code, be sure to have imported all the necessary modules.
Only the internal NLTK libraries will be downloaded automatically.
