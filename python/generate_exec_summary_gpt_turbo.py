from openai import OpenAI
from dotenv import load_dotenv 


load_dotenv()
client = OpenAI()

# Generate an executive summary using GPT-4 preview
def generate_executive_summary_gpt_turbo(aggregated_texts):
    """
    Generates an executive summary for the given aggregated article text using GPT-4 preview.
    
    Parameters:
    aggregated_texts (str): The aggregated texts of articles.

    Returns:
    str: The executive summary of the aggregated texts.
    """
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",  # Adjust for the GPT-4 model when available
    # Extracting the summary from the response
    messages = [
    {
        "role": "system",
        "content": "Act like an Insightful Business Analyst. Please create a very concise executive summary for the story. Stick to one or two key points. Your output should be structured as follows:\n\nTitle: [Insert Title Here]\n\nSummary: [Insert Summary Here]."
    },
    {
        "role": "user",
        "content": aggregated_texts  # Assuming 'aggregated_text' is the variable holding the story's content
    }
]
)
    summary = response.choices[0].message.content
    return summary


