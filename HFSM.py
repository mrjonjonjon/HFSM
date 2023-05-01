
from abc import ABC, abstractmethod
from inspect import isabstract
class HFSM():
    def __init__(self) -> None:
        self.root = self.give_me_root_state()()
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
            
    def give_me_state(outer_class,**kwargs):
        class HFSMState(outer_class.State):
            def __init__(self):
                super().__init__(**kwargs)
                self.hfsm = outer_class
        return HFSMState
                
    def give_me_root_state(outer_class,**kwargs):
        class RootState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('root')
        return RootState

    def give_move_state(outer_class,**kwargs):
        class MoveState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('moving')
        return MoveState

    def give_run_state(outer_class,**kwargs):
        class RunState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('running')
        return RunState

    def give_jump_state(outer_class,**kwargs):
        class JumpState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('jumping')
        return JumpState

    def give_swim_state(outer_class,**kwargs):
        class SwimState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('swimming')
        return SwimState

    def give_fly_state(outer_class,**kwargs):
        class FlyState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('flying')
        return FlyState

    def give_idle_state(outer_class,**kwargs):
        class IdleState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('idle')
        return IdleState

    def give_sit_state(outer_class,**kwargs):
        class SitState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('sitting')
        return SitState

    def give_sleep_state(outer_class,**kwargs):
        class SleepState(outer_class.give_me_state(**kwargs)):
            def OnUpdate(self, input):
                print('sleeping')
        return SleepState

        







if __name__=='__main__':
    hfsm = HFSM()
    move = hfsm.give_move_state(parent=hfsm.root)()
    idle = hfsm.give_idle_state(parent=hfsm.root)()
    
    sit = hfsm.give_sit_state(parent=idle)()
    sleep = hfsm.give_sleep_state(parent=idle)()
    

    s = hfsm.give_swim_state(parent = move)()
    r = hfsm.give_run_state(parent = move)()
    f = hfsm.give_fly_state(parent = move)()
    
    idle.AddTransition('f',f)
    move.AddTransition('s',sit)
    hfsm.root.AddTransition('v',s)
    
    hfsm.setup()

    print(isinstance(s,hfsm.State))

    from pynput import keyboard

    def on_press(key):
        try:
            print(key)
            hfsm.Update(key.char)
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

            