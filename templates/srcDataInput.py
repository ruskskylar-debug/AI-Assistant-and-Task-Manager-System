import os
import re
from PyPDF2 import PdfReader
from docx import Document


def readTextFile(filePath):
    with open(filePath, "r", encoding="utf-8") as file:
        return file.read()


def readPdfFile(filePath):
    reader = PdfReader(filePath)
    text = ""

    for page in reader.pages:
        pageText = page.extract_text()

        if pageText:
            text += pageText + "\n"

    return text


def readDocxFile(filePath):
    document = Document(filePath)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def readFile(filePath):
    fileExtension = os.path.splitext(filePath)[1].lower()

    if fileExtension == ".txt":
        return readTextFile(filePath)

    elif fileExtension == ".pdf":
        return readPdfFile(filePath)

    elif fileExtension == ".docx":
        return readDocxFile(filePath)

    else:
        print("File type not supported. Please use TXT, PDF, or DOCX.")
        return ""


def enterText():
    print("\nEnter your study material.")
    print("Type DONE on a new line when you are finished.\n")

    lines = []

    while True:
        line = input()

        if line.upper() == "DONE":
            break

        lines.append(line)

    return "\n".join(lines)


def cleanText(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = text.strip()

    return text


def saveRawData(subject, topic, text):
    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/study_material.txt", "w", encoding="utf-8") as file:
        file.write("Subject: " + subject + "\n")
        file.write("Topic: " + topic + "\n\n")
        file.write(text)


def saveCleanedData(subject, topic, text):
    os.makedirs("data/cleaned", exist_ok=True)

    with open(
        "data/cleaned/study_material_cleaned.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("Subject: " + subject + "\n")
        file.write("Topic: " + topic + "\n\n")
        file.write(text)


def main():
    print("=" * 50)
    print("              STUDYSENSE")
    print("=" * 50)

    subject = input("\nSubject: ")
    topic = input("Topic: ")

    print("\nHow would you like to add your study material?")
    print("1. Upload a file")
    print("2. Enter text")

    choice = input("\nChoose 1 or 2: ")

    if choice == "1":
        filePath = input("\nEnter the path to your file: ")

        if not os.path.exists(filePath):
            print("File not found.")
            return

        text = readFile(filePath)

        if text == "":
            print("No text could be extracted.")
            return

    elif choice == "2":
        text = enterText()

        if text.strip() == "":
            print("No study material was entered.")
            return

    else:
        print("Invalid choice.")
        return

    saveRawData(subject, topic, text)

    cleanedText = cleanText(text)

    saveCleanedData(subject, topic, cleanedText)

    print("\n" + "=" * 50)
    print("              DATA PROCESSED")
    print("=" * 50)

    print("Subject:", subject)
    print("Topic:", topic)
    print("Original characters:", len(text))
    print("Cleaned characters:", len(cleanedText))

    print("\nStudy material saved successfully!")


main()
