import socket
import time

def balance_game(): #밸런스 게임의 대답을 전해주는 함수.
    qst = sock.recv(1024)
    print(qst.decode("utf-8"))
    start = time.time()
    asw = input('>>>')
    if asw == "":
        asw = input("다시 입력해주세요 : ")

    end = time.time()

    running_time = str(end - start)
    print("걸린 시간 :",int(end-start),"초")
    sock.send(asw.encode("utf-8"))
    sock.send(running_time.encode("utf-8"))

def food_recommend(): #먹으러 갈 음식을 쓰면 서버로 넘겨주는 함수.
    food_answer = input("무엇을 먹으러 가시고 싶으신가요? ")
    sock.send(food_answer.encode("utf-8"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #서버와 통신할 client 소켓을 만든다.
print("서버에 접속하는 중입니다.")

sock.connect(("127.0.0.1", 8554)) # 원하는 서버 컴퓨터의 ip주소를 왼쪽값에 넣으면 된다.

print("SOMETHING에 오신 것을 환영합니다. 이 프로그램을 당신의 썸을 도와주는 채팅 프로그램입니다.")

name = input("이름이 어떻게 되시나요? 아무것도 입력하지 않으시면 익명2이라는 이름으로 채팅을 진행하게 됩니다. 상대방도 마찬가지입니다. \n>>>") #상대방에게 보낼 자신의 이름을 받고 서버로 보낸다.
if name == "":
    name = "익명2"
    sock.send(name.encode("utf-8"))
else:
    sock.send(name.encode("utf-8"))

client2_name = sock.recv(1024) #상대방의 이름을 받는다.
print(client2_name.decode("utf-8"),"님이 접속하셨습니다.")


#공통질문 단계. 대답을 받고 상대방에게 보낸다.
print("공통 질문을 드리겠습니다. 질문에 대답해 주시기 바랍니다.")
information = "당신의 나이와 성별, 사는지역, 그리고 좋아하는 음식, 취미에 대해서 말해주세요. \n엔터키를 누르면 상대방에게 바로 넘어가니 주의해주세요."
print(information)
answer = input('>>>')
if answer == "":
    answer = "상대방이 입력하지 않으셨습니다."

sock.send(answer.encode("utf-8"))

#상대방의 질문을 받고 화면에 출력한다. 상대방의 질문 시간임을 알려주고 다섯번 대답할 기회를 준다.
client2_answer = sock.recv(1024)
print(client2_answer.decode("utf-8"))
print("상대방의 질문 시간입니다. 총 5번이고, 5번의 질문이 끝나면 당신의 차례입니다. \n질문에 대해 대답해주시기 바랍니다. \n상대방이 질문을 하는 동안에 엔터키를 누르지 않도록 해주세요. 프로그램이 정상적으로 작동하지 않을 수 있습니다.")
print("상대방에게 답장을 보내고 싶지 않다면 상대방의 질문을 받은 후에 엔터키를 한 번 누르시면 됩니다.")
i = 0
while i < 5:
    client1 = sock.recv(1024)
    print("상대방 : ", client1.decode("utf-8"))

    client2 = input("상대방에게 보낼 답장 : ")
    if client2 == "":
        client2 = "대답하지 않겠습니다."
    sock.send(client2.encode("utf-8"))

    i = i + 1

else: #이제 상대방에게 질문할 시간임을 알려주고, 상대방에게 5번 질문할 기회를 준다.
    question = sock.recv(1024)
    print(question.decode("utf-8"))

    j = 0
    while j < 5:

        client2 = input("상대방에게 보낼 질문 : ")
        if client2 == "":
            client2 = "질문하지 않겠습니다."
        sock.send(client2.encode("utf-8"))

        client1 = sock.recv(1024)
        print("상대방 : ", client1.decode("utf-8"))
        j = j + 1
#밸런스 게임 시작.
    else:
        balance = sock.recv(1024)
        print(balance.decode("utf-8"))

        balance_game()
        balance_game()
        balance_game()
        balance_game()
        balance_game()

        level = sock.recv(1024)
        print("서로에 대한 호감도 레벨은 "+level.decode("utf-8")+" 입니다.")
        if float(level.decode("utf-8")) >= 50:
            if float(level.decode(("utf-8"))) == 100:
                print("두 분은 서로 매우 잘 맞는 연애 스타일을 갖고 계신 것 같습니다.")
                print("모든 문제에 대해 서로 같은 답을 말하셨습니다.")
            else:
                print("두 분은 서로 비슷한 연애 스타일을 갖고 계신 것 같습니다.")

            food_recommend()
            food_together_1 = sock.recv(1024)
            food_together_2 = sock.recv(1024)
            print(food_together_1.decode("utf-8"))
            print(food_together_2.decode(("utf-8")))
            print("좋은시간 보내세요!")
            print("이상으로 채팅앱 프로그램을 종료합니다. 감사합니다.")

            sock.close()

        else: #그렇지 않으면
            if float(level.decode("utf-8")) >= 30:
                print("두 분은 서로 선호하는 연애 스타일이 조금 다른 것 같습니다.")
            else:
                print("두 분은 서로 선호하는 연애 스타일이 다른 것 같습니다.")
            something = sock.recv(1024)
            print(something.decode("utf-8"))
            print("이상으로 채팅앱 프로그램을 종료합니다. 감사합니다.")

            sock.close()