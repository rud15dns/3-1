import socket
import random
import time

balance = "이제 밸런스 게임을 시작하겠습니다. 밸런스 게임의 결과는 호감도 레벨에 반영됩니다." #balance게임 질문을 client에게도 넘겨야 해서 질문 내용을 길게 쓰면 안될 것 같아 변수로 지정해둠.
def balance_game(a, b, c): #balance게임할 함수
    level = 0
    qst = "\n<<"+c+"에 대해서>> \n\n1."+a+" vs "+"2. "+b+" \n\n1 혹은 2로 대답하면 됩니다. 10초 이내에 답하지 않으면 호감도 레벨에 영향을 끼칠 수 있습니다."
    print(qst)
    start = time.time()

    response = input('>>>')
    if response == "":
        response = input("다시 입력해주세요 : ")

    end = time.time()
    running_time = end - start
    print("걸린 시간 : ", int(running_time),"초")
    c_sock.send(qst.encode("utf-8"))

    response_1 = c_sock.recv(1024)
    response_1_decode = response_1.decode("utf-8")


    other_side_running_time = c_sock.recv(1024)
    osrtdecode = other_side_running_time.decode("utf-8")

    if response == response_1_decode:
        if running_time <= 10 and float(osrtdecode) <= 10:
            return 20
        elif running_time <= 10 and float(osrtdecode) > 10:
            return 10
        elif running_time > 10 and float(osrtdecode) <= 10:
            return 10
        else:
            return 5
    else:
        return 0

def food_recommend(): #호감도가 일정 수준 이상일 때 실행되는 음식을 추천해주는 함수. 만일 먹고 싶은 것이 같다면 그것을 먹고 가라고 print하고, 아니면 정해둔 음식을 랜덤으로 뽑아주어 화면에 출력해주는 함수.

    food = ["마라탕", "파스타", "스시","스테이크","삼겹살","라면","피자","치킨"]
    num = random.randint(0, len(food)-1)

    food_qst = "무엇을 먹으러 가시고 싶으신가요? "
    a = input(food_qst)


    food_response = c_sock.recv(1024)
    food_response_decode = food_response.decode("utf-8")

    if a == food_response_decode:
        return a
    else:
        print("두 분이 먹고 싶어하신 음식이 달랐기 때문에 오늘의 메뉴를 추천드립니다.")
        c_sock.send("두 분이 먹고 싶어하신 음식이 달랐기 때문에 오늘의 메뉴를 추천드립니다.".encode("utf-8"))
        return food[num]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #통신할 소켓을 만든다.
sock.bind(("", 8554)) #왼쪽에 서버 ip주소를 넣으면 된다.
sock.listen() #상대방이 들어오기를 기다린다.
print("상대방이 들어오기를 기다리는 중입니다.")

c_sock, addr = sock.accept()
print("상대방이 접속하셨습니다.")
print("SOMETHING에 오신 것을 환영합니다. 이 프로그램을 당신의 썸을 도와주는 채팅 프로그램입니다.")
name = input("이름이 어떻게 되시나요? 아무것도 입력하지 않으시면 익명1이라는 이름으로 채팅을 진행하게 됩니다. 상대방도 마찬가지입니다. \n>>>") #상대방에게 보낼 자신의 이름을 받고 보낸다.
if name == "":
    name = "익명1"
    c_sock.send(name.encode("utf-8"))
else:
    c_sock.send(name.encode("utf-8"))

#상대방의 이름을 받는다. 화면에 출력해준다.
client1_name = c_sock.recv(1024)
client1_name_1 = client1_name.decode("utf-8")
print(client1_name.decode("utf-8"),"님이 접속하셨습니다.")


print("공통 질문을 드리겠습니다. 질문에 대답해 주시기 바랍니다.") #공통질문 단계. 상대방에게 보낸다.
information = "당신의 나이와 성별, 사는지역, 그리고 좋아하는 음식, 취미에 대해서 말해주세요. \n엔터키를 누르면 상대방에게 바로 넘어가니 주의해주세요."
print(information)
answer = input('>>>')
if answer == "":
    answer = "상대방이 입력하지 않으셨습니다."

c_sock.send(answer.encode("utf-8"))


client1_answer = c_sock.recv(1024) #상대방이 쓴 공통질문에 대한 대답을 받고 화면에 출력한다.
print(client1_answer.decode("utf-8"))

