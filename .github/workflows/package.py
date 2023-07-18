# -*- coding: utf-8 -*-
##############################################################################
# Project TkUtil
#
# CEA/DAM/DSSI, 2020
##############################################################################

from spack import *


class Tkutil(CMakePackage):
    """Bibliotheque d'utilitaires C++"""

    homepage = 'https://github.com/LIHPC-Computational-Geometry/tkutil'
    url = 'https://github.com/LIHPC-Computational-Geometry/tkutil/archive/refs/tags/5.14.0.tar.gz'
    git = 'https://github.com/LIHPC-Computational-Geometry/tkutil.git' 
    maintainers = ['meshing_team']

    depends_on('guitoolkitsvariables', type=('build', 'link'))
    # 5.7.6 is the last python2 only version
    depends_on('python@:2.999', type=('build', 'link'), when='@:5.7.6')
    depends_on('python', type=('build', 'link'), when='@5.7.7:')
    # On a besoin de swig >= 3.0.0 :
    depends_on('swig@3:', type=('build'))
    depends_on('libiconv', type=('build', 'link'))


    version('develop', branch='main')
    version('6.5.0', sha256='a1f1dc27fd0f5bcb8ddeee3f9d895c793f97e21d1cf395d1f607e29a47d0363e')
    version('5.14.0', sha256='e9fdc04f5a8efa4a95648a80422cfaccbb6733b79af2d49fe1af3ace4c748cb3')
    version('5.7.7', sha256='a9ed789f4088ba2bb3f1807d6317f74904fd10911b92cdb50f5c0e7f7ae61dea')
    version('5.7.5', sha256='335300ae3b441b45327d9b0fa4591c096509381b4c355d61fb407cb2eeea62fd')
    version('5.7.2', sha256='36406ad50fb73b07216f19ef34958abcf17171cc32a1d0fb44a7176aa97c03f3')
    version('5.1.0', sha256='949b97c14fcdddfc524978b472aa5129fe140049ada2b1e94717158c1a22b700')
    version('5.0.3', sha256='1fe8250cfd83c640266c54cc15687927f702cebd7d5e0a8396ea318e171f6b9a')
    version('5.0.2', sha256='7ca880377d069af81160458131c4c9c3d57bb24a7c1077f57d681abb02871669')
    version('5.0.0', sha256='9e049bbdf61ce49ff6e8bf246b94bc61a76896146f48b7aa5d5305346c6f9d50')

    variant('shared', default=True, description='Creation de bibliotheques dynamiques')

    def cmake_args(self):
        args = []
        args = [self.define_from_variant('BUILD_SHARED_LIBS', 'shared')]
        if self.spec.satisfies('%intel'):
            args.append('-DCMAKE_CXX_FLAGS="-std=c++11"')

        if self.spec['python'].version < Version('3'):
            args.append('-DUSE_PYTHON_3:BOOL=OFF')
        else:
            args.append('-DUSE_PYTHON_3:BOOL=ON')

        return args
#    def cmake_args(self):
#        spec = self.spec
#        return [
#        print(spec["libiconv"].libs)
#        return []
