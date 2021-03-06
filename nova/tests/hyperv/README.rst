=====================================
OpenStack Hyper-V Nova Testing Architecture
=====================================

The Hyper-V Nova Compute plugin uses Windows Management Instrumentation (WMI)
as the main API for hypervisor related operations.
WMI has a database / procedural oriented nature that can become difficult to
test with a traditional static mock / stub based unit testing approach.

The included Hyper-V testing framework has been developed with the
following goals:

1) Dynamic mock generation.
2) Decoupling. No dependencies on WMI or any other module.
    The tests are designed to work with mocked objects in all cases, including
    OS-dependent (e.g. wmi, os, subprocess) and non-deterministic
    (e.g. time, uuid) modules
3) Transparency. Mocks and real objects can be swapped via DI
    or monkey patching.
4) Platform independence.
5) Tests need to be executed against the real object or against the mocks
    with a simple configuration switch. Development efforts can highly
    benefit from this feature.
6) It must be possible to change a mock's behavior without running the tests
    against the hypervisor (e.g. by manually adding a value / return value).

The tests included in this package include dynamically generated mock objects,
based on the recording of the attribute values and invocations on the
real WMI objects and other OS dependent features.
The generated mock objects are serialized in the nova/tests/hyperv/stubs
directory as gzipped pickled objects.

An environment variable controls the execution mode of the tests.

Recording mode:

NOVA_GENERATE_TEST_MOCKS=True
Tests are executed on the hypervisor (without mocks), and mock objects are
generated.

Replay mode:

NOVA_GENERATE_TEST_MOCKS=
Tests are executed with the existing mock objects (default).

Mock generation is performed by nova.tests.hyperv.mockproxy.MockProxy.
Instances of this class wrap objects that need to be mocked and act as a
delegate on the wrapped object by leveraging Python's __getattr__ feature.
Attribute values and method call return values are recorded at each access.
Objects returned by attributes and method invocations are wrapped in a
MockProxy consistently.
From a caller perspective, the MockProxy is completely transparent,
with the exception of calls to the type(...) builtin function.

At the end of the test, a mock is generated by each MockProxy by calling
the get_mock() method. A mock is represented by an instance of the
nova.tests.hyperv.mockproxy.Mock class.

The Mock class task consists of replicating the behaviour of the mocked
objects / modules by returning the same values in the same order, for example:

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

check_path(path)
# The second time os.path.exists returns True
check_path(path)

The injection of MockProxy / Mock instances is performed by the
nova.tests.hyperv.basetestcase.BaseTestCase class in the setUp()
method via selective monkey patching.
Mocks are serialized in tearDown() during recording.

The actual Hyper-V test case inherits from BaseTestCase:
nova.tests.hyperv.test_hypervapi.HyperVAPITestCase


Future directions:

1) Replace the pickled files with a more generic serialization option (e.g. json)
2) Add methods to statically extend the mocks (e.g. method call return values)
3) Extend an existing framework, e.g. mox