#질문 기회 다섯 번 시작.
print("질문 기회는 다섯번 입니다. 신중하게 질문하세요. \n상대방에게 질문을 보내고 나서 다시 한번 엔터키를 누르지 마세요. 프로그램이 정상적으로 작동하지 않을 수 있습니다. \n상대방에게 질문하고 싶지 않다면 엔터키를 한번만 누르시면 됩니다.")
i = 0
while i < 5:
    client1 = input("상대방에게 보낼 질문 : ")
    if client1 == "":
        client1 = "질문하지 않겠습니다."
    c_sock.send(client1.encode("utf-8"))


    client2 = c_sock.recv(1024)
    print("상대방 : ",client2.decode("utf-8"))

    i = i + 1

else: #상대방이 질문할 차례임을 알려준다
    print("상대방이 질문할 차례입니다. 질문을 기다려주세요. \n기다리는 동안에 엔터키를 누르지 않도록 해주세요. 프로그램이 정상적으로 작동하지 않을 수 있습니다.")
    c_sock.send("당신이 질문할 차례입니다. 기회는 총 5번입니다. 신중하게 질문해주세요. \n상대방에게 질문을 보내고 나서 다시 한번 엔터를 누르지 마세요. 프로그램이 정상적으로 작동하지 않을 수 있습니다. \n상대방에게 질문하고 싶지 않다면 엔터키를 한번만 누르시면 됩니다.".encode("utf-8"))

    j = 0
    print("답장을 보내고 싶지 않다면 상대방의 질문을 받은 후에 엔터키를 한 번 누르시면 됩니다.")
    while j < 5:
        client2 = c_sock.recv(1024)
        print("상대방 : ", client2.decode("utf-8"))

        client1 = input("상대방에게 보낼 답장 : ")
        if client1 == "":
            client1 = "대답하지 않겠습니다."
        c_sock.send(client1.encode("utf-8"))

        j = j + 1
#질문이 끝나고 나서 호감도 레벨을 측정하기 위한 밸런스게임을 시작한다.
    else:
        print(balance)
        c_sock.send(balance.encode("utf-8"))

        first = balance_game("깻잎 정도는 떼어줘도 괜찮다.", "내 눈 앞에서 깻잎을 떼어주는 것은 용납할 수 없다.", "내 애인과 내 친구 셋이서 밥을 먹는데 내 애인이 친구가 먹으려고 하는 깻잎을 떼어주는 상황")
        second = balance_game("나 빼고 술을 계속 마셔도 상관 없다.", "더 이상 둘이서 술을 마시면 안된다.", "집에서 내 애인과 내 친구 3명이서 술을 먹다가 내가 먼저 크게 취해서 방으로 들어간 상황")
        third = balance_game("연상", "연하","연애 스타일")
        fourth = balance_game("오랜 기간 동안 지낸 친구들이라서 괜찮다.","이성이 포함된 외박 여행은 할 수 없다.", "내 애인이 이성이 포함된 오랜 친구들과 외박 여행을 가는 상황")
        fifth = balance_game("내 친구가 내 애인 새우를 까주기", "내 애인이 내 친구 새우를 까주기", "애인과 친구 셋이서 밥을 먹는데 새우가 나온 상황")

        level = first + second + third + fourth + fifth

        c_sock.send(str(level).encode("utf-8"))
#호감도 레벨이 어느 수준이상이라면 추천 메뉴를 주면서 밥 먹으러 가도록 장려한다.

        print("서로에 대한 호감도 레벨은", level, "입니다.")
        if level >= 50:
            if level == 100:
                print("두 분은 서로 매우 잘 맞는 연애 스타일을 갖고 계신 것 같습니다.")
                print("모든 문제에 대해 서로 같은 답을 말하셨습니다.")
            else:
                print("두 분은 서로 비슷한 연애 스타일을 갖고 계신 것 같습니다.")
            b = food_recommend()


            print(b ,"을(를) 먹으러 가면 될 것 같습니다.")
            print("좋은시간 보내세요!")
            print("이상으로 채팅앱을 종료합니다. 감사합니다.")
            food_send = str(b) + "을(를) 먹으러 가면 될 것 같습니다."
            c_sock.send(food_send.encode("utf-8"))

            c_sock.close()
            sock.close()

        else:
            if level >= 30:
                print("두 분은 서로 선호하는 연애 스타일이 조금 다른 것 같습니다.")
            else:
                print("두 분은 서로 선호하는 연애 스타일이 다른 것 같습니다.")
            next_time = "다음에 더 좋은 기회가 있으면 좋을 것 같습니다."
            print(next_time)
            c_sock.send(next_time.encode("utf-8"))

            print("이상으로 채팅앱을 종료합니다. 감사합니다.")

            c_sock.close()
            sock.close()