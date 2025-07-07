# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052


class NodeStatus:
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3

class Task:
    def __init__(self, action):
        self.action = action
    def run(self):
        print("[Árbol de comportamiento] Ejecutando tarea")
        return self.action()

class Condition:
    def __init__(self, condition):
        self.condition = condition
    def run(self):
        return NodeStatus.SUCCESS if self.condition() else NodeStatus.FAILURE

class Sequence:
    def __init__(self, children):
        self.children = children
        self.current = 0
    def run(self):
        while self.current < len(self.children):
            status = self.children[self.current].run()
            if status == NodeStatus.FAILURE:
                self.current = 0
                return NodeStatus.FAILURE
            elif status == NodeStatus.RUNNING:
                return NodeStatus.RUNNING
            else:
                self.current += 1
        self.current = 0
        return NodeStatus.SUCCESS

class Selector:
    def __init__(self, children):
        self.children = children
        self.current = 0
    def run(self):
        while self.current < len(self.children):
            status = self.children[self.current].run()
            if status == NodeStatus.SUCCESS:
                self.current = 0
                return NodeStatus.SUCCESS
            elif status == NodeStatus.RUNNING:
                return NodeStatus.RUNNING
            else:
                self.current += 1
        self.current = 0
        return NodeStatus.FAILURE
