
from fastapi import FastAPI, File, UploadFile, Form
import shutil
import os
import zipfile
import pandas as pd
import openai

app = FastAPI()


# Initialize OpenAI API client (Replace 'your-openai-api-key' with your actual key)
OPENAI_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDU0MDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K64O0PbK3iKww6-DbegKFT9WSd9U6bImWlQRsr4ZENA"
openai.api_key = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = None):
    if file:
        # Ensure temp directory exists
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("temp")

            # Look for a CSV file in extracted folder
            for extracted_file in os.listdir("temp"):
                if extracted_file.endswith(".csv"):
                    df = pd.read_csv(f"temp/{extracted_file}")
                    if "answer" in df.columns and not df.empty:
                        return {"answer": str(df["answer"].iloc[0])}

    # If no file, use OpenAI GPT-4 to generate an answer
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that answers Data Science questions."},
                  {"role": "user", "content": question}]
    )

    return {"answer": response["choices"][0]["message"]["content"].strip()}

