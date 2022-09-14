from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid
import uvicorn
from fer import FER
import matplotlib.pyplot as plt





IMAGEDIR = "/home/sam/projects/images/"

app = FastAPI()


@app.post("/images/")
async def create_upload_file(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!

    # example of how you can save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}



@app.get("/emotion_expression/")
async def emotion():

    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)
    path = f"{IMAGEDIR}{files[random_index]}"

    test_image_one = plt.imread(path)
    emo_detector = FER(mtcnn=True)

    # Capture all the emotions on the image
    captured_emotions = emo_detector.detect_emotions(test_image_one)
    emotions_dict = [d['emotions'] for d in captured_emotions][0]
    # Print all captured emotions with the image
    print(emotions_dict)

    FileResponse(path)
    #plt.imshow(test_image_one)
    return emotions_dict


@app.get("/images/")
async def read_uploaded_file():
    # get a random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    # notice you can use FileResponse now because it expects a path
    return FileResponse(path)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
