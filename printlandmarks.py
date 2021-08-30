def pl(lis):
    names=[
        "wrist",
        "thumb cmc",
        "thumb mcp",
        "thumb ip",
        "thumb tip",
        "index mcp",
        "index pip",
        "index dip",
        "index tip",
        "middle mcp",
        "middle pip",
        "middle dip",
        "middle tip",
        "ring mcp",
        "ring pip",
        "ring dip",
        "ring tip",
        "pinky mcp",
        "pinky pip",
        "pinky dip",
        "pinky pip"]
    for i in range(21):
        print(names[i])
        print(lis[i]["x"])
        print(lis[i]["y"])
        print(lis[i]["z"])