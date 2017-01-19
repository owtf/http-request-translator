"""

:synopsis: Define the specialize script classes that will generate the script code.

"""

from .base import AbstractScript


class BashScript(AbstractScript):

    """Extended `AbstractScript` class for Bash script code generation.
    Fills code variables for the request from `bash_template`.
    Overrides `_generate_request` method to generate bash specific code.
    """

    __language__ = 'bash'

    def _generate_request(self):
        code = self.code_nosearch.format(
            method=self.details.get('method', ''),
            url=self.url,
            headers=self._generate_headers())
        return code


class PHPScript(AbstractScript):

    """Extended `AbstractScript` class for PHP script code generation.
    Fills code variables for the request from `php_template`.
    Overrides `_generate_begin` method to generate php specific code.
    """

    __language__ = 'php'

    def _generate_begin(self):
        return self.code_begin.format(url=self.url) + self._generate_headers()


class PythonScript(AbstractScript):

    """Extended `AbstractScript` class for Python script code generation.
    Fills code variables for the request from `python_template`.
    Overrides `_generate_begin` method to generate python specific code.
    """

    __language__ = 'python'

    def _generate_begin(self):
        return self.code_begin.format(url=self.url, headers=str(self.headers))


class RubyScript(AbstractScript):

    """Extended `AbstractScript` class for Ruby script code generation.
    Fills code variables for the request from `ruby_template`.
    Overrides `_generate_begin` method to generate Ruby specific code.
    """

    __language__ = 'ruby'

    def _generate_begin(self):
        code = self.code_begin.format(url=self.url, method=self.details.get('method', '').strip().lower())
        code += self.code_headers.format(headers=self._generate_headers())
        return code
