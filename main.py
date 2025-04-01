

from fastapi import FastAPI, Form, File, UploadFile
import openai
from io import StringIO

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key (replace with your actual key)
OPENAI_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDU0MDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K64O0PbK3iKww6-DbegKFT9WSd9U6bImWlQRsr4ZENA"  # Replace with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to interact with OpenAI API
def get_openai_response(question: str, context: str = ""):
    # Crafting the message to OpenAI GPT model
    prompt = f"Answer the following question:\n\n{question}\n\nContext:\n{context}"
    
    try:
        # Calling OpenAI API for response
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/api/")  # Ensure the route is POST
async def answer_question(
    question: str = Form(...), 
    context: str = Form(...), 
    file: UploadFile = File(None)  # Optional file upload
):
    # If a file is uploaded, read its content and use it as context
    if file:
        try:
            # Read the uploaded file content
            content = await file.read()
            file_content = content.decode('utf-8')  # assuming the file is text-based
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not read file content")
        
        context = file_content  # Use the file content as the context for the OpenAI query
    
    # Get response from OpenAI
    answer = get_openai_response(question, context)
    
    if not answer:
        raise HTTPException(status_code=500, detail="Failed to get a valid response from OpenAI API")
    
    return {"answer": answer}
