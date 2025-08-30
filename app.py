import gradio as gr
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser


dir_faiss = "faiss_index"
# Load FAISS
embedding = OpenAIEmbeddings()
db = FAISS.load_local(dir_faiss, embedding, allow_dangerous_deserialization=True)

# Define prompt
system_template = """
You are a professional tennis coach trained. Provide advice to improve the user's tennis skills.
Answer using ONLY the provided context. If the answer is not in the context, say you don't know.
Adjust your answer based on user's level and age.
Provide advice only on the shot user is asking.
Give your answer in 3 points.

Output will be in the following format:

(On the first line, add your comments considering the user's input. Something motivating.
Always mention the user's level, age, shot, and skill.)
1. ...
2. ...
3. ...
(On the last line, add your comments to motivate the user.)
"""


prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "Question:\n{question}\n\nContext:\n{context}")
])

# Retriever
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k":12, "fetch_k":20, "lambda_mult":0.5})

# LLM
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.4)


def get_coaching_advice(level, age, shot, skill, court, comments):
    chain = prompt | llm | StrOutputParser()

    question = (
        f"I want to improve my {shot} and gain more {skill}. "
        f"I usually play on {court} court. My age is {age}. My level is {level}."
    )
    if comments and comments.strip():
        question += f" {comments.strip()}"

    print(question)

    ctx = retriever.invoke(question)
    resp = chain.invoke({"question": question, "context": ctx})

    return resp


# Dropdown options
level_options = ["Beginner", "Intermediate", "Advanced", "Pro"]
age_options = ["10 or younger", "20s", "30s", "40s", "50+"]
shot_options = ["Flat Forehand", "Topspin Forehand", "Slice Forehand", "Two-handed Backhand", "One-handed Backhand",
                "Slice Backhand", "Flat Serve", "Spin Serve", "Kick Serve", "Slice Serve", "Return", "Volley", "Drop shot", "Smash"]
skill_options = ["Power", "Consistency", "Spin", "Control", "Footwork"]
court_options = ["Clay", "Hard", "Grass", "Carpet"]

# Build Gradio app
with gr.Blocks(css=".custom-button { background-color: #1eaa50 !important; color: white !important; font-weight: bold; }") as demo:
    gr.Markdown("## 🎾 AI Tennis Coach 🧑‍🏫🎾 \nAsk your coach for advice to improve your shots! It gives you different advice every time you hit the button.\
                \nThe AI is trained on over 1000 tennis lesson videos.")

    with gr.Row():
        level_dropdown = gr.Dropdown(choices=level_options, label="Your level")
        age_dropdown = gr.Dropdown(choices=age_options, label="Your age")
        shot_dropdown = gr.Dropdown(choices=shot_options, label="Shot to Improve")
        skill_dropdown = gr.Dropdown(choices=skill_options, label="You want more...")
        court_dropdown = gr.Dropdown(choices=court_options, label="Court Surface")

    comment_input = gr.Textbox(label="Additional Comments (optional)",
                               placeholder="e.g., I'm struggling with high balls or off-balance shots.")

    ask_button = gr.Button("Ask the Coach", elem_classes=["custom-button"])

    output = gr.Textbox(label="Coach's Advice", lines=5)
    ask_button.click(fn=get_coaching_advice, inputs=[level_dropdown, age_dropdown, shot_dropdown, skill_dropdown, court_dropdown, comment_input], outputs=output)

# Launch
demo.launch()
