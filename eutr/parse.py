from datetime import datetime
from lxml import etree
from pprint import pprint

import model

SRC = 'http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=NEW'
_NS2="http://www.w3.org/1999/xlink"
_NS="http://intragate.ec.europa.eu/transparencyregister/intws/20090623_new"
_SI="http://www.w3.org/2001/XMLSchema-instance"
NS = '{%s}' % _NS
NS2 = '{%s}' % _NS2
SI = '{%s}' % _SI

def dateconv(ds):
    return datetime.strptime(ds, "%Y-%m-%dT%H:%M:%S.%f+01:00")

def parse(file_name, handle_func):
    data = []
    doc = etree.parse(file_name)
    for rep_el in doc.findall('//' + NS + 'interestRepresentative'):
        rep = {}
        rep['identificationCode'] = rep_el.findtext(NS + 'identificationCode')
        rep['status'] = rep_el.findtext(NS + 'status')
        rep['registrationDate'] = rep_el.findtext(NS + 'registrationDate')
        rep['lastUpdateDate'] = rep_el.findtext(NS + 'lastUpdateDate')
        rep['legalStatus'] = rep_el.findtext(NS + 'legalStatus')
        rep['acronym'] = rep_el.findtext(NS + 'acronym')
        rep['originalName'] = rep_el.findtext('.//' + NS + 'originalName')
        el = rep_el.find(NS + 'webSiteURL')
        rep['webSiteURL'] = el.get(NS2 + 'href') if el is not None else None
        rep['mainCategory'] = rep_el.findtext('.//' + NS + 'mainCategory')
        rep['subCategory'] = rep_el.findtext('.//' + NS + 'subCategory')

        rep['legalPersonTitle'] = rep_el.findtext(NS + 'legal/' + NS + 'title')
        rep['legalPersonFirstName'] = rep_el.findtext(NS + 'legal/' + NS +
                'firstName')
        rep['legalPersonLastName'] = rep_el.findtext(NS + 'legal/' + NS +
                'lastName')
        rep['legalPersonPosition'] = rep_el.findtext(NS + 'legal/' + NS +
                'position')
        rep['headPersonTitle'] = rep_el.findtext(NS + 'head/' + NS + 'title')
        rep['headPersonFirstName'] = rep_el.findtext(NS + 'head/' + NS +
                'firstName')
        rep['headPersonLastName'] = rep_el.findtext(NS + 'head/' + NS +
                'lastName')
        rep['headPersonPosition'] = rep_el.findtext(NS + 'head/' + NS +
                'position')

        rep['contactStreet'] = rep_el.findtext(NS + 'contactDetails/' + NS + 'street')
        rep['contactNumber'] = rep_el.findtext(NS + 'contactDetails/' + NS + 'number')
        rep['contactPostCode'] = rep_el.findtext(NS + 'contactDetails/' + NS
                + 'postCode')
        rep['contactTown'] = rep_el.findtext(NS + 'contactDetails/' + NS
                + 'town')
        rep['contactCountry'] = rep_el.findtext(NS + 'contactDetails/' + NS
                + 'country')
        rep['contactIndicPhone'] = rep_el.findtext(NS + 'contactDetails//' + NS
                + 'indicPhone')
        rep['contactIndicFax'] = rep_el.findtext(NS + 'contactDetails//' + NS
                + 'indicFax')
        rep['contactFax'] = rep_el.findtext(NS + 'contactDetails//' + NS
                + 'fax')
        rep['contactPhone'] = rep_el.findtext(NS + 'contactDetails//' + NS
                + 'phoneNumber')
        rep['contactMore'] = rep_el.findtext(NS + 'contactDetails/' + NS
                + 'moreContactDetails')
        rep['goals'] = rep_el.findtext(NS + 'goals')
        rep['networking'] = rep_el.findtext(NS + 'networking')
        rep['activities'] = rep_el.findtext(NS + 'activities')
        rep['codeOfConduct'] = rep_el.findtext(NS + 'codeOfConduct')
        rep['members'] = rep_el.findtext(NS + 'members')
        rep['actionFields'] = []
        for field in rep_el.findall('.//' + NS + 'actionField/' + NS +
                'actionField'):
            rep['actionFields'].append(field.text)
        rep['interests'] = []
        for interest in rep_el.findall('.//' + NS + 'interest/' + NS +
                'name'):
            rep['interests'].append(interest.text)
        rep['numberOfNaturalPersons'] = rep_el.findtext(NS + 'structure/' + NS
                + 'numberOfNaturalPersons')
        rep['numberOfOrganisations'] = rep_el.findtext(NS + 'structure/' + NS
                + 'numberOfOrganisations')
        rep['countryOfMembers'] = []
        el = rep_el.find(NS + 'structure/' + NS + 'countries')
        if el is not None:
            for country in el.findall('.//' + NS + 'country'):
                rep['countryOfMembers'].append(country.text)
        rep['organisations'] = []
        el = rep_el.find(NS + 'structure/' + NS + 'organisations')
        if el is not None:
            for org_el in el.findall(NS + 'organisation'):
                org = {}
                org['name'] = org_el.findtext(NS + 'name')
                org['numberOfMembers'] = org_el.findtext(NS + 'numberOfMembers')
                rep['organisations'].append(org)

        fd_el = rep_el.find(NS + 'financialData')
        # TODO: in the future, store each financial report on its own.
        rep['fdStartDate'] = fd_el.findtext(NS + 'startDate')
        rep['fdEndDate'] = fd_el.findtext(NS + 'endDate')
        rep['fdEurSourcesProcurement'] = fd_el.findtext(NS + 'eurSourcesProcurement')
        rep['fdEurSourcesGrants'] = fd_el.findtext(NS + 'eurSourcesGrants')
        fi = fd_el.find(NS + 'financialInformation')
        rep['fdType'] = fi.get(SI + 'type')
        #import ipdb; ipdb.set_trace()
        rep['fdTotalBudget'] = fi.findtext('.//' + NS +
            'totalBudget')
        rep['fdPublicFinancingTotal'] = fi.findtext('.//' + NS +
            'totalPublicFinancing')
        rep['fdPublicFinancingNational'] = fi.findtext('.//' + NS +
            'nationalSources')
        rep['fdPublicFinancingInfranational'] = fi.findtext('.//' + NS +
            'infranationalSources')
        cps = fi.find('.//' + NS + 'customisedPublicSources')
        rep['fdPublicCustomized'] = []
        if cps is not None:
            for src_el in cps.findall(NS + 'customizedSource'):
                src = {}
                src['name'] = src_el.findtext(NS + 'name')
                src['amount'] = src_el.findtext(NS + 'amount')
                rep['fdPublicCustomized'].append(src)
        rep['fdOtherSourcesTotal'] = fi.findtext('.//' + NS +
            'totalOtherSources')
        rep['fdOtherSourcesDonation'] = fi.findtext('.//' + NS +
            'donation')
        rep['fdOtherSourcesContributions'] = fi.findtext('.//' + NS +
            'contributions')
        # TODO customisedOther
        cps = fi.find('.//' + NS + 'customisedOther')
        rep['fdOtherCustomized'] = []
        if cps is not None:
            for src_el in cps.findall(NS + 'customizedSource'):
                src = {}
                src['name'] = src_el.findtext(NS + 'name')
                src['amount'] = src_el.findtext(NS + 'amount')
                rep['fdOtherCustomized'].append(src)
        
        rep['fdDirectRepCostsMin'] = fi.findtext('.//' + NS +
            'directRepresentationCosts//' + NS + 'min')
        rep['fdDirectRepCostsMax'] = fi.findtext('.//' + NS +
            'directRepresentationCosts//' + NS + 'max')
        rep['fdCostMin'] = fi.findtext('.//' + NS +
            'cost//' + NS + 'min')
        rep['fdCostMax'] = fi.findtext('.//' + NS +
            'cost//' + NS + 'max')
        rep['fdCostAbsolute'] = fi.findtext('.//' + NS +
            'cost//' + NS + 'absoluteAmount')
        rep['fdTurnoverMin'] = fi.findtext('.//' + NS +
            'turnover//' + NS + 'min')
        rep['fdTurnoverMax'] = fi.findtext('.//' + NS +
            'turnover//' + NS + 'max')
        rep['fdTurnoverAbsolute'] = fi.findtext('.//' + NS +
            'turnover//' + NS + 'absoluteAmount')
        tb = fi.find(NS + 'turnoverBreakdown')
        rep['fdTurnoverBreakdown'] = []
        if tb is not None:
            for range_ in tb.findall(NS + 'customersGroupsInAbsoluteRange'):
                max_ = range_.findtext('.//' + NS + 'max')
                min_ = range_.findtext('.//' + NS + 'min')
                for customer in range_.findall('.//' + NS + 'customer'):
                    rep['fdTurnoverBreakdown'].append({
                        'name': customer.findtext(NS + 'name'),
                        'min': min_,
                        'max': max_
                        })
            for range_ in tb.findall(NS + 'customersGroupsInPercentageRange'):
                # FIXME: I hate political compromises going into DB design 
                # so directly.
                max_ = range_.findtext('.//' + NS + 'max')
                if max_:
                    max_ = float(max_)/100.0 * \
                            float(rep['fdTurnoverAbsolute'] or
                                    rep['fdTurnoverMax'] or rep['fdTurnoverMin'])
                min_ = range_.findtext('.//' + NS + 'min')
                if min_:
                    min_ = float(min_)/100.0 * \
                            float(rep['fdTurnoverAbsolute'] or
                                    rep['fdTurnoverMin'] or rep['fdTurnoverMax'])
                for customer in range_.findall('.//' + NS + 'customer'):
                    rep['fdTurnoverBreakdown'].append({
                        'name': customer.findtext(NS + 'name'),
                        'min': min_,
                        'max': max_
                        })
        #pprint(rep)
        handle_func(rep)
        data.append(rep)
    return data


