def init_webscraping():
    import time, pickle, csv
    from selenium import webdriver
    
def init_onto():
    import owlready2 as ow
    import pandas as pd
    onto = ow.get_ontology(main_onto_name)
    vivoNS = onto.get_namespace("http://vivoweb.org/ontology/core")
    onto.load()
    return onto, vivoNS