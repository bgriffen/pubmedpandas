import pandas as pd

def load_year(db,year):
    q = db.PaperDB.select().where(db.PaperDB.pubyear == year) 
    papers = pd.DataFrame(list(q.dicts()))
    return papers

def load_all(db):
    q = db.PaperDB.select()
    papers = pd.DataFrame(list(q.dicts()))
    return papers

def check_first_last_affiliation(row,string_contains):
    if string_contains in row[0] or string_contains in row[-1]:
        return True
    else:
        return False

def filter_paper_contains(pm,string_contains,first_and_last_affiliation=True):
    print("Getting affiliates from %s..." % string_contains)

    if first_and_last_affiliation:
        m_papers = pm.papers_period['affiliations'].str.split(";").apply(check_first_last_affiliation,args=(string_contains,))
    else:
        m_papers = pm.papers_period['affiliations'].str.contains(string_contains)

    m_journal = pm.papers_period['journal_lower'].apply(lambda x: any([k.lower() == x for k in jrl.filter_journals]))
    m_combined = (m_papers & m_journal)
    if m_combined.any():
        papers = pm.papers_period[m_combined]
        vectors = pm.vectors_period.loc[papers.index]
        dfout = pm.calculate_similarities(papers,vectors)
    else:
        dfout = pd.DataFrame()
    return dfout
