from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from queue import PriorityQueue
from json import dumps
class Puzzle:
    goal_state=[]
    heuristic=None
    evaluation_function=None
    needs_hueristic=False
    def set_goal_state(goal):
        Puzzle.goal_state=goal
    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost


    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution
class A_star:
    def Astar_search(initial_state,goal_state):
        count=0
        explored=[]
        Puzzle.set_goal_state(goal_state)
        start_node=Puzzle(initial_state,None,None,0,True)
        q = PriorityQueue()
        q.put((start_node.evaluation_function,count,start_node))

        while not q.empty():
            node=q.get()
            node=node[2]
            explored.append(node.state)
            if node.goal_test():
                return node.find_solution()

            children=node.generate_child()
            for child in children:
                if child.state not in explored:
                    count += 1
                    q.put((child.evaluation_function,count,child))
        return -1
def check_values(curr,goal):
    for i in curr:
        if curr.count(i)>1:
            return False
    for i in goal:
        if goal.count(i)>1:
            return False
    return True
def index(request):
    curr=[request.POST.get('c1'),
          request.POST.get('c2'),
          request.POST.get('c3'),
          request.POST.get('c4'),
          request.POST.get('c5'),
          request.POST.get('c6'),
          request.POST.get('c7'),
          request.POST.get('c8'),
          request.POST.get('c9')]   
    goal=[request.POST.get('g1'),
          request.POST.get('g2'),
          request.POST.get('g3'),
          request.POST.get('g4'),
          request.POST.get('g5'),
          request.POST.get('g6'),
          request.POST.get('g7'),
          request.POST.get('g8'),
          request.POST.get('g9')] 
    astar=[]
    fun=""
    alert=""
    if request.method=='POST':
        curr=[int(i) for i in curr]
        goal=[int(i) for i in goal]
        if check_values(curr,goal):
            Puzzle.num_of_instances = 0
            astar = A_star.Astar_search(curr,goal)
            fun="view();"
        else:
            alert="warning();"
    template = loader.get_template('index.html')
    data={ 
      'astar':astar,
      'curr':curr
    }
    data=dumps(data)
    return HttpResponse(template.render({'data':data,'fun':fun,'warning':alert},request))