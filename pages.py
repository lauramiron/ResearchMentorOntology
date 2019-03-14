from owlready2 import *
from tkinter import *
# from tkinter.ttk import *
class ResearchMentorApp(Tk):
    def __init__(self):
        # style
#         s = Style()
#         s.theme_use('clam')
        
        # preload ontology individuals
        self.load_ontology()
        self.load_individuals()
        
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomePage)
    
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0,column=0)

    def load_individuals(self):
        return
# #         self.faculty_members = self.vivoNS.FacultyMember.instances()
# #         self.undergraduate_students = self.vivoNS.UndergraduateStudent.instances()
# #         self.doctoral_students = self.onto.DoctoralStudent.instances()
#         self.organizations = {}
#         for org in self.foafNS.Organization.instances():
#             self.organizations[org.name] = org
# #         self.documents = self.vivoNS.AcademicArticle.instances()
#         self.mesh_terms = {}
#         for mesh_i in self.onto.Mesh.instances():
#             if len(mesh_i.label)>0:
#                 self.mesh_terms[mesh_i.label[0]] = mesh_i

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
        Frame.__init__(self,master)
        
        Label(self, text="Welcome to the Research Mentor Ontology").grid(row=0,column=0,columnspan=2)
        
        button = Button(self, text="Search by Affliation", fg="red", command=lambda: master.switch_frame(AffiliationSearchPage))
        button.grid(row=1,column=0)
        
        button = Button(self, text="Search by Mesh", fg="red", command=lambda: master.switch_frame(MeshSearchPage))
        button.grid(row=1,column=1)
        
class MeshSearchPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        MESH_OPTIONS = list(master.mesh_terms.keys())
        mesh_var = StringVar(master)
        mesh_var.set(MESH_OPTIONS[0])

        button = Button(self, text="Search", fg="red", command=lambda: self.search_mesh_term(master,mesh_var.get()))
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

        button = Button(self, text="Search", fg="red", command=lambda: self.search_organization(master,depart_var.get()))
        button.grid(row=0,column=1,sticky="nsew")
        back_button = Button(self, text="<< Back", fg="red", command=lambda: master.switch_frame(HomePage))
        back_button.grid(row=0,column=5)

        mesh_option = OptionMenu(self, depart_var, *DEPART_OPTIONS)
        mesh_option.grid(column=0,row=0)
        
    def search_organization(self,master,org):
        org_results = []
        org_i = master.organizations[org]
        for fac in master.faculty_members:
            if org_i in fac.currentMemberOf:
                fac_results.append(org)
        print(fac_results)