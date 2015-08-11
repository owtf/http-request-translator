"""

:synopsis: Define the specialize script classes that will generate the script code.

"""

from .base import AbstractScript
from .templates import bash_template, php_template, python_template, ruby_template


class BashScript(AbstractScript):

    code_begin = bash_template.code_begin
    code_header = bash_template.code_header
    code_proxy = bash_template.code_proxy
    code_post = bash_template.code_post
    code_search = bash_template.code_search
    code_nosearch = bash_template.code_nosearch

    def _generate_request(self):
        code = self.code_nosearch.format(
            method=self.details.get('method', ''),
            url=self.url,
            headers=self._generate_headers())
        if self.search:
            code += self.code_search.format(search_string=self.search)
        return code


class PHPScript(AbstractScript):

    code_begin = php_template.code_begin
    code_header = php_template.code_header
    code_proxy = php_template.code_proxy
    code_post = php_template.code_post
    code_search = php_template.code_search
    code_nosearch = php_template.code_nosearch

    def _generate_begin(self):
        return self.code_begin.format(url=self.url) + self._generate_headers()


class PythonScript(AbstractScript):

    code_begin = python_template.code_begin
    code_proxy = python_template.code_proxy
    code_post = python_template.code_post
    code_https = python_template.code_https
    code_search = python_template.code_search
    code_nosearch = python_template.code_nosearch

    def _generate_begin(self):
        return self.code_begin.format(url=self.url, headers=str(self.headers))


class RubyScript(AbstractScript):

    code_begin = ruby_template.code_begin
    code_header = ruby_template.code_header
    code_proxy = ruby_template.code_proxy
    code_post = ruby_template.code_post
    code_search = ruby_template.code_search
    code_nosearch = ruby_template.code_nosearch

    def _generate_begin(self):
        code = self.code_begin.format(url=self.url, method=self.details.get('method', '').strip().lower())
        code += ruby_template.code_headers.format(headers=self._generate_headers())
        return code
