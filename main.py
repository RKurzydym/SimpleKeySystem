import asyncio
import os
from prisma import Prisma, register
from prisma.models import Person, Card, Tag
from quart import Quart

flag = 0


async def main() -> any:
    # Generate the Database if not exists
    print("Generating Database...")
    prisma = Prisma()
    await prisma.connect()
    global flag
    if flag == 0:
        register(prisma)
        flag = 1
    if os.path.exists("Flag") == False:
        await Default(prisma)
        open("Flag", "w")
    else:
        print("Database Exists")
    return await Card.prisma().find_many()
    # await generate.generate()
    # await addItem()


async def Default(DB: any) -> any:
    Person = await DB.person.create(
        data={
            "name": "Robin",
            "Cards": {
                "create": {"name": "Robin's Card", "uid": "23S48243C988F23949E8234"}
            },
            "Tags": {
                "create": {
                    "name": "Test",
                }
            },
        }
    )


app = Quart(__name__)
  
@app.route("/")
async def hello():
    return 'Hello World'


@app.route("/all/")
async def index():
    data = await main()
    print(data)

    return {"data": [data.dict(exclude={"drawer"}) for data in data]}


@app.route("/<string:uid>")
async def findCard(uid):
    data = await main()

    print(data)
    for card in data:
        if card.uid == uid:
            return "Exists"
    return "Not Found"
@app.route("/add/really/add/<string:uid>/<string:person>/<string:tag>/")
async def addCard(uid, person,tag):
    data = await main()
    print(data)
    for card in data:
        if card.uid == uid:
            return "Exists"
    await Person.prisma().create(
        data={
            "name": person,
            "Cards": {
                "create": {"name": person+"'s Card", "uid": uid}
            },
            "Tags": {
                "create": {
                    "name": tag,
                }
            },
        }
    )
    return "Added"

if __name__ == "__main__":
    app.run(debug=True)
  #04 49 2e 42 d0 76 80