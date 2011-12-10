from eutr.core import db, app

class HaveMixin(object):

    @classmethod
    def have(cls, name, **kw):
        e = db.session.query(cls).filter_by(name=name).first()
        if e is None:
            e = cls()
            e.name = name
            db.session.add(e)
        for key, value in kw.items():
            setattr(e, key, value)
        return e


class AsDictMixin(object):

    def as_dict(self, exclude=[]):
        data = {}
        remove = []
        conv = lambda v: v.as_dict_child() if hasattr(v, 'as_dict_child') else v
        for col in self.__mapper__.iterate_properties:
            value = getattr(self, col.key)
            if col.key in exclude: 
                continue
            if isinstance(value, list) or isinstance(value, db.Query):
                value = [conv(v) for v in value]
            else:
                value = conv(value)
            data[col.key] = value
            if hasattr(col, 'local_side'):
                remove.extend([c.name for c in col.local_side])
        return dict([(k, v) for k, v in data.items() if k not in remove])


class Organisation(db.Model, HaveMixin, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': type}

    name = db.Column(db.Unicode)
    members = db.Column(db.Float)

    def as_dict_child(self):
        return {'id': self.id, 'name': self.name}


class Member(Organisation):
    __mapper_args__ = {'polymorphic_identity': 'member'}


class Customer(Organisation):
    __mapper_args__ = {'polymorphic_identity': 'customer'}

    turnoversFor = db.relationship('Turnover',
        primaryjoin='Turnover.customer_id==Customer.id',
        backref='customer', lazy='dynamic')

memberships = db.Table('memberships',
    db.Column('member_id', db.Integer, db.ForeignKey('organisation.id')),
    db.Column('representative_id', db.Integer, db.ForeignKey('organisation.id'))
)

class Country(db.Model, HaveMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

    representativesContacts = db.relationship('Representative',
        backref='contactCountry', lazy='dynamic')

    def as_dict_child(self):
        return self.name


countries_of_members = db.Table('countries_of_members',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('representative_id', db.Integer, db.ForeignKey('organisation.id'))
)

class ActionField(db.Model, HaveMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    
    def as_dict_child(self):
        return self.name

fields = db.Table('fields',
    db.Column('action_field_id', db.Integer, db.ForeignKey('action_field.id')),
    db.Column('representative_id', db.Integer, db.ForeignKey('organisation.id'))
)

class Interest(db.Model, HaveMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    
    def as_dict_child(self):
        return self.name

interests_table = db.Table('interests',
    db.Column('representative_id', db.Integer, db.ForeignKey('organisation.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

class FinancialSource(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    financialData_id = db.Column(db.Integer, db.ForeignKey('financial_data.id'))
    public = db.Column(db.Boolean)
    name = db.Column(db.Unicode)
    amount = db.Column(db.Float, nullable=True)

    def as_dict_child(self):
        return {
            'id': self.id, 
            'public': self.public,
            'name': self.name,
            'amount': self.amount
            }

class Turnover(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    representative_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    financialData_id = db.Column(db.Integer, db.ForeignKey('financial_data.id'))
    min = db.Column(db.Float, nullable=True)
    max = db.Column(db.Float, nullable=True)
    
    def as_dict_child(self):
        return {
            'id': self.id,
            'customer': self.customer.as_dict_child(),
            'representative': self.representative.as_dict_child(),
            'min': self.min,
            'max': self.max
            }

class FinancialData(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    representative_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    type = db.Column(db.Unicode)
    startDate = db.Column(db.Unicode)
    endDate = db.Column(db.Unicode)
    eurSourcesProcurement = db.Column(db.Float, nullable=True)
    eurSourcesGrants = db.Column(db.Float, nullable=True)
    publicFinancingTotal = db.Column(db.Float, nullable=True)
    publicFinancingNational = db.Column(db.Float, nullable=True)
    publicFinancingInfranational = db.Column(db.Float, nullable=True)
    otherSourcesTotal = db.Column(db.Float, nullable=True)
    otherSourcesDonation = db.Column(db.Float, nullable=True)
    otherSourcesContributions = db.Column(db.Float, nullable=True)
    directRepCostsMin = db.Column(db.Float, nullable=True)
    directRepCostsMax = db.Column(db.Float, nullable=True)
    costMin = db.Column(db.Float, nullable=True)
    costMax = db.Column(db.Float, nullable=True)
    costAbsolute = db.Column(db.Float, nullable=True)
    turnoverMin = db.Column(db.Float, nullable=True)
    turnoverMax = db.Column(db.Float, nullable=True)
    turnoverAbsolute = db.Column(db.Float, nullable=True)
    
    sourcesCustomized = db.relationship('FinancialSource',
        backref='financialData', lazy='dynamic')
    turnovers = db.relationship('Turnover',
        backref='financialData', lazy='dynamic')
    
    def as_dict_child(self):
        return self.as_dict()

class Representative(Organisation):
    __mapper_args__ = {'polymorphic_identity': 'representative'}
    #id = db.Column(db.Integer, primary_key=True)
    identificationCode = db.Column(db.Unicode, unique=True)
    status = db.Column(db.Unicode)
    registrationDate = db.Column(db.Unicode)
    lastUpdateDate = db.Column(db.Unicode)
    legalStatus = db.Column(db.Unicode)
    acronym = db.Column(db.Unicode)
    originalName = db.Column(db.Unicode)
    webSiteURL = db.Column(db.Unicode)
    mainCategory = db.Column(db.Unicode)
    subCategory = db.Column(db.Unicode)
    goals = db.Column(db.Unicode)
    networking = db.Column(db.Unicode)
    activities = db.Column(db.Unicode)
    codeOfConduct = db.Column(db.Unicode)

    legalPersonTitle = db.Column(db.Unicode)
    legalPersonFirstName = db.Column(db.Unicode)
    legalPersonLastName = db.Column(db.Unicode)
    legalPersonPosition = db.Column(db.Unicode)

    headPersonTitle = db.Column(db.Unicode)
    headPersonFirstName = db.Column(db.Unicode)
    headPersonLastName = db.Column(db.Unicode)
    headPersonPosition = db.Column(db.Unicode)

    contactStreet = db.Column(db.Unicode)
    contactNumber = db.Column(db.Unicode)
    contactPostCode = db.Column(db.Unicode)
    contactTown = db.Column(db.Unicode)
    contactCountry_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    contactIndicPhone = db.Column(db.Unicode)
    contactPhone = db.Column(db.Unicode)
    contactIndicFax = db.Column(db.Unicode)
    contactFax = db.Column(db.Unicode)
    contactMore = db.Column(db.Unicode)

    interests = db.relationship(Interest, secondary=interests_table,
        backref=db.backref('representatives', lazy='dynamic'))

    actionFields = db.relationship(ActionField, secondary=fields,
        backref=db.backref('representatives', lazy='dynamic'))

    countryOfMembers = db.relationship(Country, secondary=countries_of_members,
        backref=db.backref('representativesMembers', lazy='dynamic'))
    
    memberships = db.relationship(Member, secondary=memberships,
        primaryjoin='Representative.id==memberships.c.representative_id',
        secondaryjoin='Member.id==memberships.c.member_id',
        backref=db.backref('representedBy', lazy='dynamic'))
    
    financialData = db.relationship('FinancialData', uselist=False,
        backref='representative', lazy='dynamic')
    
    turnoversBy = db.relationship('Turnover',
        primaryjoin='Representative.id==Turnover.representative_id',
        backref='representative', lazy='dynamic')

