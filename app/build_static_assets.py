from webassets import Environment, Bundle

my_env = Environment('static/', 'static/')

common_css = Bundle(
    'css/bootstrap.min.css',
    'vendor/flatui/css/flat-ui.css',
    'css/sb-admin-2.css',
    'vendor/font-awesome-4.1.0/css/font-awesome.min.css',
    'vendor/datepicker/css/datepicker.css',
    'vendor/bootstrap-select/css/bootstrap-select.css',
    output='public/css/common.css'
)

common_js = Bundle(
    'vendor/flatui/js/vendor/jquery.min.js',
    'vendor/datepicker/js/bootstrap-datepicker.js',
    'vendor/bootstrap-select/js/bootstrap-select.js',
    'vendor/flatui/js/flat-ui.min.js',
    'js/d3.v3.js',
    'js/mpld3.v0.2.js',
    output='public/js/common.js'
)
my_env.register('css_all', common_css)
my_env.register('js_all', common_js)
my_env['css_all'].urls()
my_env['js_all'].urls()
