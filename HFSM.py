
from abc import ABC, abstractmethod
from inspect import isabstract
class HFSM():
    def __init__(self) -> None:
        self.root = self.give_me_root_state()()
        #the executing leaf node
        self.activestate = self.root
        
    def setup(self):
        while len(self.activestate.children)>0:
            self.activestate=self.activestate.children[0]
            
    def Update(self,input):
        self.HandleTransition(input)
        self.activestate.Update(input)
        
    def HandleTransition(self,input):
        self.activestate.HandleTransition(input)
    
    def SetActiveState(self,state=None):
        if state:
            self.activestate = state
        else:
            while len(self.activestate.children)>0:
                self.activestate = self.activestate.children[0]
        
    class State(ABC):
        def __init__(selff,name='state',parent=None,children=[],transitions=[],outer_class=None):
            selff.name=name
            selff.currentsubstate=None
            selff.defaultsubstate=None
            selff.parent=None
            selff.children=[]
            selff.transitions=[]
            
            selff.hfsm = outer_class
            
            for child in children:
                if child is not None:
                    selff.AddChild(child)
                    
            if parent is not None:
                parent.AddChild(selff)
            
            for cond,dest in transitions:
                selff.AddTransition(cond,dest)

            
        @abstractmethod
        def OnUpdate(self,input):
            pass  

        def HandleTransition(selff,input):
            root = selff
            while root.parent is not None:
                root.parent.currentsubstate = root
                root = root.parent
                
            while root is not None:
                for cond,dest in root.transitions:
                    #print(type(cond),dest,type(input),cond==input)
                    if cond == input:
                        selff.hfsm.activestate = dest
                        return
                root = root.currentsubstate
                        
                        
        def Update(self,input):
            if self.parent is not None:
                self.parent.Update(input)
            self.OnUpdate(input)
            
        def AddChild(selff,child):
            if selff.currentsubstate is None:
                selff.currentsubstate = child
            selff.children.append(child)
            child.parent=selff

        def AddTransition(self,cond,dest):
            self.transitions.append((cond,dest))
            
    def give_me_state(outer_class):
        class HFSMState(outer_class.State):
            def __init__(self,**kwargs):
                super().__init__(**kwargs)
                self.hfsm = outer_class
        return HFSMState
                
    def give_me_root_state(outer_class):
        class RootState(outer_class.give_me_state()):
            def OnUpdate(self, input):
                print('root')
        return RootState

if __name__=='__main__':
    #create HFSM instance
    hfsm = HFSM()
    attackhfsm = HFSM()
    hfsms = [hfsm,attackhfsm]
    #define states
    class CustomState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('custom')
            
    class MoveState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('move')
    class IdleState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('idle')
            
    class SitState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('sit')
    class SleepState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('sleep')
    class SwimState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('swim')
    class FlyState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('fly')
    class RunState(hfsm.give_me_state()):
        def OnUpdate(self,input):
            print('run')
            
    class AttackState(attackhfsm.give_me_state()):
        def OnUpdate(self,input):
            print('attack')
            
    #instantiate states
    custom = CustomState(parent=hfsm.root)
    move =  MoveState(parent=hfsm.root)
    idle = IdleState(parent=hfsm.root)
    
    sit = SitState(parent=idle)
    sleep = SleepState(parent=idle)
    
    s = SwimState(parent = move)
    r = RunState(parent = move)
    f = FlyState(parent = move)
    
    atk = AttackState(parent = attackhfsm.root)
    #set up transitions
    idle.AddTransition('f',f)
    move.AddTransition('s',sit)
    hfsm.root.AddTransition('v',s)
    
    #set active state
    hfsm.SetActiveState(custom)
    attackhfsm.SetActiveState()
   
    #check to make sure inheritance issue is fixed. should return true
    print(isinstance(s,hfsm.State))

    from pynput import keyboard

    def on_press(key):
        try:
            print(key)
            hfsm.Update(key.char)
            attackhfsm.Update(key.char)
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

            