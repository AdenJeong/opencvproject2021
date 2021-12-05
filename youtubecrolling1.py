import cv2, pafy, youtube_dl

url = 'https://www.youtube.com/watch?v=wtLCB3UPUNY'
video = pafy.new(url)
print('title = ', video.title)
print('author = ', video.author)
print('video.rating = ', video.rating)
print('video.likes = ', video.likes)
print('video.duration = ', video.duration)

best = video.getbest(preftype='mp4')  # 'webm','3gp'
print('best.resolution= ', best.resolution)
cap = cv2.VideoCapture(best.url)
while (True):
    retval, frame = cap.read()
    if not retval:
        break
    cv2.imshow('frame', frame)
    key = cv2.waitKey(25)

    if key == 27:  # Esc
        break

cv2.destroyAllWindows()