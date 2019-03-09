from owlready2 import *
# onto_path.append("/Users/lauramiron/Desktop/CS270/project")
# onto = get_ontology("http://vivoweb.org/ontology/core")
# onto = get_ontology("vivo-core-public-1.4.owl")
# onto = get_ontology("merged-research-mentor.owl")
onto = get_ontology("Untitled-1.owl")
# onto = get_ontology("http://edamontology.org/EDAM_1.21.owl")
# onto = get_ontology("https://duraspace.org/archive/vivo/vivo.owl")
# print(onto.base_iri)
onto.load(only_local=True,fileobj=open("Untitled-1.owl",'rb'))
# onto.load()
# onto.load()

# import pdb
print(onto.base_iri)
print(onto.base_iri.endswith('#'))
print(onto.imported_ontologies)
imp_onto = onto.imported_ontologies[0]
for c in imp_onto.properties():
    print(c)
    print(type(c.name))
    c.python_name = python_name(c.name)
#     pdb.set_trace()
#     print(get_namespace(c,onto.base_iri))
#     break

for c in imp_onto.classes():
#     print(c)
#     print(c.name)
    print(type(c.python_name))
    print(c.python_name)

# with onto:
# #     RA = onto.ResearchArea("Biochemistry")
#     test_indi = onto.core.FacultyMember("StevenArtandi")
#     test_indi.lastName = "Artandi"
#     test_indi.firstName = "Steven"
# #     test_indi.hasResearchArea = "RA"
#     onto.save()