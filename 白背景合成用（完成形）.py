gousei = cv2.imread('/home/pi/gazou/gousei.jpg')
gousei2 = crop

white_size = gousei.shape[:2]
hantei_size = gousei2.shape[:2]

if img_size[0] > size[1] or img_size[1] > size[0]:
        raise Exception("img is larger than size")

row = (white_size[1] - hantei_size[0]) // 2
col = (white_size[0] - hantei_size[1]) // 2
resized[row:(row + hantei.shape[0]), col:(col + hantei.shape[1])] = gousei2
cv2.imshow("white2", filled)
cv2.waitKey(0)
