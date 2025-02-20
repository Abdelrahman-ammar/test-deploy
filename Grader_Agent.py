from Config import qwen , REDIS_URL , qwen_json_mode
from langchain_core.prompts import ChatPromptTemplate , SystemMessagePromptTemplate , HumanMessagePromptTemplate
import json

def grade_answer(question : str , answer : str):
    # grading_instructions = SystemMessagePromptTemplate.from_template(""" Yor are a turtles researcher grader assessing answer of a question,

    # If the answer contains keyword(s) or semantic meaning related to the question, grade it as relevant.
    
    # Return JSON with single key, 'binary_score' that is 'yes' or 'no' score to indicate wehter the document cotains atleast some information that is relevant to the question.
    # """)
    grading_instructions = SystemMessagePromptTemplate.from_template(""" Yor are an answer evaluation agent, Your task is to determine wether the given answer is relevant to the provided question.

    If the answer contains keyword(s) or semantic meaning related to the question, grade it as relevant.
    
    Return JSON with single key, 'binary_score' that is 'yes' or 'no' score to indicate wehter the document cotains atleast some information that is relevant to the question.
    """)

    grading_prompt = HumanMessagePromptTemplate.from_template("""
    Please grade the following:

    QUESTION: {question}
    ANSWER: {answer}
    """)

    chat_prompt = ChatPromptTemplate.from_messages([
        grading_instructions,
        grading_prompt],
        # input_variables=["question", "answer"]
          )
    
    
    
    grader_chain = chat_prompt | qwen_json_mode 

    grade = grader_chain.invoke({"question" : question , "answer" : answer})
    grade = json.loads(grade.content)
    
    print(f"Question is : {question}")
    print(f"Answer is : {answer}")
    print(f"Grade is : {grade["binary_score"]}")

    if grade["binary_score"].lower() == "yes":
        return answer
    else:
        pass

print(grade_answer(question="can you show me some photos for it?" , answer="""Here is one photo of a green turtle (Chelonia mydas):

![](https://static.inaturalist.org/photos/471323621/original.jpeg)"""))