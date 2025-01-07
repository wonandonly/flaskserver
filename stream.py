from flask import Flask, render_template, Response, send_file
from time import sleep, time
import cv2

# Flask 애플리케이션 생성 
app = Flask(__name__)

# 웹캠으로부터 비디오 캡처 객체 생성
capture = cv2.VideoCapture(0)  
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 캡처된 비디오의 폭 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 캡처된 비디오의 높이 설정

# fps 측정을 위한 변수 초기화
prev_time = 0
fps = 0

# 프레임 생성
def GenerateFrames():
    global prev_time, fps
    while True:
        #sleep(0.1)  # 프레임 생성 간격을 잠시 지연시키고 싶으면 이 라인 쓰기
        ref, frame = capture.read()  # 비디오 프레임을 읽어옴 (ref:읽어오기 성공 여부 t/f, frame=img)
        if not ref:  # 비디오 프레임을 제대로 읽어오지 못했다면 반복문을 종료
            break
        else:
            # fps 계산
            curr_time=time() #현재 시간
            fps=1/(curr_time-prev_time) if prev_time!=0 else 0 
            prev_time=curr_time

            # 프레임에 fps 텍스트 추가
            cv2.putText(frame, f"FPS:{fps:.2f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)



            ref, buffer = cv2.imencode('.jpg', frame)  # JPEG 형식으로 이미지를 인코딩
            frame = buffer.tobytes()  # 인코딩된 이미지를 바이트 스트림으로 변환
            # multipart/x-mixed-replace 포맷으로 비디오 프레임을 클라이언트에게 반환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def Index():
    return render_template('index.html')  # index.html 파일을 렌더링하여 반환


@app.route('/stream')
def Stream():
    # GenerateFrames 함수를 통해 비디오 프레임을 클라이언트에게 실시간으로 반환
    return Response(GenerateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def send_video():
    return send_file("video.mp4", as_attachment=False, mimetype='video/mp4')


# Flask 서버를 실행하려는 의도가 있을 경우(외부 import가 아니라 직접 실행한 경우)
if __name__ == "__main__":
    # IP 번호와 포트 번호를 지정하여 Flask 앱을 실행
    app.run(host="10.117.5.56", port="8080")
