from typing import Union
from usdm.api.api_base_model import ApiBaseModel
from usdm.api.study import Study
from usdm.api.study_title import StudyTitle
from usdm.api.code import Code
from usdm.api.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm.api.study_definition_document import StudyDefinitionDocument      
from usdm.api.study_version import StudyVersion
from usdm.api.identifier import StudyIdentifier
from usdm.api.organization import Organization
from usdm.base.globals import Globals
from usdm.base.api_instance import APIInstance
from usdm import __model_version__, __package_name__, __package_version__
from uuid import uuid4

class Wrapper(ApiBaseModel):
  study: Study
  usdmVersion: str
  systemName: Union[str, None] = None
  systemVersion: Union[str, None] = None

  

    @classmethod
    def minimum(cls, title: str,identifier: str, version: str) -> 'Wrapper':
        """
        Create a minimum study with the given title, identifier, and version.
        """
        globals = Globals()
        globals.clear()
        api_instance = APIInstance(globals)
        cdisc_code_system = "cdisc.org"
        cdisc_code_system_version = "2023-12-15"
        
        # Define the codes to be used in the study 
        study_type = api_instance.create(Code, {
            "code": "C98388",
            "codeSystem": cdisc_code_system,
            "codeSystemVersion": cdisc_code_system_version,
            "decode": "Interventional Study"
        })
        organization_type = api_instance.create(Code, {
            "code": "C70793",
            "codeSystem": cdisc_code_system,
            "codeSystemVersion": cdisc_code_system_version,
            "decode": "Clinical Study Sponsor",
        })
        doc_status = api_instance.create(Code, {
            "code": "C98388",
            "codeSystem": cdisc_code_system,
            "codeSystemVersion": cdisc_code_system_version,
            "decode": "Interventional Study",
        })


        study_title = api_instance.create(StudyTitle, {
            "text": title,
            "type": study_type
        })

        # Define the protocol documents
        study_protocol_document_version = api_instance.create(StudyProtocolDocumentVersion, {
            "protocolVersion": version,
            "protocolStatus": doc_status
        })
        study_protocol_document = api_instance.create(StudyProtocolDocument, {
            "name": "PROTOCOL",
            "label": "Study Protocol",
            "description": "The study protocol document",
            "versions": [study_protocol_document_version]
        })

        # Define the organization and the study identifier
        organization = api_instance.create(Organization, {
            "name": "Sponsor",
            "organizationType": organization_type,
            "identifier": "To be provided",
            "identifierScheme": "To be provided",
            "legalAddress": None,
        })
        study_identifier = api_instance.create(StudyIdentifier, {
            "studyIdentifier": identifier,
            "studyIdentifierScope": organization
        })

        # Define the study version
        study_version = api_instance.create(StudyVersion, {
            "versionIdentifier": "1",
            "rationale": "To be provided",
            "titles": [study_title],
            "studyDesigns": [],
            "documentVersionId": study_protocol_document_version.id,
            "studyIdentifiers": [study_identifier]
        })
        study = api_instance.create(Study, {
            "id": str(uuid4()),
            "name": "Study",
            "label": "",
            "description": "",
            "versions": [study_version],
            "documentedBy": study_protocol_document,
        })
        
        # Return the wrapper for the study
        return api_instance.create(Wrapper, {
            "study": study,
            "usdmVersion": __model_version__,
            "systemName": f"Python {__package_name__} Package",
            "systemVersion": __package_version__,
        })



    globals.id_manager.clear()
    factory = Factory(globals)
    feedback_reason = factory.item(StudyAmendmentReason, {'code': factory.cdisc_code("C99904x3", "IRB/IEC Feedback")})
    other_reason = factory.item(StudyAmendmentReason, {'code': factory.cdisc_code("C17649", "Other"), "otherReason": "Fix typographical errors"})
    subjects = factory.item(Quantity, {'value': 10.0})
    enrollments = factory.item(SubjectEnrollment, {'type': factory.cdisc_code("C68846", "Global"), 'quantity': subjects})
    amendment = factory.item(StudyAmendment,{"number": "1", "summary": "Updated inclusion criteria", "substantialImpact": True,
                                             "primaryReason": feedback_reason, "secondaryReasons": [other_reason], "enrollments": [enrollments]}) 
    global_scope = factory.item(GeographicScope, {'type': factory.cdisc_code("C68846", "Global")})
    europe_code = factory.alias_code(factory.geo_code('150', 'Europe'), [])
    europe_scope = factory.item(GeographicScope, {'type': factory.cdisc_code("C41129", "Region"), "code": europe_code})
    study_approval_date = factory.item(GovernanceDate, {"name": "D_APPROVE", "label": "Design Approval", "description": "Design approval date", 
                                                  "type": factory.cdisc_code("C132352", "Sponsor Approval Date"), "dateValue": "2006-06-01", "geographicScopes": [global_scope]})
    doc_approval_date = factory.item(GovernanceDate, {"name": "D_APPROVE", "label": "Design Approval", "description": "Design approval date", 
                                             "type": factory.cdisc_code("C99903x1", "Sponsor Approval Date"), "dateValue": "2006-06-01", "geographicScopes": [europe_scope]})
    phase_code = factory.cdisc_code('C12345', 'Phase Code')
    alias_phase = factory.alias_code(phase_code, [])
    self.population = factory.item(StudyDesignPopulation, {'name': 'POP1', 'label': '', 'description': '', 'includesHealthySubjects': True, 'criteria': []})
    cell = factory.item(StudyCell, {'armId': "X", 'epochId': "Y"})
    arm = factory.item(StudyArm, {'name': "Arm1", 'type': factory.cdisc_dummy(), 'dataOriginDescription': 'xxx', 'dataOriginType': factory.cdisc_dummy()})
    epoch = factory.item(StudyEpoch, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'type': factory.cdisc_code('C22222', 'Epoch Code')})
    study_title = factory.item(StudyTitle, {'text': 'Title', 'type': factory.cdisc_code('C44444', 'Official Study Title')})
    study_short_title = factory.item(StudyTitle, {'text': 'Short Title', 'type': factory.cdisc_code('C33333', 'Brief Study Title')})
    study_acronym = factory.item(StudyTitle, {'text': 'ACRONYM', 'type': factory.cdisc_code('C33333', 'Study Acronym')})
    self.study_definition_document_version = factory.item(StudyDefinitionDocumentVersion, {'version': '1', 'status': factory.cdisc_dummy(), 'dateValues': [doc_approval_date]})
    self.study_definition_document = factory.item(StudyDefinitionDocument, {'name': 'PD1', 'label': 'Protocol Document', 'description': '', 
      'language': factory.english(), 'type': factory.cdisc_code('C70817', 'Protocol'), 'templateName': "Sponsor", 
      'versions': [self.study_definition_document_version]})
    self.study_design = factory.item(StudyDesign, {'name': 'Study Design', 'label': '', 'description': '', 
      'rationale': 'Study Design Rationale', 'interventionModel': factory.cdisc_dummy(), 'arms': [arm], 'studyCells': [cell], 
      'epochs': [epoch], 'population': self.population})
    address = factory.item(Address, {'line': 'line 1', 'city': 'City', 'district': 'District', 'state': 'State', 'postalCode': '12345', 'country': factory.code("UKK", "UKK_decode")})
    organization_1 = factory.item(Organization, {'name': 'Sponsor', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456789", 'identifierScheme': "DUNS", 
                                                 'legalAddress': address}) 
    identifier = factory.item(StudyIdentifier, {'text': 'SPONSOR-1234', 'scopeId': organization_1.id})
    organization_2 = factory.item(Organization, {'name': 'Sponsor', 'type': factory.cdisc_code("C188863", "reg 1"), 
                                                 'identifier': "REG 1", 'identifierScheme': "DUNS", 'legalAddress': address}) 
    reg_1_identifier = factory.item(StudyIdentifier, {'text': 'REG 111111', 'scopeId': organization_2.id})
    organization_3 = factory.item(Organization, {'name': 'Sponsor', 'type': factory.cdisc_code("C93453", "reg 2"), 
                                                 'identifier': "REG 2", 'identifierScheme': "DUNS", 'legalAddress': address}) 
    reg_2_identifier = factory.item(StudyIdentifier, {'text': 'REG 222222', 'scopeId': organization_3.id})
    self.study_version = factory.item(StudyVersion, {'versionIdentifier': '1', 'rationale': 'Study version rationale', 'titles': [study_title, study_short_title, study_acronym], 
                                                     'studyDesigns': [self.study_design], 
                                                     'documentVersionId': self.study_definition_document_version.id, 'studyIdentifiers': [identifier, reg_1_identifier, reg_2_identifier], 
                                                     'studyPhase': alias_phase, 'dateValues': [study_approval_date], 'amendments': [amendment], 'organizations': [organization_1, organization_2, organization_3]})
    self.study = factory.item(Study, {'id': None, 'name': 'Study', 'label': '', 'description': '', 'versions': [self.study_version], 'documentedBy': [self.study_definition_document]}) 