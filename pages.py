from owlready2 import *
from tkinter import *

class ResearchMentorApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        # style
        # self._bstyle = 'TButton'
        # self._fstyle = 'TFrame'
        # self._lstyle = 'TLabel'
        # self.s.configure('TLabel',foreground='green')
        # self.s.configure('TFrame',bg='red')

        # preload ontology individuals
        self.load_ontology()
        self.load_individuals()
        
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0,column=0,sticky=N+S+E+W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def load_individuals(self):
        self.faculty_members = self.vivoNS.FacultyMember.instances()
        self.undergraduate_students = self.vivoNS.UndergraduateStudent.instances()
        self.doctoral_students = self.onto.DoctoralStudent.instances()
        self.organizations = {}
        for org in self.foafNS.Organization.instances():
            self.organizations[org.name] = org
        self.documents = self.vivoNS.AcademicArticle.instances()
        self.mesh_terms = {}
        for mesh_i in self.onto.Mesh.instances():
            if len(mesh_i.label)>0:
                self.mesh_terms[mesh_i.label[0]] = mesh_i

    def load_ontology(self):
        self.onto = get_ontology('main-ResearchMentorOntology.owl')
        self.vivoNS = self.onto.get_namespace("http://vivoweb.org/ontology/core")
        self.meshNS = self.onto.get_namespace("http://phenomebrowser.net/ontologies/mesh/mesh.owl#")
        self.foafNS = self.onto.get_namespace("http://xmlns.com/foaf/0.1/")
        self.onto.load()
    
    def get_departments(self, onto, vivoNS):
        res = onto.search(type=vivoNS.Division)
        return res
           

class HomePage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bg='grey')
        master.title('Research Mentor Ontology 1.0')
        for i in range(0,3):
            self.columnconfigure(i,weight=1)
            self.rowconfigure(i,weight=1)

        main_frame = Frame(self,bg='white',borderwidth=10, relief='solid',pady=20)
        main_frame.grid(row=1,column=1,sticky=N+E+S+W)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1,weight=1)

        label = Label(main_frame, text="Welcome to the Research Mentor Ontology",font=("Helvetica", 24), fg='green')
        label.grid(row=0,column=1,padx=10, columnspan=2, sticky=N+S+E+W)

        label = Label(main_frame, text="Choose an option below to search for research mentors at Stanford University",font=("Helvetica", 15))
        label.grid(row=1,column=1,padx=10, columnspan=2, sticky=N+S+E+W)

        button = Button(main_frame, text="Search by Affliation", fg='red', padx=5, pady=5, command=lambda: master.switch_frame(AffiliationSearchPage))
        button.grid(row=2,column=1,sticky=N)
        
        button = Button(main_frame, text="Search by Mesh", fg='red', padx=5, pady=5, command=lambda: master.switch_frame(MeshSearchPage))
        button.grid(row=2,column=2,sticky=N)
        
class MeshSearchPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        MESH_OPTIONS = list(master.mesh_terms.keys())
        mesh_var = StringVar(master)
        mesh_var.set(MESH_OPTIONS[0])

        button = Button(self, text="Search", bg='red', command=lambda: self.search_mesh_term(master,mesh_var.get()))
        button.grid(row=0,column=1,sticky="nsew")

        mesh_option = OptionMenu(self, mesh_var, *MESH_OPTIONS)
        mesh_option.grid(column=0,row=0)
        
    def search_mesh_term(self,master,term):
        fac_results = []
        mesh_i = master.mesh_terms[term]
        for fac in master.faculty_members:
            if mesh_i in fac.hasResearchArea:
                fac_results.append(fac)
        print(fac_results)
        

class AffiliationSearchPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        DEPART_OPTIONS = list(master.organizations.keys())
        depart_var = StringVar(master)
        depart_var.set(DEPART_OPTIONS[0])

        button = Button(self, text="Search", bg='red', command=lambda: self.search_organization(master,depart_var.get()))
        button.grid(row=0,column=1,sticky="nsew")
        back_button = Button(self, text="<< Back", bg='red', command=lambda: master.switch_frame(HomePage))
        back_button.grid(row=0,column=5)

        mesh_option = OptionMenu(self, depart_var, *DEPART_OPTIONS)
        mesh_option.grid(column=0,row=0)
        
    def search_organization(self,master,org):
        org_results = []
        org_i = master.organizations[org]
        for fac in master.faculty_members:
            if org_i in fac.currentMemberOf:
                org_results.append(org)
        print(org_results)