def load(rep):
    r = model.Representative()
    r.identificationCode = rep['identificationCode']
    r.status = rep['status']
    r.registrationDate = dateconv(rep['registrationDate'])
    r.lastUpdateDate = dateconv(rep['lastUpdateDate'])
    r.legalStatus = rep['legalStatus']
    r.acronym = rep['acronym']
    r.originalName = rep['originalName']
    r.name = rep['originalName']
    r.webSiteURL = rep['webSiteURL']
    r.mainCategory = rep['mainCategory']
    r.subCategory = rep['subCategory']
    r.goals = rep['goals']
    r.networking = rep['networking']
    r.activities = rep['activities']
    r.codeOfConduct = rep['codeOfConduct']
    r.members = rep['members']

    r.legalPersonTitle = rep['legalPersonTitle']
    r.legalPersonFirstName = rep['legalPersonFirstName']
    r.legalPersonLastName = rep['legalPersonLastName']
    r.legalPersonPosition = rep['legalPersonPosition']
    
    r.headPersonTitle = rep['headPersonTitle']
    r.headPersonFirstName = rep['headPersonFirstName']
    r.headPersonLastName = rep['headPersonLastName']
    r.headPersonPosition = rep['headPersonPosition']

    r.contactStreet = rep['contactStreet']
    r.contactNumber = rep['contactNumber']
    r.contactPostCode = rep['contactPostCode']
    r.contactTown = rep['contactTown']
    r.contactCountry = model.Country.have(rep['contactCountry'])
    r.contactIndicPhone = rep['contactIndicPhone']
    r.contactPhone = rep['contactPhone']
    r.contactIndicFax = rep['contactIndicFax']
    r.contactFax = rep['contactFax']
    r.contactMore = rep['contactMore']

    r.interests = map(model.Interest.have, rep['interests'])
    r.actionFields = map(model.ActionField.have, rep['actionFields'])
    r.countryOfMembers = map(model.Country.have, rep['countryOfMembers'])
    r.memberships = [model.Organisation.have(o['name'], \
        members=o['numberOfMembers']) for o in rep['organisations']]
    model.db.session.add(r)
    
    fd = model.FinancialData()
    fd.representative = r
    fd.type = rep['fdType']
    fd.startDate = dateconv(rep['fdStartDate'])
    fd.endDate = dateconv(rep['fdEndDate'])
    fd.eurSourcesProcurement = rep['fdEurSourcesProcurement']
    fd.eurSourcesGrants = rep['fdEurSourcesGrants']
    fd.totalBudget = rep['fdTotalBudget']
    fd.publicFinancingTotal = rep['fdPublicFinancingTotal']
    fd.publicFinancingNational = rep['fdPublicFinancingNational']
    fd.publicFinancingInfranational = rep['fdPublicFinancingInfranational']
    fd.otherSourcesTotal = rep['fdOtherSourcesTotal']
    fd.otherSourcesDonation = rep['fdOtherSourcesDonation']
    fd.otherSourcesContributions = rep['fdOtherSourcesContributions']
    fd.directRepCostsMin = rep['fdDirectRepCostsMin']
    fd.directRepCostsMax = rep['fdDirectRepCostsMax']
    fd.costMin = rep['fdCostMin']
    fd.costMax = rep['fdCostMax']
    fd.costAbsolute = rep['fdCostAbsolute']
    fd.turnoverMin = rep['fdTurnoverMin']
    fd.turnoverMax = rep['fdTurnoverMax']
    fd.turnoverAbsolute = rep['fdTurnoverAbsolute']

    for src in rep['fdPublicCustomized']:
        fs = model.FinancialSource()
        fs.financialData = fd
        fs.public = True
        fs.name = src['name']
        fs.amount = src['amount']
        model.db.session.add(fs)

    for src in rep['fdOtherCustomized']:
        fs = model.FinancialSource()
        fs.financialData = fd
        fs.public = False
        fs.name = src['name']
        fs.amount = src['amount']
        model.db.session.add(fs)

    for bd in rep['fdTurnoverBreakdown']:
        t = model.Turnover()
        t.financialData = fd
        t.representative = r
        t.customer = model.Organisation.have(bd['name'])
        t.min = bd['min']
        t.max = bd['max']
        model.db.session.add(t)
    
    print r.id
    model.db.session.add(fd)
    model.db.session.commit()

if __name__ == '__main__':
    #file_name = '../full_export_new.xml'
    file_name = SRC
    model.db.drop_all()
    model.db.create_all()
    data = parse(file_name, load)
    #data = parse(file_name, lambda x: x)
    #print len(data)
    #print len([d['identificationCode'] for d in data])
    #model.db.session.commit()


