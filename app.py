from flask import Flask
from flask import request
from secrets import token_hex
app = Flask(__name__)
a=[]
spisok_game=[]
scores={}
active_game=[]##индексы активных игр
games=[]##список активных игр
cards={}##оставшиеся карты
active_cards={}##карты на поле
for i in range(500):
    spisok_game.append(i)
def datta():
    data=request.get_json()
    return data
@app.get("/")
def main():
    return "<h1>Niger</h1>"
@app.post("/vozved")
def fuc():
    pata=datta()
    w=pata["chislo"]
    n=pata["step"]
    k=1
    for i in range(0,n):
        k=k*w
    return {"otvet":k}
def register():
    pata=datta()
    p=token_hex(16);
    error=False
    for i in range(len(a)):
        if (a[i]["nickname"]==pata["nickname"]):
            error=True
    if (error):
        n={
        "success": False,
        "exception": {
        "message": "Nickname exist"
            }
        }
        return n
    else:
        b={"nickname": pata["nickname"], "password": pata["password"],"accesstoken": p}
        c={"success": True, "exception": None, "nickname": pata["nickname"], "accesstoken": p}
        a.append(b)
        return c
@app.post("/user/success")
def success():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False
            c={"success": True, "exception": None, "nickname": nickname, "accesstoken": pata["accesstoken"]}
            return c
    n={
    "success": False,
    "exception": {
        "message": "Nickname or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/room/create")
def create():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False
            gameid=spisok_game[0]
            if (active_game==[]):
                active_game.append(gameid)
            else:
                for i in range(len(active_game)):
                    if (gameid<active_game[i]):
                        active_game.insert(i, gameid)
                        break
                    elif (i==len(active_game)-1and gameid>active_game[i]):
                        active_game.insert(i+1, gameid)
                        break
            for i in range(len(active_game)):
                games.append({"id": active_game[i],"users":[]})
            spisok_game.pop(0)
            cards1=[]
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for t in range(3):
                             cards1.append({"id": i*3*3*3+j*3*3+k*3+t+1,
                            "color": i+1,
                            "shape": j+1,
                            "fill": k+1,
                            "count": t+1})
            cards[gameid]= cards1
            cards2=[]
            chislo=[]
            while(len(chislo)<12):
                new=int(random.random() * len(cards[gameid]))
                while(new in chislo):
                    new=int(random.random() * len(cards[gameid]))
                chislo.append(new)
            chet=0
            m=0
            while (m<len(cards[gameid])):
                if (cards[gameid][m]["id"] in chislo):
                    cards2.append(cards[gameid][m])
                    cards[gameid].pop(m)
                    m=m-1
                m+=1
            active_cards[gameid]= cards2
            c= {"success": True,"exception": None,"gameId": gameid}
            return c
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/room/list")
def lisst():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False    
            return {"games:": games}
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/room/enter")
def enter():
    pata=datta()
    error=True
    if (pata["gameid"] in active_game):
        for i in range(1, len(a)+1):
            if (a[i-1]["accesstoken"]==pata["accesstoken"]):
                nickname=a[i-1]["nickname"]
                error=False
                for i in range(len(games)):
                    if (pata["accesstoken"] in games[i]["users"]):
                        n={
                            "success": False,
                            "exception": {
                            "message": "user is already playing"
                            }
                            }
                        return n
                for i in range(len(games)):
                    if (games[i]["id"]==pata["gameid"]):
                        games[i]["users"].append(pata["accesstoken"])
                        scores[pata["accesstoken"]]=0
                return {"success": True,"exception": None,"gameId": pata["gameid"],"a": games[i]["users"]}
        n={
        "success": False,
        "exception": {
            "message": "token or password is incorrect"
        }
        }
        if(error):
            return n
    else:
        n={
        "success": False,
        "exception": {
            "message": "gameid is not active"
        }
        }
        return n
@app.post("/set/field")
def field():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False
            for l in range(len(games)):
                if (pata["accesstoken"] in games[l]["users"]):
                    b=games[l]["id"]
                    s=active_cards[b]
                    return s
                else:
                    n={"success": False,"exception": {"message": "user is not playing"}}
                    return n
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/pick")
def pick():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False
            for l in range(len(games)):
                if (pata["accesstoken"] in games[l]["users"]):
                    b=games[l]["id"]
                    spisok_id=[]
                    for n in range(len(active_cards[b])):
                        spisok_id.append(active_cards[b][n]["id"])
                    if (pata["cards"][0] in spisok_id and pata["cards"][1] in spisok_id and pata["cards"][2] in spisok_id ):
                        three_card=[]
                        id_udul1=[]
                        for k in range(3):
                            id_udul1.append(pata["cards"][k])
                            three_card.append({"id": pata["cards"][k],
                            "color": (pata["cards"][k]-1)//27+1,
                            "shape": (pata["cards"][k]-1)%27//9+1,
                            "fill": (pata["cards"][k]-1)%9//3+1,
                            "count": (pata["cards"][k]-1)%3+1
                                })
                        fact=["color","shape","fill","count"]
                        fact1=[1,2,3,4]
                        for s in range(len(fact)):
                            if (three_card[0][fact[s]]==three_card[1][fact[s]]):
                                fact1[s]=three_card[0][fact[s]]
                            else:
                                fact1[s]=6-three_card[0][fact[s]]-three_card[1][fact[s]]
                        setio=True
                        for s in range(len(fact)):
                            if (three_card[2][fact[s]]!=fact1[s]):
                                setio=False
                        if(setio):
                            op=0
                            while(op < len(active_cards[b])):
                                if (active_cards[b][op]["id"] in id_udul1):
                                    active_cards[b].pop(op)
                                    op-=1
                                op+=1
                            cards2=[]
                            chislo=[]
                            if (cards[b]!=[]):
                                while(len(chislo)<3):
                                    new=int(random.random() * len(cards[b]))
                                    while(new in chislo):
                                        new=int(random.random() * len(cards[b]))
                                    chislo.append(new)
                                id_udal=[]
                                while(len(chislo)>0):
                                    for m in range(len(cards[b])):
                                        if (m==chislo[0]):
                                            active_cards[b].append(cards[b][m])
                                            chislo.pop(0)
                                            id_udal.append(cards[b][m]["id"])
                                            break
                                m=0
                                while (m<len(cards[b])):
                                    if (int(cards[b][m]["id"]) in id_udal):
                                        cards[b].pop(m)
                                        m=m-1
                                    m+=1
                            scores[pata["accesstoken"]]+=1
                            return {"isSet": True,"score": scores[pata["accesstoken"]]}
                        else:
                            return {"isSet": False,"score": scores[pata["accesstoken"]]}
                    else:
                        return {
                            "success": False,
                            "exception": {
                            "message": "cards are not exist"
                            }
                            }
                else:
                    n={"success": False,"exception": {"message": "user is not playing"}}
                    return n
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/add")
def add():
    pata=datta()
    error=True
    b=0
    for u in range(1, len(a)+1):
        if (a[u-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[u-1]["nickname"]
            error=False
            for l in range(len(games)):
                if (pata["accesstoken"] in games[l]["users"]):
                    end=False
                    b=games[l]["id"]
                    for i in range(len(active_cards[b])):
                        one=active_cards[b][i]
                        for j in range(len(active_cards[b])):
                            if (i!=j):
                                two=active_cards[b][j]
                                fact=["color","shape","fill","count"]
                                fact1=[1,2,3,4]
                                for s in range(len(fact)):
                                    if (one[fact[s]]==two[fact[s]]):
                                        fact1[s]=one[fact[s]]
                                    else:
                                        fact1[s]=6-one[fact[s]]-two[fact[s]]
                                for r in range(81):
                                    carta={"id": r,
                                    "color": fact1[0],
                                    "shape": fact1[1],
                                    "fill": fact1[2],
                                    "count": fact1[3]}
                                    if carta in active_cards[b]:
                                        mass=[one,two,carta]
                                        end=True
                                    if(end):
                                        break
                                if(end):
                                    break
                            if(end):
                                break

                        if(end):
                            break
                    if (end):
                        return {"success": False,"exception": {"message": "Set is exist"},"set": mass}
                    else:
                        
                        chislo=[]
                        if(cards[b]!=[]):
                            while(len(chislo)<3):
                                new=int(random.random() * len(cards[b]))
                                while(new in chislo):
                                    new=int(random.random() * len(cards[b]))
                                chislo.append(new)
                            id_udal=[]
                            while(len(chislo)>0):
                                for m in range(len(cards[b])):
                                    if (m==chislo[0]):
                                        active_cards[b].append(cards[b][m])
                                        id_udal.append(cards[b][m]["id"])
                                        chislo.pop(0)
                                        break
                            m=0
                            while (m<len(cards[b])):
                                if (cards[b][m]["id"] in id_udal):
                                    cards[b].pop(m)
                                    m=m-1
                                m+=1
                            return{
                            "success": True,
                            "exception": None
                            }
                        else:
                            for i in range(len(games)):
                                if (pata["accesstoken"] in games[i]["users"]):
                                    games.pop(i)
                                    active_game.pop(i)
                                    active_cards.pop(i)
                                    cards.pop(i)
                            return{
                            "success": False,
                            "exception": True
                            }
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
@app.post("/set/scores")
def scor():
    pata=datta()
    error=True
    for i in range(1, len(a)+1):
        if (a[i-1]["accesstoken"]==pata["accesstoken"]):
            nickname=a[i-1]["nickname"]
            error=False
            for l in range(len(games)):
                if (pata["accesstoken"] in games[l]["users"]):
                    m={
                        "success": True,
                        "exception": None,
                        "users": []
                    }
                    for k in range(len(a)):
                        if (a[k]["accesstoken"] in games[l]["users"]):
                            m["users"].append({"name": a[k]["nickname"],"score": scores[a[k]["accesstoken"]]})
                    return m
                else:
                    n={"success": False,"exception": {"message": "user is not playing"}}
                    return n
    n={
    "success": False,
    "exception": {
        "message": "token or password is incorrect"
    }
    }
    if(error):
        return n
