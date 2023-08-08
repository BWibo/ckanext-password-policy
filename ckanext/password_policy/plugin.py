import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.password_policy.views as views
import ckan.lib.navl.dictization_functions as df
import ckanext.password_policy.helpers as h
from six import string_types


from ckan.common import _

Missing = df.Missing
missing = df.missing


def user_custom_password_validator(key, data, errors, context):
    value = data[key]
    valid_pass = h.custom_password_check(value)

    breakpoint()

    if isinstance(value, Missing):
        pass
    elif not isinstance(value, string_types):
        errors[('password',)].append(_('Passwords must be strings'))
    elif value == '':
        pass
    elif not valid_pass['password_ok']:
        errors[('password',)].append(_('Your password must be 12 characters or '
                                       'longer and contain Uppercase, Lowercase, '
                                       'digit and special character'))
    # elif len(value) < 17:
    #     errors[('password',)].append(_('Your password must be 17 characters or '
    #                                    'longer'))
          
        
class PasswordPolicyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer) 
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'password_policy')
        
    def get_validators(self):
        return {'user_custom_password_validator': user_custom_password_validator}
    

    def get_blueprint(self):
        return views.get_blueprints()


