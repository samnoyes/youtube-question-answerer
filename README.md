# GPT-Powered Youtube Question Answerer
Provide a Youtube link, ask questions, and get answers. Simple as that.

Uses LangChain, GPT 3.5 for the LLM, and Chroma for the vector database.

## Usage

1. Ensure you have Python installed

2. Clone this repository to your local machine using the following command:

`git clone https://github.com/samnoyes/youtube-question-answerer.git`

3. Install the required dependencies. In terminal: navigate to the project directory and run the following command:
`pip install -r requirements.txt` (pip3 if you are using python3)

4. In the root directory of your project, create a `.env` file and add the following line to it, replacing `YOUR_OPENAI_API_KEY` with your actual API key:

`OPENAI_API_KEY=YOUR_OPENAI_API_KEY`

5. Transcribe the Youtube video and load into the vector store with the following command (choose whatever name you like for the vector store): `python3 script.py <Youtube link> <Name of vector store>`

Example: `python3 script.py https://www.youtube.com/watch?v=kVeOpcw4GWY create_react_app`

This may take a few minutes.

6. Ask questions about the video: `python3 answer_question.py <Name of vector store> <Question text>`

Example: `python3 answer_question.py create_react_app "What version of node do I need?"`

Result, as stated in the video: `You need a modern version of Node installed on your computer, ideally version 5.2 or above.`

## Limitations

We split the transcription into 1000-token chunks and only refer to the 4 most relevant chunks (k=4 is baked into Langchain's vector DB QA retrieval), so if the question is too broad it may struggle to answer because it won't be able to see all of the available information. Try to rephrase the question to be more specific if you run into this issue.
