from collections import OrderedDict
import copy

from BaseIntegrationModule import BaseIntegrationModule

ENTITY_NAME = 'citrix_adc_appfw_xmlerrorpage'

####### TESTBED DATA STARTS ###########

# PREREQUISITES/Testbed
def get_testbed_data(test_type='citrix_adc_direct_calls', ns_version='12.1'):
    testbed_data = []
    return testbed_data
    
####### TESTBED DATA ENDS ###########



####### ACTUAL MODULE INPUT DATA STARTS ###############

def get_input_data(test_type='citrix_adc_direct_calls', ns_version='12.1'):
    input_data = OrderedDict()
    # For Submodule 'citrix_adc_appfw_xmlerrorpage'
    submodObj = BaseIntegrationModule(test_type, ENTITY_NAME, 'citrix_adc_appfw_xmlerrorpage')

    # Create error.xml
    create_error_xml = [OrderedDict([
        ('name', 'create error xml'),
        ('delegate_to', 'localhost'),
        ('citrix_adc_nitro_request', OrderedDict([
            ('nitro_user', '{{ nitro_user }}'),
            ('nitro_pass', '{{ nitro_pass }}'),
            ('nsip', '{{ nsip }}'),

            ('operation', 'add'),

            ('resource', 'systemfile'),
            ('attributes', OrderedDict([
                ('filename', 'error.xml'),
                ('filecontent', '{{ \'<error></error>\' | b64encode }}'),
                ('filelocation',  '/var/tmp')
            ])),
        ])),
    ])]
    submodObj.add_raw_operation('Create error page', copy.deepcopy(create_error_xml), run_once=True)

    import_data = OrderedDict(
        [
            ('name', 'integration_test'),
            ('src', 'local://error.xml'),
            ('comment', 'integration test comment'),
            ('overwrite', True),
        ]
    )
   
    remove_data = copy.deepcopy(import_data)
    remove_data['state'] = 'absent'    

    submodObj.add_operation('import', import_data)
    submodObj.add_operation('remove', remove_data)

    # Delete error.xml
    delete_error_xml = [OrderedDict([
        ('name', 'setup auditnslogpolicy'),
        ('delegate_to', 'localhost'),
        ('citrix_adc_nitro_request', OrderedDict([
            ('nitro_user', '{{ nitro_user }}'),
            ('nitro_pass', '{{ nitro_pass }}'),
            ('nsip', '{{ nsip }}'),

            ('operation', 'delete_by_args'),

            ('resource', 'systemfile/error.xml'),
            ('args', OrderedDict([
                ('filelocation',  '\'%2Fvar%2Ftmp\'')
            ])),
        ])),
    ])]
    submodObj.add_raw_operation('Delete error xml', copy.deepcopy(delete_error_xml), run_once=True)
    
    input_data.update({submodObj.get_sub_mod_name(): copy.deepcopy(submodObj.get_mod_attrib())})
    
    return input_data

####### ACTUAL MODULE INPUT DATA ENDS ###############
