import cv2

#グレースケール化関数
def to_grauscale(path):
	img = cv2.imread(path)
	grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return grayed
	
#matplotlib用のBGR→RGB変換関数
def to_matplotlib_format(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

"""	閾値説明
背景を落とす->THRESH_BINARY
閾値より大きい箇所(=明るい=薄い=背景): maxValue(255=白=消す)
閾値未満: 0(黒=強調)
境界の明確化->THRESH_BINARY_INV
閾値より大きい箇所(=明るい=鳥の骨=境界): 0(黒=強調)
閾値未満: maxValue(255=白=消す)
"""
def binary_threshold(path):
	img = cv2.imread(path)
	grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	under_thresh = 105
	upper_thresh = 145
	maxvalue = 255
	th, drop_back = cv2.threshold(grayed, under_thresh, maxValue, cv2.THRESH_BINARY)
	th, clarify_born = cv2.threshold(grayed, upper_thresh, maxValue, cv2.THRESH_BINARY_INV)
	merged = np.minium(drop_back, clarify_born)
	return merged

#特定色の抜き出し
def mask_blue(path):
	img = cv2.imread(path)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	blue_min = np.array([100, 170, 200], np.uint8)
	blue_max = np.array([120, 180, 255], np.unit8)
	
	blue_region = cv2.inRange(hsv, blue_min, blue_max)
	white = np.full(img.shape, 255, dtype=img.dtype)
	background = cv2.bitwise_and(white, white, mask=blue_region)
	
	inv_mask = cv2.bitwise_not(blue_region)
	extracted = cv2.bitwise_and(img, img, mask=inv_mask)
	
	masked =cv2.add(extracted, background)
	
	return masked

#平滑化（スムージング）関数
def blur(img):
    filtered = cv2.GaussianBlur(img, (11, 11), 0)
    return filtered
    
#モルフォロジー
def morph(img):
    kernel = np.ones((3, 3),np.uint8)
    opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)
    return opened
    
#両方
def morph_and_blur(img):
    kernel = np.ones((3, 3),np.uint8)
    m = cv2.GaussianBlur(img, (3, 3), 0)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel, iterations=2)
    m = cv2.GaussianBlur(m, (5, 5), 0)
    return m

#輪郭検出
def detect_contour(path, min_size):
	contoured = cv2.imread(path)
	forcrop = cv2.imread(path)
	
	birds = binary_threshold_for_birds(path) #閾値処理の関数の呼び出し　　白黒の場合「白」の方が値が高いため(255)、輪郭検出を行う場合輪郭が白で描画されている画像を入力として与える必要
	birda = cv2.bitwise_not(birds)
	
	im2, contours, hierarchy = cv2.findContours(birds, cv2.RETR_EXTERNAL, cv2.CGAIN_APPROX_SIMPLE)
	
	crops = []
	
	for c in contours:
		if cv2.contourArea(c) < min_size:
			continue
			
		x, y, w, h = cv2.boundingRect(c)
		x, y, w, h = padding_position(x, y, w, h, 5)
		
		cropped = forcrop[y:(y + h), x:(x + w)]
		cropped = resize_image(cropped, (210, 210))
		crops.append(cropped)
		
		cv2.drawContours(contoured, c, -1, (0, 0, 255), 3)
		cv2.rectangle(contoured, (x, y), (x + w, y + h), (0, 255, 0), 3)
		
	return contoured, crops
	
def padding_position(x, y, w, h, p):
	return x-p, y-p, w+p*2, h+p*2
	
#輪郭の近似
#cv2.arcLengthは輪郭の長さで、これを使いepsilon、最低限の直線の長さを計算
def various_contours(path):
	color = cv2.imread(path)
	grayed = cv2.cvtColor(color, cv2.COLOR_BRG2GRAY)
	_, binary = cv2.threshold(grayed, 218, 255, cv2.THRESH_BINARY)
	inv = cv2.bitwise_not(binary)
	_, contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for c in contours:
		if cv2.contourArea(c) < 90:
			continue
		epsilon = 0.01 * cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, epsilom, True)
		cv2.drawContours(color, c, -1, (0, 0, 255), 3)
		cv2.drawContours(color, [approx], -1, (0, 255, 0), 3)
		
	plt.imshow(cv2.cvtColor(color, cv2.COLOR_BGR2RGB))
various_contours(IMF_FOR_CONTOUR)


#領域の切り出し
#resize: 所定のサイズのキャンバス(resized)を用意(学習データの画像のサイズか、後から切り取るためちょっと大きめにする)
#centering: 用意したキャンバスの中心に、切り出した画像をセット
#filling: セットした画像の周辺領域を、元の画像の情報を利用し埋める
def resize_image(img, size):
	img_size = img.shape[:2]
	if img_size[0] > size[1] or img_size[1] > size[0]:
		raise Exception("img is larger than size")
	
	#centering
	row = (size[1] - img_size[0]) // 2
	col = (size[0] - img_size[1]) // 2
	resized = np.zeros(list(size) + [img.shape[2]], dtype=np.unit8)
	resized[row:(row + img.shape[0]), col:(col + img.shape[1])] = img
	
	#filling
	mask = np.full(size, 255, dtype=np.unit8)
	mask[row:(row + img.shape[0]), col:(col + img.shape[1])] = 0
	filled = cv2.inipaint(trsized, mask, 3, cv2.INPAINT_TELEA)
	
	return filled
	
#画像の位置揃え
def align(base_img, target_img, warp_mode=cv2.MOTION_TRANSLATION, number_of_iterations=5000, termination_eps=1e-10):
    base_gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    # prepare transformation matrix
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    sz = base_img.shape

    # estimate transformation
    try:
        (cc, warp_matrix) = cv2.findTransformECC(base_gray, target_gray, warp_matrix, warp_mode, criteria)

        # execute transform
        if warp_mode == cv2.MOTION_HOMOGRAPHY :
            # Use warpPerspective for Homography 
            aligned = cv2.warpPerspective(target_img, warp_matrix, (sz[1], sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        else :
            # Use warpAffine for Translation, Euclidean and Affine
            aligned = cv2.warpAffine(target_img, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

        return aligned
    except Exception as ex:
        print("can not align the image")
        return target_img
        
#顔の特徴点揃え
def face_align(base, base_position, target, target_position):
    sz = base.shape
    fsize = min(len(base_position), len(target_position))  # adjust feature size
    tform = cv2.estimateRigidTransform(target_position[:fsize], base_position[:fsize], False)
    aligned = cv2.warpAffine(target, tform, (sz[1], sz[0]))
    return aligned

