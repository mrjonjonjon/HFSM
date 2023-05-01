
from abc import ABC, abstractmethod
from inspect import isabstract
class HFSM():
    def __init__(self) -> None:
        self.root = self.RootState()
        self.activestate = self.root
        
    def setup(self):
        while len(self.activestate.children)>0:
            self.activestate=self.activestate.children[0]
            
    def Update(self,input):
        self.HandleTransition(input)
        self.activestate.Update(input)
        
    def HandleTransition(self,input):
        self.activestate.HandleTransition(input)

    class State(ABC):
        def __init__(self,parent=None,children=[],transitions=[],name='state',hfsm=None):
            self.name=name
            self.currentsubstate=None
            self.defaultsubstate=None
            self.parent=None
            self.children=[]
            self.transitions=[]
            
            self.hfsm = hfsm
            
            for child in children:
                if child is not None:
                    self.AddChild(child)
                    
            if parent is not None:
                parent.AddChild(self)
            
            for cond,dest in transitions:
                self.AddTransition(cond,dest)

            
        @abstractmethod
        def OnUpdate(self,input):
            pass  

        def HandleTransition(self,input):
            root = self
            while root.parent is not None:
                root.parent.currentsubstate = root
                root = root.parent
                
            while root is not None:
                for cond,dest in root.transitions:
                    #print(type(cond),dest,type(input),cond==input)
                    if cond == input:
                        self.hfsm.activestate = dest
                        return
                root = root.currentsubstate
                        
                        
        def Update(self,input):
            if self.parent is not None:
                self.parent.Update(input)
            self.OnUpdate(input)
            
        def AddChild(self,child):
            if self.currentsubstate is None:
                self.currentsubstate = child
            self.children.append(child)
            child.parent=self

        def AddTransition(self,cond,dest):
            self.transitions.append((cond,dest))
            

    class RootState(State):
        def OnUpdate(self,input):
            print('root') 
                
    class MoveState(State):
        def OnUpdate(self,input):
            print('moving')
        
    class RunState(State):
        def OnUpdate(self,input):
            print('running')

    class JumpState(State):
        def OnUpdate(self,input):
            print('jumping')
            
    class SwimState(State):
        def OnUpdate(self, input):
            print('swimming')
        
    class FlyState(State):
        def OnUpdate(self, input):
            print('flying')
            
    class IdleState(State):
        def OnUpdate(self, input):
            print('idle')
        
    class SitState(State):
        def OnUpdate(self, input):
            print('sitting')
            
    class SleepState(State):
        def OnUpdate(self, input):
            print('sleeping')
        
        
        







if __name__=='__main__':
    hfsm = HFSM()
    move = hfsm.MoveState(parent=hfsm.activestate, hfsm=hfsm)
    idle = hfsm.IdleState(parent=hfsm.activestate,hfsm=hfsm)
    
    sit = hfsm.SitState(parent=idle,hfsm=hfsm)
    sleep = hfsm.SleepState(parent=idle,hfsm=hfsm)
    

    s = hfsm.SwimState(parent=move,hfsm=hfsm)
    r = hfsm.RunState(parent = move,hfsm=hfsm)
    f = hfsm.FlyState(parent = move,hfsm=hfsm)
    
    idle.AddTransition('f',f)
    move.AddTransition('s',sit)
    hfsm.root.AddTransition('v',s)
    
    hfsm.setup()




    from pynput import keyboard

    def on_press(key):
        try:
            print(key)
            hfsm.Update(key.char)
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

            