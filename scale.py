import cv2


def scale_cv2(filename, src):
    img = cv2.imread(filename)
    # инициализировать распознаватель лиц (каскад Хаара по умолчанию)
    face_cascade = cv2.CascadeClassifier("haarcascade_fontalface_default.xml")
    width = face_cascade.detectMultiScale(img)[0, 2]
    ratio = 1
    print(width)
    if width < 244:
        while width < 244:
            ratio += 0.01
            res = cv2.resize(img, None, fx=float(ratio), fy=float(ratio),
                             interpolation=cv2.INTER_CUBIC)  # Коэффициент масштабирования: fx , fy
            width = face_cascade.detectMultiScale(res)[0, 2]
    else:
        while width >= 244:
            ratio -= 0.01
            res = cv2.resize(img, None, fx=float(ratio), fy=float(ratio),
                             interpolation=cv2.INTER_CUBIC)  # Коэффициент масштабирования: fx , fy
            width = face_cascade.detectMultiScale(res)[0, 2]
    # преобразуем изображение к оттенкам серого
    image_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # инициализировать распознаватель лиц (каскад Хаара по умолчанию)
    face_cascade = cv2.CascadeClassifier("haarcascade_fontalface_default.xml")
    # обнаружение всех лиц на изображении
    faces = face_cascade.detectMultiScale(image_gray)
    # печатать количество найденных лиц
    print(f"{len(faces)} лиц обнаружено на изображении.")
    # для всех обнаруженных лиц рисуем синий квадрат
    for x, y, width, height in faces:
        # cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
        # cv2.rectangle(image, (x-25, y-100), (x + 275, y + 300), color=(255, 212, 0), thickness=2)

        # обрезаем изображение 3х4
        crop_img = res[y - 100:y + 300, x - 25:x + 275]
        cv2.imwrite(src+'result.jpg', crop_img)
