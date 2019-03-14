from owlready2 import *
from tkinter import *
from tutils import *

class ResearchMentorApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("800x600")
        self._tfont = "Courier New"
        self._font = "Helvetica"
        self._bcolor = "red"
        self._bpadx = 5
        self._bpady = 5
        self._backtext = "<< Back to Home"
        self._bgcolor = "grey"

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
            if org.hasCurrentMember and len(org.hasCurrentMember) > 0:
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

    def make_button(self,frame,text,command):
        b = Button(frame,text=text,bg=self._bcolor, font=(self._font, 12, 'bold'), padx=self._bpadx, pady=self._bpady, command=command)
        return b
    
    def make_page_title(self,frame,text):
        l = Label(frame,text=text,font=(self._font,18,'bold'), fg='green', padx=10, pady=10)
        return l
    
    def make_label(self,frame,text):
        l = Label(frame,text=text,font=(self._font,14), padx=5, pady=5)
        return l

    def make_main_frame(self,frame):
        for i in range(0,3):
            frame.columnconfigure(i,weight=1)
            frame.rowconfigure(i,weight=1)
        main_frame = Frame(frame,pady=20)
        main_frame.grid(row=1,column=1,sticky=N+E+S+W)
        return main_frame

    def make_heading_label(self,frame,text):
        l = Label(frame,text=text, font=(self._font,14,'bold'), anchor='w')
        return l

    def make_data_label(self,frame,text):     
        l = Label(frame,text=text, font=(self._font,14), anchor='w')
        return l

class HomePage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bg=master._bgcolor)
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

        label = Label(main_frame, text="Welcome to the Research Mentor Ontology",font=(master._tfont,24), fg='green')
        label.grid(row=0,column=1,padx=10, columnspan=2, sticky=N+S+E+W)

        label = Label(main_frame, text="Choose an option below to search for research mentors at Stanford University",font=(master._font, 15))
        label.grid(row=1,column=1,padx=10, columnspan=2, sticky=N+S+E+W)

        button = master.make_button(main_frame, text="Search by Affliation",command=lambda: master.switch_frame(AffiliationSearchPage))
        button.grid(row=2,column=1,sticky=N)
        
        button = master.make_button(main_frame, text="Search by Mesh", command=lambda: master.switch_frame(MeshSearchPage))
        button.grid(row=2,column=2,sticky=N)
        
class MeshSearchPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bg=master._bgcolor)

        MESH_OPTIONS = list(master.mesh_terms.keys())
        mesh_var = StringVar(master)
        mesh_var.set(MESH_OPTIONS[0])
        
        back_button = master.make_button(self,text=master._backtext, command=lambda: master.switch_frame(HomePage))
        back_button.grid(row=0,column=5)

        button = master.make_button(self, text="Search", command=lambda: self.search_mesh_term(master,mesh_var.get()))
        button.grid(row=0,column=1,sticky="n")

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
        Frame.__init__(self,master,bg=master._bgcolor)
        self.results_frame = None
        main_frame = master.make_main_frame(self)

        DEPART_OPTIONS = list(master.organizations.keys())
        depart_var = StringVar(master)
        depart_var.set(DEPART_OPTIONS[0])

        for i in range(0,4):
            main_frame.columnconfigure(i, weight=1)
            main_frame.rowconfigure(i, weight=1)

        l = master.make_page_title(main_frame,"Search Faculty by Affiliation")
        l.grid(row=0,column=1,columnspan=2,sticky='nswe')

        l = master.make_label(main_frame,"Select an academic department, medical school division, or university research center from the dropdown below, \nand click 'search' to display all Stanford faculty members currently affiliated with this organization")
        l.grid(row=1,column=1,columnspan=2, sticky='nswe')
        
        mesh_option = OptionMenu(main_frame, depart_var, *DEPART_OPTIONS)
        mesh_option.grid(column=1,columnspan=2, row=2)
        
        button = master.make_button(main_frame,"Search",lambda: self.search_organization(master,depart_var.get()))
        button.grid(row=3,column=1)

        back_button = master.make_button(main_frame, text=master._backtext, command=lambda: master.switch_frame(HomePage))
        back_button.grid(row=3,column=2)


        
    def search_organization(self,master,org):
        org_results = []
        org_i = master.organizations[org]
        for fac in master.faculty_members:
            if org_i in fac.currentMemberOf:
                org_results.append(fac)
        self.results = org_results
        if self.results_frame:
            self.results_frame.destroy()
        self.canvas_frame = make_canvas(self,row=4,column=1,root2=master)
        self.add_search_results(master)


    def add_search_results(self,master):
        for i in range(0,len(self.results)):
            fac = self.results[i]
            f = Frame(self.canvas_frame)
            f.grid(row=i,column=0, sticky='new')
            
            name_text = "{0} {1}".format(fac.firstName, fac.lastName)
            l = Label(f,text=name_text, font=(master._font,14))
            l.grid(row=0,column=0,sticky='nsew')

            affls = fac.currentMemberOf
            if (len(affls)>0): 
                affl_text1 = "Affiliations: "
                affl_text2 =  ", ".join([aff.name for aff in affls])
                l1 = master.make_heading_label(f,text=affl_text1)
                l1.grid(row=1,column=0)
                l2 = master.make_data_label(f,text=affl_text2)
                l2.grid(row=2,column=0)
            
            mentees = fac.mentorOf
            if len(mentees)>0:
                mentee_text1 = "Past and current student research assistants: "
                mentee_text2 = ",".join(["{0} {1}".format(m.firstName, m.lastName) for m in mentees])
                l1 = master.make_heading_label(f,text=mentee_text1)
                l1.grid(row=3,column=0)
                l2 = master.make_data_label(f,text=mentee_text2)

            docs = fac.authorOf
            if (len(docs)>0):
                doc_text = "Published papers: "
                for doc in docs:
                    doc_text += "{0} ({1})\n".format(doc.title,str(doc.year))
                l = master.make_data_label(f,text=doc_text)
                l.grid(row=4,column=0)