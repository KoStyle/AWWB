def get_survivors(listar):
    listatmp = []
    for index in range(len(listar)):
        if listar[index].isAlive:
            listatmp.append(listar[index])
    return listatmp


def get_corpses(harpies):
    corpses = []
    for index in range(len(harpies)):
        if not harpies[index].isAlive:
            corpses.append(harpies[index])
    return corpses
