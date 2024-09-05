from Core.Controllers.Controller import Controller

def testBaseControllerHasListMethod():
    assert hasattr(Controller, 'list') is True

def testBaseControllerHasCreateMethod():
    assert hasattr(Controller, 'create') is True

def testBaseControllerHasUpdateMethod():
    assert hasattr(Controller, 'update') is True

def testBaseControllerHasDeleteMethod():
    assert hasattr(Controller, 'delete') is True

def testBaseControllerHasDestroyMethod():
    assert hasattr(Controller, 'destroy') is True

def testBaseControllerHasViewMethod():
    assert hasattr(Controller, 'view') is True

def testBaseControllerHasTrashMethod():
    assert hasattr(Controller, 'trash') is True

def testBaseControllerHasRestoreMethod():
    assert hasattr(Controller, 'restore') is True
