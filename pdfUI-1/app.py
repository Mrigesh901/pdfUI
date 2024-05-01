from flask import Flask, render_template, request, redirect, url_for
# pip install -q --upgrade google-generativeai
# pip install -q --upgrade langchain
# pip install -q --upgrade langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate

from pprint import pprint


app = Flask(__name__)

api_key="$API"
def set_model_parameters(model= "gemini-pro",
                         temperature=0.3,
                         top_p = None,
                         top_k = None,
                         max_output_tokens = 4096,
                         candidate_count =  1,
                         google_api_key = api_key
                         ):
  print("set_model_parameters fired")
  model = ChatGoogleGenerativeAI(model= model,
                                 temperature=temperature,
                                 top_p = top_p,
                                 top_k = top_k,
                                 max_output_tokens = max_output_tokens,
                                 candidate_count = candidate_count,
                                 google_api_key = google_api_key)
  return(model)


# Define follow-up prompts based on user's initial prompt
follow_up_prompts = {
    'Paraphrase the text': None,
    'Draft the document': ['Draft a force majeure clause to exclude labour disputes involving the supplier’s own personnel, and to additionally include COVID-19 and other pandemic', 'Outline and organize the document to ensure logical flow and coherence. Create headings, subheadings, and sections to facilitate readability and comprehension. Incorporate legal formatting requirements and standard document elements (e.g., title page, table of contents).', 'Review and address feedback from stakeholders, attorneys, or clients.Make revisions to reflect comments, suggestions, and revisions provided during the review process.Ensure that changes align with legal requirements and maintain document integrity.'],
    'Proofread a document': ['Proof read this legal brief to ensure consistency in verb tenses and correct any grammatical errors. Be very diligent.', 'Conduct a thorough spell check to detect and rectify typographical errors and misspellings Verify legal terminology and ensure accuracy in terminology usage Use legal dictionaries and reference materials for precise language.', 'Verify the use of commas, periods, semicolons, and other punctuation marks according to legal writing standards. Ensure proper formatting of citations footnotes and references Confirm adherence to legal style guides (e.g., Bluebook, APA) for accurate citation and referencing.'],
    'Review document': ['Analyze the legal document for completeness, accuracy, and relevance to the intended purpose. Offer substantive comments on legal arguments, contract terms, or regulatory compliance.Identify potential legal risks, inconsistencies, or areas requiring further clarification.', 'Assess the documents structure, including headings, subheadings, and transitions between sections.Recommend improvements to enhance readability and logical progression of ideas.Ensure that legal arguments are presented coherently and persuasively.', 'Propose revisions to simplify complex legal language and improve overall clarity.Clarify ambiguous terms or phrases to eliminate potential misinterpretations. Condense verbose passages while preserving legal precision and completeness.'],
    'Answer question about a document': ['Define legal terminology and elucidate their relevance within the documents context.', 'Pd2', 'Pd3'],
    'Summarise a document': ['Condense the document into a concise overview highlighting key points, objectives, and outcomes.', 'Identify critical legal issues, arguments, or provisions central to the documents purpose.', 'Distill intricate legal concepts or technical details into simplified explanations.'],
    'Create ideas for Brainstorming': ['Propose alternative legal frameworks, negotiation tactics, or dispute resolution methods.', 'Lead collaborative discussions to elicit diverse perspectives and ideas from legal colleagues.Use structured techniques (e.g., mind mapping, SWOT analysis) to stimulate creativity and problem-solving.', 'Prepare summary reports or documentation outlining brainstorming results and recommendations.'],
    'Legal research': ['Employ advanced legal research tools and databases to retrieve comprehensive information.', 'Synthesize complex legal information into structured research findings.', 'Evaluate the legal consequences of specific actions or scenarios based on case law and statutes.']
}

def set_prompt_softwired():

  #https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/
  prompt_template = """Paraphrase this text:

  {input_text}

  In the style of a {style}.

  Paraphrase: """

  prompt = PromptTemplate(template=prompt_template, input_variables=["style", "input_text"])

  return(prompt)



def paraphrase_softwired(paraphrase_text,style):

    input_text = paraphrase_text
    style = style
    print("paraphrase_softwired fired..")
    model = set_model_parameters()
    #print("MODEL: ",model)

    prompt = set_prompt_softwired()
    print("PROMPT: ", prompt)

    chain = LLMChain(prompt = prompt, llm = model)
    print("CHAIN: ", chain)

    resp = chain.invoke({"style" : style,
                         "input_text": input_text
                         })

    ptext = resp["text"]
    pprint("PARAPHRASED TEXT: " + ptext)
    return ptext




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next', methods=['GET', 'POST'])
def next_page():
    user_prompt = request.args.get('userPrompt', '')

    if follow_up_prompts[user_prompt] is None:
            return render_template('paraphrase_template.html')
    else:

        if user_prompt in follow_up_prompts and follow_up_prompts[user_prompt] is not None:
            prompts = follow_up_prompts[user_prompt]
        else:
            prompts = []

        # print(f"User Prompt: {user_prompt}")
        # print(f"Follow-up Prompts: {prompts}")

        return render_template('next.html', prompts=prompts)

@app.route('/submit_follow_up', methods=['POST'])
def submit_follow_up():
    custom_prompt = request.form.get('customPrompt', '')

    # Process custom prompt if needed
    
    return redirect(url_for('index'))

@app.route('/submit_paraphrase', methods=['POST'])
def submit_paraphrase():
    paraphrase_text = request.form.get('ParaphraseText', '')  # Get the value of inputText from the form
    style = request.form.get('ParaphraseStyle', '')  # Get the value of style from the form

    # Call set_hardwired function with the extracted values
    output=paraphrase_softwired(paraphrase_text, style)
    return render_template('result.html', result=output)

if __name__ == '__main__':
    app.run(debug=True)
