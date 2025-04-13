import os


def save_image(image):
    UPLOAD_FOLDER = "/home/smt/uploads"  # Replace with your desired directory
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists

    # Save the image to the upload folder
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
