import ConfigParser
import sys
import subprocess
import os

# command line arguments configuration
ARGUMENTS_MAP = {
    '-c': {
        'help': "You can specify custom configuration file. By default it's ./browsers.cfg",
        'dst_key': 'config',
        'example': "-f conf/browsers.cfg",
        'default': './browsers.cfg'
    },
    '-b': {
        'help': "You can specify particular destination browser section to run tests. It's possible to specify several browsers",
        'dst_key': 'browsers',
        'example': "-b internetexplorer-9 -b firefox-mac",
        'default': []
    },
    '-t': {
        'help': "Execute single test",
        'dst_key': 'particular_test',
        'example': "test.test_sample_file:TestSampleClass.test_sample_method",
        'default': ''
    },
    '-s': {
        'help': "Execute tests synchronously",
        'dst_key': 'sync',
        'example': "-s 1",
        'default': '1'
    },
    '-h': {
        'help': "Param to display this message",
        'default': False
    },
    }


def help():
    print ""
    for key, args_map in ARGUMENTS_MAP.iteritems():
        print "%(key)s - %(msg)s\n"\
              "     Example: %(example)s\n"\
              "     Default: %(default)s\n" % {
            'key': key,
            'msg': args_map.get('help', ''),
            'example': args_map.get('example', 'Not available'),
            'default': args_map.get('default', 'Not available'),
            }
    sys.exit(0)

def args_parse():
    """
    Parse the arguments
    """

    params_map = dict([
    (key, args_map.get('dst_key'))\
    for key, args_map in ARGUMENTS_MAP.iteritems()
    ])

    defaults = dict([
    (args_map.get('dst_key'), args_map.get('default'))\
    for key, args_map in ARGUMENTS_MAP.iteritems()\
    if 'dst_key' in args_map
    ])

    if '-h'in sys.argv:
        help()

    for param, value in zip(sys.argv[1::2], sys.argv[2::2]):
        if not param in params_map:
            print "Error: Unknown param `%s`" % param
            help()

        prev_value = defaults.get(params_map.get(param), None)

        if isinstance(prev_value, list):
            defaults[params_map.get(param)].append(value)

        else:
            defaults[params_map.get(param)] = value

    return defaults

def runner_config(params):
    #config = ConfigParser.RawConfigParser(allow_no_value=True)
    config = ConfigParser.RawConfigParser()
    config.readfp(open(params.get('config')))

    def config_with_default(section, name, default=None):
        """
        Get value from section or return default value for the field
        """
        try:
            value = config.get(section, name)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            value = default
        return value

    nose_args = config_with_default('runner', 'nose_args', default='')
    nose_single_test_args = config_with_default('runner', 'nose_single_test_args', default='')
    selenium_host = config_with_default('runner', 'selenium_host', 'http://localhost:4444/wd/hub')
    selenium_env = config_with_default('runner', 'selenium_env', 'LOCAL')
    base_url = config_with_default('runner', 'base_url', 'http://beta.qualifiedhardware.com/')
    user_name = config_with_default('runner', 'user_name', 'rohini')
    password = config_with_default('runner', 'password', 'pass123')

    return config, {
        'nose_args': nose_args,
        'nose_single_test_args': nose_single_test_args,
        'selenium_rc_host': selenium_host,
        'selenium_env': selenium_env,
        'base_url': base_url,
        'user_name': user_name,
        'password':password
    }

def read_browsers(params, config):
    """
    Get list of browsers to test project's UI
    """

    browsers = []
    for section in config.sections():
        try:
            name = config.get(section, 'name')
            platform = config.get(section, 'platform')
        except ConfigParser.NoOptionError:
            continue

        try:
            version = config.get(section, 'version')
        except ConfigParser.NoOptionError:
            version = None

        if not name or not platform:
            raise ValueError(
                u"You're not properly configured section '%s': "\
                u"please specify both 'name' and 'platform'" % section)

        if params.get('browsers') and not section in params.get('browsers'):
            continue

        browsers.append({
            'name': name,
            'version': version,
            'platform': platform
        })

    return browsers

def request_platforms(settings, browsers):
    """
    Here we need to create connection to our RPC service server and pass all
    browsers, platforms and its versions
    """
    pass


def release_platform(settings, browser):
    """
    When tests are done for particular browser and platform we can release platform
    """
    pass

def execute_tests(params, settings, browsers):
    """
    Execute tests for different browsers simultaneously
    """

    separate = lambda e="": "%s%s" % ("=" * 60, e)
    particular_test = params.get('particular_test', '')

    for browser in browsers:

        name = browser.get('name')
        version = browser.get('version', None)
        platform = browser.get('platform', 'WINDOWS')

        os.environ["SELENIUM_BROWSER"] = name
        if version:
            os.environ["SELENIUM_BROWSER_VERSION"] = version
        os.environ["SELENIUM_BROWSER_PLATFORM"] = platform
        os.environ["SELENIUM_RC_HOST"] = settings.get('selenium_rc_host')
        os.environ["SELENIUM_ENV"] = settings.get('selenium_env')
        os.environ["BASE_URL"] = settings.get('base_url')
        os.environ["USER_NAME"] = settings.get('user_name')
        os.environ["PASSWORD"] = settings.get('password')

        print separate()
        print "Browser Name: %(name)s\n"\
              "Browser Version: %(version)s\n"\
              "Browser Platform: %(platform)s" % browser
        print "This may take a long time without any output. Please, be patient."
        print separate()

        # execute single test or all tests
        if particular_test == '':
            cmd = "nosetests %s %s" % ((settings.get('nose_args') % browser), particular_test)
        else:
            cmd = "nosetests %s %s" % ((settings.get('nose_single_test_args')), particular_test)

        output, error = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        title = "%(name)s V:%(version)s (%(platform)s)" % browser
        print "\nOutput for: %s\n%s\n" % (title, '-' * 60)
        print output
        print error
        print "\nTests are finished for: %s" % title
        print separate('\n\n')


if __name__ == '__main__':

    params = args_parse()

    config, settings = runner_config(params)
    browsers = read_browsers(params, config)
    request_platforms(settings, browsers)
    execute_tests(params, settings, browsers)

    sys.exit(0)
